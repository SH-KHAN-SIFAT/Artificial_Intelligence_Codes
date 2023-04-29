import math
import random
import csv
from collections import deque

engine_file = "engines.txt"
tire_file = "tires.txt"
transmission_file = "transmissions.txt"
valid_cars_file = "valid_book.csv"

valid_cars = set()


class Car:
    def __init__(self, engine, tire, transmission, roof):
        self.transmission = transmission
        self.engine = engine
        self.tire = tire
        self.roof = roof

    def __eq__(self, other):
        if isinstance(other, Car):
            return self.engine == other.engine and self.tire == other.tire and self.transmission == other.transmission and self.roof == other.roof
        return False

    def __hash__(self):
        return hash((self.engine, self.tire, self.transmission, self.roof))


def load_cars(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for engine, tire, transmission, roof in reader:
            valid_cars.add(Car(engine, tire, transmission, roof))


def content_reader(filename):
    with open(filename) as file:
        container = [line.rstrip() for line in file]
        return container


# compare with the target
# car2 -> target
def compare_with_target(car1, car2):
    num_mismatched = 0
    if car1.transmission != car2.transmission:
        num_mismatched += 1
    if car1.engine != car2.engine:
        num_mismatched += 1
    if car1.tire != car2.tire:
        num_mismatched += 1
    if car1.roof != car2.roof:
        num_mismatched += 1
    return num_mismatched


def delta_e(parent_car, child_car, target):
    return compare_with_target(parent_car, target) - compare_with_target(child_car, target)


def get_e(delta_e, level):
    return math.e ** (delta_e / level)


engines = content_reader(engine_file)
transmission = content_reader(transmission_file)
tires = content_reader(tire_file)
roofs = ["Sunroof", "Moonroof", "Noroof"]

start_car = Car("EFI", "Danlop", "AT", "Noroof")
goal_car = Car("V12", "Pirelli", "CVT", "Sunroof")
#goal_car = Car("EFI", "Danlop", "AT", "Moonroof")

load_cars(valid_cars_file)

frontier = deque()
level = -1
seen = set()
seen.add(start_car)
frontier.append(start_car)
goal_reached = False

while frontier:
    level += 1
    # explore the current level

    children = deque()
    while frontier:
        current_car = frontier.popleft()
        current_engine = current_car.engine
        current_tire = current_car.tire
        current_transmission = current_car.transmission
        current_roof = current_car.roof

        for engine in engines:
            candidate_car = Car(engine, current_tire, current_transmission, current_roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(level + 1)
                    goal_reached = True
                    break
                # check if this candidate_car is worthy: calculate delta E
                # if delta E > 0 just pick the child
                # if delta E <= 0 pick the child with some probability
                if compare_with_target(current_car, goal_car) > compare_with_target(candidate_car, goal_car):
                    children.append(candidate_car)
                    seen.add(candidate_car)
                elif random.uniform(0, 1) <= get_e(delta_e(current_car, candidate_car, goal_car), 1 / level):
                    children.append(candidate_car)
                    seen.add(candidate_car)
        if goal_reached:
            break
        for tire in tires:
            candidate_car = Car(current_engine, tire, current_transmission, current_roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(level + 1)
                    goal_reached = True
                    break
                if compare_with_target(current_car, goal_car) > compare_with_target(candidate_car, goal_car):
                    children.append(candidate_car)
                    seen.add(candidate_car)
                elif random.uniform(0, 1) <= get_e(delta_e(current_car, candidate_car, goal_car), 1 / max(1, level)):
                    children.append(candidate_car)
                    seen.add(candidate_car)
        if goal_reached:
            break
        for transmission in transmission:
            candidate_car = Car(current_engine, current_tire, transmission, current_roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(level + 1)
                    goal_reached = True
                    break
                if compare_with_target(current_car, goal_car) > compare_with_target(candidate_car, goal_car):
                    children.append(candidate_car)
                    seen.add(candidate_car)
                elif random.uniform(0, 1) <= get_e(delta_e(current_car, candidate_car, goal_car), 1 /max(1, level)):
                    children.append(candidate_car)
                    seen.add(candidate_car)
        if goal_reached:
            break
        for roof in roofs:
            candidate_car = Car(current_engine, current_tire, current_transmission, roof)
            if candidate_car not in seen and candidate_car in valid_cars:
                if candidate_car == goal_car:
                    print(level + 1)
                    goal_reached = True
                    break
                if compare_with_target(current_car, goal_car) > compare_with_target(candidate_car, goal_car):
                    children.append(candidate_car)
                    seen.add(candidate_car)
                elif random.uniform(0, 1) <= get_e(delta_e(current_car, candidate_car, goal_car), 1/ max(1, level)):
                    children.append(candidate_car)
                    seen.add(candidate_car)
        if goal_reached:
            break
    if goal_reached:
        break
    frontier = children

print(level + 1)








