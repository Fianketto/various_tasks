class PearsBasket:
    def __init__(self, pear_count):
        self.pear_count = max(pear_count, 0)

    def __str__(self):
        return str(self.pear_count)

    def __repr__(self):
        return f"PearsBasket({self.pear_count})"

    def __floordiv__(self, n):
        basket_count = n
        pear_count = self.pear_count // n
        baskets = [PearsBasket(pear_count) for i in range(basket_count)]
        pears_left = self.pear_count - pear_count * n
        if pears_left > 0 or not baskets:
            baskets.append(PearsBasket(pears_left))
        return baskets

    def __mod__(self, n):
        return self.pear_count % n

    def __add__(self, other):
        if isinstance(other, self.__class__):
            return PearsBasket(max(0, self.pear_count + other.pear_count))
        else:
            self.pear_count = max(0, self.pear_count + other)

    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return PearsBasket(max(0, self.pear_count - other.pear_count))
        self.pear_count = max(0, self.pear_count - other)


pb = PearsBasket(17)
array = pb // 4
print(array)
pb_2 = PearsBasket(13)
pb_3 = pb + pb_2
print(pb_3)
print(pb_3 % 7)
pb - 2
print([pb])
