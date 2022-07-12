class CyclicIterator:
    def __init__(self, value):
        self.value = value
        self.iterator = iter(self.value)
        

    def __iter__(self):
        return self 

    def __next__(self):
        try:
            return next(self.iterator)
        except StopIteration:
            self.iterator = iter(self.value)
            return next(self.iterator)
            


if __name__ == '__main__':
    cyclic_iterator = CyclicIterator(range(3))
    for i in cyclic_iterator:
        print(i)