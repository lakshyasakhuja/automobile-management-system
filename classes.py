'''
NAME: LAKSHYA SAKHUJA
SID: 540863213
UNIKEY: LSAK0709
USYD CODE CITATION ACKNOWLEDGEMENT
I declare that the given code was written by me and is my own work.
'''

'''
Module containing class definitions and decorators for the Automobile Management System.
Includes classes:
- Vehicle
- Car
- ElectricCar
- Bike
'''

import time  # import the time module for time-related functions.
from functools import wraps  # import wraps decorator from functools module.
import numpy as np  # import numpy library as np for numerical operations.

def log_action(func):
    """Decorator to log the action with a timestamp."""
    @wraps(func)  # preserve the metadata of the original function.
    def wrapper(*args, **kwargs):
        action_start_time = time.strftime("%Y-%m-%d %H:%M:%S")  # record the start time of the action.
        print(f"\nAction '{func.__name__}' started at {action_start_time}")  # print a message indicating the action has started.
        result = func(*args, **kwargs)  # execute the original function and store the result.
        print(f"Action '{func.__name__}' completed.")  # print a message indicating the action has completed.
        return result  # return the result of the original function.
    return wrapper  # return the wrapper function.

class Vehicle:
    """Base class for all vehicles, containing common attributes and methods."""

    all_vehicles = []  # class variable to store all vehicles.

    def __init__(self, brand, model, year, price, color, add_to_inventory=True):
        self.brand = brand  # set the brand of the vehicle.
        self.model = model  # set the model of the vehicle.
        self.year = year  # set the manufacturing year of the vehicle.
        self.price = price  # set the price of the vehicle.
        self.color = color  # set the color of the vehicle.
        if add_to_inventory:  # check if the vehicle should be added to the inventory.
            Vehicle.all_vehicles.append(self)  # add the vehicle to the class variable 'all_vehicles'.

    def get_info(self):
        """Returns basic vehicle information as a string."""
        return (
            f"{self.brand} {self.model}, Year: {self.year}, Color: {self.color}, "
            f"Price: ${self.price:.2f}"
        )  # return a formatted string with vehicle details.

    def apply_discount(self, discount_percent):
        """Applies a discount to the vehicle's price."""
        self.price *= (1 - discount_percent / 100)  # reduce the price by the given discount percentage.

    @staticmethod
    def display_inventory():
        """Displays all vehicles in a tabular format with a 'Type' column."""
        from tabulate import tabulate  # import 'tabulate' function for table display.
        if not Vehicle.all_vehicles:  # check if there are any vehicles in the inventory.
            print("No vehicles available.")  # inform the user that no vehicles are available.
            return  # exit the function.
        table = list(
            (
                [
                    i + 1,  # vehicle index number.
                    (
                        "Car"
                        if isinstance(vehicle, Car)
                        and not isinstance(vehicle, ElectricCar)
                        else "Electric Car"
                        if isinstance(vehicle, ElectricCar)
                        else "Bike"
                        if isinstance(vehicle, Bike)
                        else "Unknown"
                    ),  # determine the type of vehicle.
                    vehicle.brand,  # vehicle brand.
                    vehicle.model,  # vehicle model.
                    vehicle.year,  # vehicle year.
                    vehicle.color,  # vehicle color.
                    f"${vehicle.price:.2f}",  # vehicle price formatted as currency.
                ]
                for i, vehicle in enumerate(Vehicle.all_vehicles)  # enumerate over all vehicles.
            )
        )  # create a list of vehicle data for the table display.
        headers = ["Index", "Type", "Brand", "Model", "Year", "Color", "Price"]  # define the headers for the table.
        print(tabulate(table, headers, tablefmt="grid"))  # print the table using 'tabulate'.

    def to_line(self):
        """Converts the vehicle instance to a line of text."""
        data = [
            self.__class__.__name__,  # vehicle class name.
            self.brand,  # vehicle brand.
            self.model,  # vehicle model.
            str(self.year),  # vehicle year as a string.
            str(self.price),  # vehicle price as a string.
            self.color,  # vehicle color.
        ]  # create a list of vehicle attributes as strings.
        return ",".join(data)  # join the data list into a comma-separated string.

    @classmethod
    def from_line(cls, line, add_to_inventory=True):
        """Creates a vehicle instance from a line of text."""
        data = line.strip().split(",")  # split the input line into a list of data fields.
        vehicle_type = data[0]  # extract the vehicle type from the data.
        constructor_map = {
            "Car": lambda data: Car(
                data[1],  # brand.
                data[2],  # model.
                int(data[3]),  # year.
                float(data[4]),  # price.
                data[5],  # color.
                data[6],  # fuel_type.
                float(data[7]),  # fuel_level.
                add_to_inventory=add_to_inventory,
            ),
            "ElectricCar": lambda data: ElectricCar(
                data[1],  # brand.
                data[2],  # model.
                int(data[3]),  # year.
                float(data[4]),  # price.
                data[5],  # color.
                float(data[6]),  # battery_level.
                add_to_inventory=add_to_inventory,
            ),
            "Bike": lambda data: Bike(
                data[1],  # brand.
                data[2],  # model.
                int(data[3]),  # year.
                float(data[4]),  # price.
                data[5],  # color.
                data[6],  # bike_type.
                float(data[7]),  # distance_covered.
                float(data[8]),  # fuel_level.
                add_to_inventory=add_to_inventory,
            ),
            "Vehicle": lambda data: cls(
                data[1],  # brand.
                data[2],  # model.
                int(data[3]),  # year.
                float(data[4]),  # price.
                data[5],  # color.
                add_to_inventory=add_to_inventory,
            ),
        }  # map vehicle types to constructor functions.
        constructor = constructor_map.get(
            vehicle_type,
            lambda data: cls(
                data[1],  # brand.
                data[2],  # model.
                int(data[3]),  # year.
                float(data[4]),  # price.
                data[5],  # color.
                add_to_inventory=add_to_inventory,
            ),
        )  # get the appropriate constructor function.
        return constructor(data)  # create and return the vehicle instance.

