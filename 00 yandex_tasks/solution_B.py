class AbstractCat:
    MAX_WEIGHT = 100
    FOOD_TO_GROW = 10

    def __init__(self):
        self.weight = 0
        self.food_left = 0

    def eat(self, food):
        current_food_count = food + self.food_left
        self.food_left = current_food_count % AbstractCat.FOOD_TO_GROW
        self.weight += current_food_count // AbstractCat.FOOD_TO_GROW
        self.weight = min(self.weight, AbstractCat.MAX_WEIGHT)

    def __str__(self):
        return f"{self.__class__.__name__} ({self.weight})"


class Kitten(AbstractCat):
    SNORE_COEFFICIENT = 5

    def __init__(self, weight):
        super().__init__()
        self.weight = weight

    def sleep(self):
        return "Snore" * (self.weight // Kitten.SNORE_COEFFICIENT)

    @staticmethod
    def meow():
        return "meow..."


class Cat(Kitten):
    def __init__(self, weight, name):
        super().__init__(weight)
        self.name = name

    def get_name(self):
        return self.name

    @staticmethod
    def meow():
        return "MEOW..."

    @staticmethod
    def catch_mice():
        return "Got it!"
