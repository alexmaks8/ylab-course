import json
from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException

from sqlmodel import Session

from src.api.v1.resources.auth import AuthHandler
from src.api.v1.schemas.users import UserInput, UserLogin
from src.db import get_session
from src.models.users import User
from src.services.cache_services import CacheRedisService, get_cache_service
from src.services.mixins import CacheServiceMixin, UserServiceMixin


__all__ = ("UserService", "get_user_service")


class UserService(UserServiceMixin):
    """Для обработки запросов пользователя."""

    auth_handler = AuthHandler()
    hours_access_tkn = 1    # время жизни access токена
    hours_refresh_tkn = 48   # время жизни refresh токена

    def __init__(self, session: Session, cache_service: CacheRedisService):
        super().__init__(session)
        self.cache_service = cache_service


    def register_service(self, user_info: UserInput):
        """Регистрация."""
        users = self.select_all_users()
        if any(x.username == user_info.username for x in users):
            raise HTTPException(status_code=400, detail='Username is taken')
        hashed_pwd = self.auth_handler.get_password_hash(user_info.password)
        while True:
            uuid_gen = self.auth_handler.get_a_uuid()
            if any(x.uuid == uuid_gen for x in users):
                continue
            else:
                break
        u = User(username=user_info.username, password=hashed_pwd, email=user_info.email, uuid=uuid_gen)
        self.session.add(u)
        self.session.commit()
        user = self.session.query(User).filter(User.username == user_info.username).first()
        return user.dict()


    def login_service(self, user_info: UserLogin):
        """Войти через логин и пароль."""
        user = self.session.query(User).filter(User.username == user_info.username).first()
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found.")
        self.cache_service.set_user_to_cache_db0(user)
        user = user.dict()
        verified = self.auth_handler.verify_password(user_info.password, user["password"])
        if not verified:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Invalid username and/or password')
        # генерируем access_token refresh_token, где новые токены добавятся в redis
        access_token, refresh_token = self.generate_token(user=user)
        return {'access_token': access_token, "refresh_token": refresh_token}


    def refresh_token(self, payload_info):
        """Обновить токены, только по refresh token!."""
        payload = payload_info[0]
        token = payload_info[1]
        credentials_exception = HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Could not validate.")
        if payload["type"] == "refresh":
            if cached_user := self.cache_service.get_user_from_cache_db0(payload["user_uuid"]):
                user_found = json.loads(cached_user)
            else:
                user_found = self.session.query(User).filter(User.uuid == payload["user_uuid"]).first()
                user_found = user_found.dict()
            # генерируем access_token refresh_token, где новые токены добавятся в redis
            access_token, refresh_token = self.generate_token(user=user_found, old_refresh_tkn=token)
            return {'access_token': access_token, "refresh_token": refresh_token}
        raise credentials_exception


    def check_access_tkn(self, jti_token):
        """Проверить и вернуть при наличии access токен из основного кеша."""
        if self.cache_service.check_access_tkn_in_cache(jti_token):
            return True


    def check_refresh_tkn(self, payload_info):
        """Проверить наличие refresh токен в списке разрешенных."""
        user_uuid = payload_info[0]['user_uuid']
        token = payload_info[1]
        if self.cache_service.check_refresh_tkn_in_cache(user_uuid, token):
            return True


    def get_current_user(self, user_uuid):
        """Получить пользователя по uuid."""
        credentials_exception = HTTPException(status_code=401, detail='Could not validate credentials')
        if user_uuid is None:
            raise credentials_exception
        if cached_user := self.cache_service.get_user_from_cache_db0(user_uuid):
            return json.loads(cached_user)
        user = self.session.query(User).filter(User.uuid == user_uuid).first()
        return user.dict() if user else None


    def patch_current_user(self, payload_info, update_data):
        """Редактировать пользователя."""
        user_uuid = payload_info[0]['user_uuid']
        old_rfrsh_uuid = payload_info[0]['rfi']
        patch_user = self.session.query(User).filter(User.uuid == user_uuid).first()
        patch_data = update_data.dict(exclude_unset=True)
        for key, value in patch_data.items():
            setattr(patch_user, key, value)
        self.session.add(patch_user)
        self.session.commit()
        self.session.refresh(patch_user)
        self.cache_service.set_user_to_cache_db0(patch_user)
        # self.cache_service.delete_access_tkn_permission(payload_info)
        access_token, refresh_token = self.generate_token(patch_user.dict(), rfrsh_uuid=old_rfrsh_uuid)
        return patch_user, access_token if patch_user else None


    def delete_current_user(self, user_uuid, payload_info):
        """Удалить пользователя."""
        user = self.session.query(User).filter(User.uuid == user_uuid).first()
        self.cache_service.delete_user_from_cache_db0(user_uuid)
        self.session.delete(user)
        self.session.commit()
        self.cache_service.delete_access_tkn_permission(payload_info)
        self.cache_service.delete_all_refresh_tkn(user_uuid)
        return "msg: user deleted" if user else None


    def select_all_users(self):
        """Выбрать всех пользователей."""
        all_users = self.session.query(User).order_by(User.created_at).all()
        return all_users


    def generate_token(self, user, old_refresh_tkn=False, rfrsh_uuid=False):
        """Генерирация access_token и refresh_token. Добавление их в redis.
        """
        jti_token = self.auth_handler.get_a_uuid()
        if rfrsh_uuid is False:
            rfrsh_uuid = self.auth_handler.get_a_uuid()
        user_uuid = user["uuid"]
        username = user["username"]
        email = user["email"]
        is_super = user["is_superuser"]
        hours_access_tkn = self.hours_access_tkn    # время access токена
        hours_refresh_tkn = self.hours_refresh_tkn   # время refresh токена
        access_token = self.auth_handler.encode_token(type_token="access", username=username, email=email,
                                                      is_super=is_super, user_uuid=user_uuid, hours=hours_access_tkn,
                                                      rfrsh_uuid=rfrsh_uuid, jti_token=jti_token)
        refresh_token = self.auth_handler.encode_token(type_token="refresh", username=username, email=email,
                                                       is_super=is_super, user_uuid=user_uuid, hours=hours_refresh_tkn,
                                                       rfrsh_uuid=rfrsh_uuid, jti_token=jti_token)
        self.cache_service.add_access_token_to_cache(jti_token, access_token, hours_access_tkn)
        self.cache_service.add_access_token_to_cache(rfrsh_uuid, refresh_token, hours_refresh_tkn)
        self.cache_service.cache_active_refresh_tkn_list(user_uuid, refresh_token, hours_refresh_tkn)
        # Удаление старых токенов и перенос в блеклист при необходимости
        if old_refresh_tkn:
            self.cache_service.delete_refresh_tkn_from_list(user_uuid=user_uuid, oldtoken=old_refresh_tkn)
            if payload_rfrsh_tkn := self.auth_handler.decode_token(old_refresh_tkn):
                if old_access_tkn := self.cache_service.check_access_tkn_in_cache(payload_rfrsh_tkn["jti"]):
                    payload_access_tkn = self.auth_handler.decode_token(old_access_tkn)
                    result = (payload_access_tkn, old_access_tkn)
                    self.cache_service.delete_access_tkn_permission(result)
        return access_token, refresh_token


    def logout(self, payload_info):
        """Метод выхода из аккаунта."""
        user_uuid = payload_info[0]["user_uuid"]
        rfi = payload_info[0]["rfi"]
        self.cache_service.delete_access_tkn_permission(payload_info)
        old_refresh_tkn = self.cache_service.check_access_tkn_in_cache(rfi)
        self.cache_service.delete_refresh_tkn_from_list(
            user_uuid=user_uuid, oldtoken=old_refresh_tkn.decode("utf-8"), rfi=rfi)
        return True


    def logout_all(self, payload_info):
        """Выйти со всех устройств."""
        user_uuid = payload_info[0]["user_uuid"]
        self.cache_service.delete_all_refresh_tkn(user_uuid)
        return True


@lru_cache()
def get_user_service(
    cache_service: CacheServiceMixin = Depends(get_cache_service),
    session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache_service=cache_service, session=session)