class Car(Vehicle):
    """Class for regular cars, with fuel-related methods."""

    def __init__(
        self,
        brand,  # car brand.
        model,  # car model.
        year,  # manufacturing year.
        price,  # car price.
        color,  # car color.
        fuel_type,  # type of fuel used.
        fuel_level=100,  # initial fuel level.
        add_to_inventory=True,
    ):
        super().__init__(brand, model, year, price, color, add_to_inventory)  # initialize base Vehicle attributes.
        self.fuel_type = fuel_type  # set the fuel type.
        self.fuel_level = fuel_level  # set the fuel level.

    @log_action
    def refuel(self, amount):
        """Refuels the car up to a maximum of 100 units."""
        self.fuel_level = min(self.fuel_level + amount, 100)  # increase fuel level without exceeding 100.

    @log_action
    def drive(self, distance):
        """Simulates driving, consuming fuel based on the distance driven."""
        fuel_consumed = distance * np.random.uniform(0.08, 0.12)  # calculate fuel consumed based on distance.
        self.fuel_level = max(self.fuel_level - fuel_consumed, 0)  # reduce the fuel level, ensuring it doesn't go below 0.
        print(
            f"Drove {distance} km. Fuel consumed: {fuel_consumed:.2f}. "
            f"Remaining fuel level: {self.fuel_level:.2f}"
        )  # print the driving summary.

    def get_info(self):
        """Returns car information, including fuel type and level."""
        return (
            f"{super().get_info()}, Fuel Type: {self.fuel_type}, "
            f"Fuel Level: {self.fuel_level:.2f}"
        )  # include fuel type and level in the info.

    def to_line(self):
        """Converts the car instance to a line of text."""
        data = [
            self.__class__.__name__,  # class name 'Car'.
            self.brand,  # car brand.
            self.model,  # car model.
            str(self.year),  # year as string.
            str(self.price),  # price as string.
            self.color,  # car color.
            self.fuel_type,  # fuel type.
            str(self.fuel_level),  # fuel level as string.
        ]  # create a list of car attributes as strings.
        return ",".join(data)  # join the data into a comma-separated string.

