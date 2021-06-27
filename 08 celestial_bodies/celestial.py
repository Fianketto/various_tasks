from abc import ABC, abstractmethod
from math import pi


ME = 5.972E+24          # Масса Земли
MS = 333_030 * ME       # Масса Солнца
RE = 6_371_000          # Радиус Земли
RS = 109.076 * RE       # Радиус Солнца
AU = 149_597_870_700    # Радиус рбиты Земли (астрономическая единица)
G = 6.6743E-11          # Гравитационная постянная


# Абстрактный класс "Небеное тело"
class CelestialBody(ABC):
    def __init__(self, name, mass, radius):
        self.name = name
        self.r = radius
        self.m = mass
        self.orbital_r = None
        self.type = None

    def __repr__(self):
        return f"{self.name}: {self.type} массой {self.m} МЗ (масс Земли) и радиусом {self.r} RЗ (радиусов Земли)"

    # Установить радиус орбиты (в астрономических единицах)
    def set_orbital_radius(self, orbital_radius):
        self.orbital_r = orbital_radius

    # Захватить небесное тело в качестве спутника
    @abstractmethod
    def capture_body(self, body):
        print(f"Попытка захватить небесное тело {body.name}")


# Класс Звезда
class Star(CelestialBody):
    def __init__(self, name, mass, radius):
        super().__init__(name, mass, radius)
        self.type = "Звезда"
        self.planets = []

    def __repr__(self):
        repr = f"{self.name}: {self.type} массой {self.m} МЗ (масс Земли) и радиусом {self.r} RЗ (радиусов Земли)"
        if not self.planets:
            repr += "\nНет планет, обращающихся вокруг."
        else:
            repr += f"\nСписок планет: {[p.name for p in self.planets]}"
        return repr

    def capture_body(self, body):
        super().capture_body(body)
        self.__capture_planet(body)

    # Захватить планету
    def __capture_planet(self, planet):
        if not isinstance(planet, Planet):
            print(f"Можно захватить только планеты. {planet.name} не является планетой!")
        elif planet.mother_star:
            print(f"{planet.name} уже обращается вокруг звезды {planet.mother_star.name}")
        else:
            self.planets.append(planet)
            planet.mother_star = self
            print(f"{planet.name} теперь обращается вокруг звезды {self.name}")

    # Удалить планету из захваченных
    def remove_body(self, planet):
        if not isinstance(planet, Planet):
            print(f"{planet.name} не является планетой! (Тип - {planet.type})")
        elif not self == planet.mother_star:
            print(f"Невозможно удалить: {planet.name} не обращается вокруг звезды {self.name}")
        else:
            for i in range(len(self.planets)):
                if self.planets[i] == planet:
                    del self.planets[i]
                    break
            planet.mother_star = None
            planet.orbital_r = None
            print(f"Планета {planet.name} перестала обращаться вокруг звезды {self.name}")


