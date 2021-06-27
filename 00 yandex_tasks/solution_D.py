class Vehicle:
    def __init__(self, v_id, v_type, v_speed):
        self.id = v_id
        self.type = v_type
        self.speed = v_speed
        self.till_finish = 0

    def recalculate_speed(self, coefficient):
        self.speed = self.speed * (1 - coefficient)

    def calculate_till_finish(self, track_distance, race_time):
        self.till_finish = track_distance - ((self.speed * race_time) % track_distance)
        if self.till_finish == track_distance:
            self.till_finish = 0


class Car(Vehicle):
    fuel_influence = {98: 0.0, 95: 0.1, 92: 0.2}

    def __init__(self, v_id, v_type, v_speed, fuel_type):
        super().__init__(v_id, v_type, v_speed)
        self.fuel_type = fuel_type
        coefficient = self.__class__.fuel_influence[self.fuel_type]
        self.recalculate_speed(coefficient)


class Motorcycle(Car):
    fuel_influence = {98: 0.0, 95: 0.2, 92: 0.4}

    def __init__(self, v_id, v_type, v_speed, fuel_type):
        super().__init__(v_id, v_type, v_speed, fuel_type)


class Wagon(Vehicle):
    def __init__(self, v_id, v_type, v_speed):
        super().__init__(v_id, v_type, v_speed)


vehicle_class = {1: Car, 2: Motorcycle, 3: Wagon}
n, m, t = tuple(map(int, input().split()))
vehicles = []
for i in range(n):
    params = tuple(map(int, input().split()))
    vehicle = vehicle_class[params[1]](*params)
    vehicle.calculate_till_finish(m, t)
    vehicles.append(vehicle)

vehicles = sorted(sorted(vehicles, key=lambda x: x.id), key=lambda x: x.till_finish)
print(vehicles[0].id)