class ElectricCar(Car):
    """Class for electric cars, with battery-specific methods."""

    def __init__(
        self,
        brand,  # electric car brand.
        model,  # electric car model.
        year,  # manufacturing year.
        price,  # electric car price.
        color,  # electric car color.
        battery_level=100,  # initial battery level.
        add_to_inventory=True,
    ):
        super().__init__(
            brand,
            model,
            year,
            price,
            color,
            fuel_type="ELECTRIC",
            add_to_inventory=add_to_inventory,
        )  # initialize Car with 'ELECTRIC' as fuel type.
        self.battery_level = battery_level  # set the battery level.

    @log_action
    def charge_battery(self, charge):
        """Charges the battery up to a maximum of 100 units."""
        self.battery_level = min(self.battery_level + charge, 100)  # increase battery level without exceeding 100.

    def get_info(self):
        """Returns electric car information, including battery level."""
        return (
            f"{super().get_info()}, Battery Level: {self.battery_level:.2f}"
        )  # include battery level in the info.

    def to_line(self):
        """Converts the electric car instance to a line of text."""
        data = [
            self.__class__.__name__,  # class name 'ElectricCar'.
            self.brand,  # electric car brand.
            self.model,  # electric car model.
            str(self.year),  # year as string.
            str(self.price),  # price as string.
            self.color,  # electric car color.
            str(self.battery_level),  # battery level as string.
        ]  # create a list of electric car attributes as strings.
        return ",".join(data)  # join the data into a comma-separated string.

class Bike(Vehicle):
    """Class for bikes, with methods to manage bike-specific attributes."""

    def __init__(
        self,
        brand,  # bike brand.
        model,  # bike model.
        year,  # manufacturing year.
        price,  # bike price.
        color,  # bike color.
        bike_type,  # type of bike (e.g., Road, Mountain).
        distance_covered=0.0,  # initial distance covered.
        fuel_level=100,  # initial fuel level.
        add_to_inventory=True,
    ):
        super().__init__(brand, model, year, price, color, add_to_inventory)  # initialize base Vehicle attributes.
        self.bike_type = bike_type  # set the bike type.
        self.distance_covered = distance_covered  # set the initial distance covered.
        self.fuel_level = fuel_level  # set the fuel level (bikes can be refueled with petrol).

    @log_action
    def ride(self, time_hours):
        """Simulates riding the bike, calculating the distance covered."""
        distance = time_hours * 15  # assuming constant speed of 15 km/h.
        self.distance_covered += distance  # update the total distance covered.
        print(f"Rode {distance} km in {time_hours} hours.")  # print the riding summary.

    @log_action
    def refuel(self, amount):
        """Refuels the bike up to a maximum of 100 units."""
        self.fuel_level = min(self.fuel_level + amount, 100)  # increase fuel level without exceeding 100.

    def get_info(self):
        """Returns bike information, including type and distance covered."""
        return (
            f"{super().get_info()}, Type: {self.bike_type}, "
            f"Distance Covered: {self.distance_covered:.2f} km, "
            f"Fuel Level: {self.fuel_level:.2f}"
        )  # include bike type, distance covered, and fuel level in the info.

    def to_line(self):
        """Converts the bike instance to a line of text."""
        data = [
            self.__class__.__name__,  # class name 'Bike'.
            self.brand,  # bike brand.
            self.model,  # bike model.
            str(self.year),  # year as string.
            str(self.price),  # price as string.
            self.color,  # bike color.
            self.bike_type,  # type of bike.
            str(self.distance_covered),  # distance covered as string.
            str(self.fuel_level),  # fuel level as string.
        ]  # create a list of bike attributes as strings.
        return ",".join(data)  # join the data into a comma-separated string.