# Класс Планета
class Planet(CelestialBody):
    def __init__(self, name, mass, radius):
        super().__init__(name, mass, radius)
        self.type = "Планета"
        self.mother_star = None
        self.satellites = []

    def __repr__(self):
        repr = f"{self.name}: {self.type} массой {self.m} МЗ (масс Земли) и радиусом {self.r} RЗ (радиусов Земли)"
        if not self.mother_star:
            repr += "\nНе обращается вокруг какой-либо звезды"
        else:
            repr += f"\nОбращается вокруг звезды {self.mother_star.name}"
        if not self.satellites:
            repr += "\nСпутников нет"
        else:
            repr += f"\nСписок спутников: {[s.name for s in self.satellites]}"
        return repr

    # Вывести период обращения вокруг звезды
    def get_orbital_period(self):
        if not self.mother_star:
            print(f"{self.name} не обращается вокруг какой-либо звезды")
        elif not self.orbital_r:
            print(f"Сначала задайте радиус орбиты")
        else:
            t = 2 * pi * (((self.orbital_r*AU)**3)/(G * ME * (self.m + self.mother_star.m))) ** 0.5
            t = t / 3600 / 24 / 365
            print(f"Период вращения планеты {self.name} вокруг звезды {self.mother_star.name} в земных годах: "
                  f"{round(t, 2)} ({round(t * 365, 2)} земных дн.)")

    def capture_body(self, body):
        super().capture_body(body)
        self.__capture_satellite(body)

    # Захватить спутник
    def __capture_satellite(self, satellite):
        if not isinstance(satellite, Satellite):
            print(f"Тип объекта {satellite.name} - {satellite.type}. Нельзя захватить!")
        elif satellite.mother_planet:
            print(f"{satellite.name} уже является спутником планеты {satellite.mother_planet.name}")
        else:
            self.satellites.append(satellite)
            satellite.mother_planet = self
            print(f"{satellite.name} стал(а) спутником планеты {self.name}")

    # Удалить спутник из захваченных
    def remove_body(self, satellite):
        if not isinstance(satellite, Satellite):
            print(f"{satellite.name} не является спутником! (Тип - {satellite.type})")
        elif not self == satellite.mother_planet:
            print(f"Невозможно удалить: {satellite.name} не является спутником планеты {self.name}")
        else:
            for i in range(len(self.satellites)):
                if self.satellites[i] == satellite:
                    del self.satellites[i]
                    break
            satellite.mother_planet = None
            satellite.orbital_r = None
            print(f"{satellite.name} успешно удален(а) из списка спутников планеты {self.name}")


# Класс Спутник
class Satellite(CelestialBody):
    def __init__(self, name, mass, radius):
        super().__init__(name, mass, radius)
        self.type = "Спутник"
        self.mother_planet = None

    # Вывести период обращения вокруг планеты
    def get_orbital_period(self):
        if not self.mother_planet:
            print(f"{self.name} не обращается вокруг какой-либо планеты")
        elif not self.orbital_r:
            print(f"Сначала задайте радиус орбиты")
        else:
            t = 2 * pi * (((self.orbital_r*AU)**3)/(G * ME * (self.m + self.mother_planet.m))) ** 0.5
            t = t / 3600 / 24 / 365
            print(f"Период вращения спутника {self.name} вокруг планеты {self.mother_planet.name} в земных годах: "
                  f"{round(t, 2)} ({round(t * 365, 2)} земных дн.)")

    def capture_body(self, body):
        return "Спутник не может захватывать другие объекты"

    def __repr__(self):
        repr = f"{self.name}: {self.type} массой {self.m} МЗ (масс Земли) и радиусом {self.r} RЗ (радиусов Земли)"
        if not self.mother_planet:
            repr += "\nНе обращается вокруг какой-либо планеты"
        else:
            repr += f"\nОбращается вокруг планеты {self.mother_planet.name}"
        return repr


if __name__ == '__main__':
    # звезды
    sun = Star("Солнце", 333030, 109.076)
    alpha = Star("Альфа Центавра", 1.1 * MS, 1.227 * RS)
    # планеты
    earth = Planet("Земля", 1, 1)               # 1au,          1y
    saturn = Planet("Сатурн", 95.2, 9.46)       # 10.116au,     29.46y
    # спутники
    moon = Satellite("Луна", 0.0123, 0.273)     # 0.0027106au,  27.3d
    titan = Satellite("Титан", 0.0225, 0.804)   # 0.0081677au,  15.9d

    # захватываем объекты
    sun.capture_body(earth)
    sun.capture_body(saturn)
    earth.capture_body(moon)
    saturn.capture_body(titan)

    # задаем радиусы
    earth.set_orbital_radius(1)
    saturn.set_orbital_radius(10.116)
    moon.set_orbital_radius(0.0027106)
    titan.set_orbital_radius(0.0081677)

    # выводим периоды
    earth.get_orbital_period()
    saturn.get_orbital_period()
    moon.get_orbital_period()
    titan.get_orbital_period()
