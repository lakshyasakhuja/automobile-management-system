'''
NAME: LAKSHYA SAKHUJA
SID: 540863213
UNIKEY: LSAK0709
USYD CODE CITATION ACKNOWLEDGEMENT
I declare that the given code was written by me and is my own work.
'''

'''
Automobile Management System: This script allows users to manage vehicles, including adding, purchasing, and maintaining cars, electric cars, and bikes. It includes admin functionalities for managing inventory and viewing sales data.
'''

import time  # import time module for time-related functions.
import sys  # import sys module for system-specific parameters and functions.
import hashlib  # import hashlib module for secure hashes and message digests.
import ast  # import ast module for abstract syntax tree manipulation.
import os  # import os module for operating system dependent functionality.
import atexit  # import atexit module to register functions to be executed upon program termination.
import numpy as np  # import numpy library as np for numerical operations.
from tabulate import tabulate  # import tabulate function for table display.
from classes import Vehicle, Car, ElectricCar, Bike, log_action  # import classes and decorator from classes.py.

# admin login details - username: lakshya, password: info1110.
# reset codes - inventory: info1110iloveyou, user data: info1110resetusers.

# company details.
COMPANY_NAME = "LAKSHYA AUTOMOBILES"
ADDRESS = "7, Wattle St, Ultimo NSW 2007"
REGISTRATION_NUMBER = "3197206"

# files to store the data.
INVENTORY_FILE = "vehicle_inventory.txt"  # file to store vehicle inventory.
USER_DATA_FILE = "user_data.txt"  # file to store user data.
USER_VEHICLES_FILE = "user_vehicles.txt"  # file to store user vehicles.
SALES_DATA_FILE = "sales_data.txt"  # file to store sales data.

user_data = {}  # user storage; stores data into an in-memory dictionary.
user_vehicles = {}  # stores the vehicles owned by each user; key: username, value: list of vehicles.
sales_data = []  # stores sales transactions in a list.
LOGGED_IN_USER = None  # to determine which user has logged in.
LOGIN_TIME = None  # to store login times.

def hash_password(password):
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()  # return the hashed password.

def print_welcome_banner():
    """Prints a welcome banner with the company details."""
    current_date = time.strftime("%d %B %Y")  # get current date.
    current_time = time.strftime("%I:%M %p")  # get current time.

    print("\n" + "=" * 50)  # print top border.
    print(f"{COMPANY_NAME.center(50)}")  # print company name centered.
    print(f"Registration No: {REGISTRATION_NUMBER}".center(50))  # print registration number centered.
    print(f"{ADDRESS.center(50)}")  # print address centered.
    print(f"Date: {current_date}  Time: {current_time}".center(50))  # print date and time centered.
    print("=" * 50 + "\n")  # print bottom border.

def create_account():
    """Allows a new user to create an account."""
    while True:
        username = input("Enter a username: ").strip()  # prompt for username.
        if username in user_data:  # check if username already exists.
            print("Username already exists. Please choose a different username.\n")  # inform user.
            continue  # continue to prompt for username.
        break  # exit loop if username is unique.
    password = input("Enter a password: ").strip()  # prompt for password.
    user_data[username] = hash_password(password)  # store hashed password.
    save_user_data()  # save user data to file.
    print("Account created successfully!\n")  # inform user.
    return True  # return success.

def login():
    """Logs a user in by verifying their username and password."""
    global LOGGED_IN_USER, LOGIN_TIME  # declare global variables.
    while True:
        username = input("Enter your username: ").strip()  # prompt for username.
        password = input("Enter your password: ").strip()  # prompt for password.
        if user_data.get(username) == hash_password(password):  # verify credentials.
            LOGGED_IN_USER = username  # set the logged-in user.
            LOGIN_TIME = time.strftime("%Y-%m-%d %H:%M:%S")  # capture login time.
            print(f"Welcome, {username}!")  # greet user.
            user_options()  # direct the user to user options.
            return True  # return success.
        print("Invalid username or password. Please try again.\n")  # inform user.

def admin_login():
    """Logs an admin in with special privileges and displays admin menu."""
    global LOGGED_IN_USER  # declare global variable.
    while True:
        username = input("Enter admin username: ").strip()  # prompt for admin username.
        password = input("Enter admin password: ").strip()  # prompt for admin password.
        if user_data.get(username) == hash_password(password):  # verify credentials.
            LOGGED_IN_USER = username  # set the logged-in user.
            print("Admin logged in successfully!")  # inform admin.
            admin_menu()  # display admin menu.
            return True  # return success.
        print("Invalid admin credentials. Please try again.\n")  # inform user.

def get_valid_year(prompt):
    """Prompts the user to enter a valid year (integer)."""
    attempts = 0  # initialize attempts counter.
    while attempts < 3:
        try:
            year = int(input(prompt))  # prompt for year.
            return year  # return valid year.
        except ValueError:
            attempts += 1  # increment attempts.
            print(
                f"Invalid input. Please enter a valid year. "
                f"Attempts left: {3 - attempts}"
            )  # inform user.
    print("Too many invalid attempts.\n")  # inform user.
    return None  # return None after too many attempts.

def get_valid_price(prompt):
    """Prompts the user to enter a valid price (float)."""
    attempts = 0  # initialize attempts counter.
    while attempts < 3:
        try:
            price = float(input(prompt))  # prompt for price.
            return price  # return valid price.
        except ValueError:
            attempts += 1  # increment attempts.
            print(
                f"Invalid input. Please enter a valid price. "
                f"Attempts left: {3 - attempts}"
            )  # inform user.
    print("Too many invalid attempts.\n")  # inform user.
    return None  # return None after too many attempts.

def add_vehicle():
    """Allows adding a Car, Electric Car, or Bike."""
    print("\nAdding a new vehicle:")  # inform user.

    print("Select Vehicle Type:")  # prompt for vehicle type.
    print("1. Car")  # option 1.
    print("2. Electric Car")  # option 2.
    print("3. Bike")  # option 3.
    vehicle_type = input("Choose an option (1-3): ").strip()  # get user choice.

    brand = input("Enter Brand: ")  # prompt for brand.
    model = input("Enter Model: ")  # prompt for model.
    year = get_valid_year("Enter Year: ")  # prompt for year.
    if year is None:
        return  # return if invalid year.
    price = get_valid_price("Enter Price: ")  # prompt for price.
    if price is None:
        return  # return if invalid price.
    color = input("Enter Color: ")  # prompt for color.

    if vehicle_type == "1":
        while True:
            fuel_type = input("Enter Fuel Type (Petrol/Diesel): ").strip()  # prompt for fuel type.
            if fuel_type.lower() in ['petrol', 'diesel']:
                fuel_type = fuel_type.upper()  # convert to uppercase.
                break  # exit loop.
            print("Invalid fuel type. Please enter 'Petrol' or 'Diesel'.")  # inform user.
        Car(brand, model, year, price, color, fuel_type)  # create Car instance.
        print("Car added successfully!")  # inform user.
    elif vehicle_type == "2":
        ElectricCar(brand, model, year, price, color)  # create ElectricCar instance.
        print("Electric Car added successfully!")  # inform user.
    elif vehicle_type == "3":
        while True:
            bike_type = input("Enter Bike Type (Road/Mountain): ").strip()  # prompt for bike type.
            if bike_type.lower() in ['road', 'mountain']:
                bike_type = bike_type.upper()  # convert to uppercase.
                break  # exit loop.
            print("Invalid bike type. Please enter 'Road' or 'Mountain'.")  # inform user.
        Bike(brand, model, year, price, color, bike_type)  # create Bike instance.
        print("Bike added successfully!")  # inform user.
    else:
        print("Invalid option selected. Returning to menu.")  # inform user.

def admin_menu():
    """Displays admin-specific options after admin login."""
    admin_options = {
        "1": clearance_sale,
        "2": apply_custom_discount,
        "3": Vehicle.display_inventory,
        "4": update_inventory,
        "5": reset_inventory,
        "6": reset_user_data,
        "7": view_sales,
        "8": logout_admin,
    }  # define admin options.

    while True:
        print("\nAdmin Options:")  # display admin options.
        for key, value in admin_options.items():
            option_text = {
                "1": "Start Clearance Sale (40% Discount)",
                "2": "Apply Custom Discount",
                "3": "Display Inventory",
                "4": "Update Inventory",
                "5": "Reset Inventory",
                "6": "Reset User Data",
                "7": "View Sales Data",
                "8": "Logout",
            }.get(key, "Unknown Option")  # get option text.
            print(f"{key}. {option_text}")  # print option.

        choice = input("Select an option (1-8): ")  # get admin choice.
        action = admin_options.get(
            choice, lambda: print("Invalid choice. Please select again.")
        )  # get corresponding action.
        if choice == "8":
            action()  # logout action.
            break  # exit loop.
        action()  # execute action.

def logout_admin():
    """Logs out the admin and saves data."""
    print("Logging out...\n")  # inform admin.
    save_all_data()  # save all data.

def logout_user():
    """Logs out the user and saves data."""
    print("Logging out...\n")  # inform user.
    save_all_data()  # save all data.

def save_all_data():
    """Saves all data."""
    save_inventory()  # save inventory data.
    save_user_data()  # save user data.
    save_user_vehicles()  # save user vehicles.
    save_sales_data()  # save sales data.

def view_sales():
    """Displays the sales data to the admin."""
    if not sales_data:  # check if sales data is empty.
        print("No sales data available.")  # inform admin.
        return  # exit function.

    total_amount = 0.0  # initialize total amount.
    print("\nSales Transactions:")  # display header.
    for transaction in sales_data:
        print("\n" + "-" * 50)  # print separator.
        print(f"Transaction Type: {transaction['transaction_type']}")  # print transaction type.
        print(f"Date and Time: {transaction['date_time']}")  # print date and time.
        print(f"User: {transaction['user']}")  # print user.
        details = transaction['details']  # get transaction details.
        if transaction['transaction_type'] == 'Purchase':
            print(
                f"Vehicle: {details['brand']} {details['model']}, "
                f"Year: {details['year']}, Color: {details['color']}"
            )  # print vehicle details.
            print(f"Vehicle Price: ${details['price']:.2f}")  # print vehicle price.
            print(f"Insurance: {details['insurance']}")  # print insurance.
            print(f"Insurance Cost: ${details['insurance_cost']:.2f}")  # print insurance cost.
            print(f"Total Price: ${details['total_price']:.2f}")  # print total price.
            total_amount += details['total_price']  # add to total amount.
        elif transaction['transaction_type'] == 'Refuel':
            print(
                f"Vehicle: {details['brand']} {details['model']}, "
                f"Year: {details['year']}"
            )  # print vehicle details.
            print(f"Fuel Type: {details['fuel_type']}")  # print fuel type.
            print(f"Amount Fueled: {details['amount_fueled']:.2f} units")  # print amount fueled.
            print(f"Total Cost: ${details['total_cost']:.2f}")  # print total cost.
            total_amount += details['total_cost']  # add to total amount.
        elif transaction['transaction_type'] == 'Charge':
            print(
                f"Vehicle: {details['brand']} {details['model']}, "
                f"Year: {details['year']}"
            )  # print vehicle details.
            print(f"Amount Charged: {details['amount_charged']:.2f} units")  # print amount charged.
            print(f"Total Cost: ${details['total_cost']:.2f}")  # print total cost.
            total_amount += details['total_cost']  # add to total amount.
        else:
            print("Unknown transaction type.")  # inform admin.
    print("\n" + "=" * 50)  # print separator.
    print(f"Total Amount from All Transactions: ${total_amount:.2f}")  # print total amount.
    print("=" * 50)  # print separator.

def reset_inventory():
    """Resets the inventory after verifying a special code."""
    code = input("Enter the special reset code: ").strip()  # prompt for reset code.
    confirm = (
        input(
            "Are you sure you want to reset the inventory? "
            "This action cannot be undone. (yes/no): "
        ).strip().lower()
        if code == "info1110iloveyou"
        else None
    )  # prompt for confirmation.
    if code == "info1110iloveyou" and confirm == "yes":
        Vehicle.all_vehicles.clear()  # clear all vehicles.
        save_inventory()  # save inventory.
        print("Inventory has been reset.")  # inform admin.
    elif confirm == "no":
        print("Inventory reset canceled.")  # inform admin.
    else:
        print("Invalid reset code. Inventory not reset.")  # inform admin.

def reset_user_data():
    """Resets the user data after verifying a special code."""
    code = input("Enter the special user reset code: ").strip()  # prompt for reset code.
    confirm = (
        input(
            "Are you sure you want to reset all user data? "
            "This action cannot be undone. (yes/no): "
        ).strip().lower()
        if code == "info1110resetusers"
        else None
    )  # prompt for confirmation.
    if code == "info1110resetusers" and confirm == "yes":
        user_data.clear()  # clear user data.
        user_data["lakshya"] = hash_password("info1110")  # add default admin user.
        save_user_data()  # save user data.
        print("User data has been reset to default admin account.")  # inform admin.
    elif confirm == "no":
        print("User data reset canceled.")  # inform admin.
    else:
        print("Invalid reset code. User data not reset.")  # inform admin.

def clearance_sale():
    """Applies a 40% discount to a random selection of vehicles."""
    if not Vehicle.all_vehicles:  # check if inventory is empty.
        print("No vehicles available for clearance sale.")  # inform admin.
        return  # exit function.

    num_vehicles = len(Vehicle.all_vehicles) // 2 or 1  # calculate number of vehicles.
    sale_vehicles = np.random.choice(
        Vehicle.all_vehicles, size=num_vehicles, replace=False
    )  # select random vehicles.
    list(map(lambda vehicle: vehicle.apply_discount(40), sale_vehicles))  # apply discount.
    for vehicle in sale_vehicles:
        print(f"Applied 40% discount to {vehicle.get_info()}")  # inform admin.

def apply_custom_discount():
    """Allows admin to apply a custom discount to vehicles."""
    print("\nCustom Discount Options:")  # display header.
    Vehicle.display_inventory()  # display inventory.

    try:
        discount_percent = float(input("Enter discount percentage: "))  # prompt for discount.
    except ValueError:
        print("Invalid discount percentage. Returning to admin menu.")  # inform admin.
        return  # exit function.

    subset_choice = input(
        "Apply discount to all vehicles (A) or a random subset (R)? "
    ).strip().upper()  # prompt for choice.

    discount_actions = {
        "A": lambda: (
            list(
                map(
                    lambda vehicle: vehicle.apply_discount(discount_percent),
                    Vehicle.all_vehicles,
                )
            ),
            print(f"Applied {discount_percent}% discount to all vehicles."),
        ),
        "R": lambda: apply_discount_to_subset(discount_percent),
    }  # define actions.

    discount_action = discount_actions.get(
        subset_choice, lambda: print("Invalid choice. Returning to admin menu.")
    )  # get action.
    discount_action()  # execute action.

def apply_discount_to_subset(discount_percent):
    """Applies discount to a subset of vehicles."""
    try:
        num_vehicles = int(
            input("Enter the number of vehicles to apply the discount to: ")
        )  # prompt for number.
        if num_vehicles > len(Vehicle.all_vehicles) or num_vehicles < 1:
            print("Invalid number. Returning to admin menu.")  # inform admin.
            return  # exit function.
    except ValueError:
        print("Invalid input. Returning to admin menu.")  # inform admin.
        return  # exit function.

    selected_vehicles = np.random.choice(
        Vehicle.all_vehicles, size=num_vehicles, replace=False
    )  # select random vehicles.
    list(
        map(
            lambda vehicle: vehicle.apply_discount(discount_percent),
            selected_vehicles,
        )
    )  # apply discount.
    for vehicle in selected_vehicles:
        print(f"Applied {discount_percent}% discount to {vehicle.get_info()}")  # inform admin.
    print(
        f"Applied {discount_percent}% discount to {num_vehicles} "
        "randomly selected vehicles."
    )  # inform admin.

def update_inventory():
    """Allows admin to add or remove vehicles from the inventory."""
    update_actions = {
        "1": add_vehicle,
        "2": remove_vehicle,
        "3": lambda: None,
    }  # define actions.

    while True:
        print("\nUpdate Inventory Options:")
        print("1. Add a Vehicle")
        print("2. Remove a Vehicle")
        print("3. Return to Admin Menu")

        choice = input("Select an option (1-3): ")  # get admin choice.
        action = update_actions.get(
            choice, lambda: print("Invalid choice. Please select again.")
        )  # get action.
        if choice == "3":
            break  # exit loop.
        action()  # execute action.

def remove_vehicle():
    """Allows the admin to remove vehicles based on indices."""
    print("\nRemoving vehicles:")  # inform admin.
    Vehicle.display_inventory()  # display inventory.
    indices_input = input(
        "Enter the indices of the vehicles to remove (comma-separated): "
    ).split(",")  # get indices.
    indices = sorted(
        (int(i.strip()) - 1 for i in indices_input if i.strip().isdigit()),
        reverse=True,
    )  # process indices.

    removed_vehicles = []
    for index in indices:
        if 0 <= index < len(Vehicle.all_vehicles):
            removed_vehicles.append(Vehicle.all_vehicles.pop(index))  # remove vehicle.
        else:
            print(f"Invalid index {index + 1}. Skipping...")  # inform admin.

    if removed_vehicles:
        print("\nRemoved vehicles:")  # display removed vehicles.
        for vehicle in removed_vehicles:
            print(vehicle.get_info())  # print vehicle info.
    else:
        print("No vehicles were removed.")  # inform admin.

def save_inventory():
    """Saves the current inventory to a text file."""
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        lines = (vehicle.to_line() + '\n' for vehicle in Vehicle.all_vehicles)  # prepare lines.
        f.writelines(lines)  # write to file.
    print("Inventory saved successfully.")  # inform user.

def load_inventory():
    """Loads the inventory from a text file."""
    if os.path.exists(INVENTORY_FILE):  # check if file exists.
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            lines = (line.strip() for line in f if line.strip())  # read lines.
            Vehicle.all_vehicles.clear()  # clear current inventory.
            for line in lines:
                vehicle = Vehicle.from_line(line, add_to_inventory=True)  # create vehicle.
        print("Inventory loaded successfully.")  # inform user.
    else:
        print("No existing inventory found. Starting with an empty inventory.")  # inform user.

def save_user_data():
    """Saves the user data to a text file."""
    with open(USER_DATA_FILE, 'w', encoding='utf-8') as f:
        lines = (
            f"{username},{hashed_password}\n"
            for username, hashed_password in user_data.items()
        )  # prepare lines.
        f.writelines(lines)  # write to file.
    print("User data saved successfully.")  # inform user.

def load_user_data():
    """Loads the user data from a text file."""
    if os.path.exists(USER_DATA_FILE):  # check if file exists.
        with open(USER_DATA_FILE, 'r', encoding='utf-8') as f:
            lines = (line.strip() for line in f if line.strip())  # read lines.
            user_data.clear()  # clear current data.
            for line in lines:
                username, hashed_password = line.strip().split(',', 1)  # split line.
                user_data[username] = hashed_password  # store data.
        print("User data loaded successfully.")  # inform user.
    else:
        user_data["lakshya"] = hash_password("info1110")  # create default admin user.
        print("No existing user data found. Created default admin user.")  # inform user.

def save_user_vehicles():
    """Saves the user vehicles to a text file."""
    with open(USER_VEHICLES_FILE, 'w', encoding='utf-8') as f:
        for username, vehicles in user_vehicles.items():
            for vehicle in vehicles:
                line = f"{username},{vehicle.to_line()}\n"  # prepare line.
                f.write(line)  # write to file.
    print("User vehicles saved successfully.")  # inform user.

def load_user_vehicles():
    """Loads the user vehicles from a text file."""
    user_vehicles.clear()  # clear existing data.
    if os.path.exists(USER_VEHICLES_FILE):  # check if file exists.
        with open(USER_VEHICLES_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()  # strip whitespace.
                if not line:
                    continue  # skip empty lines.
                username, vehicle_data = line.split(',', 1)  # split line.
                vehicle = Vehicle.from_line(
                    vehicle_data, add_to_inventory=False
                )  # create vehicle.
                user_vehicles.setdefault(username, []).append(vehicle)  # store vehicle.
        print("User vehicles loaded successfully.")  # inform user.
    else:
        print("No existing user vehicles found.")  # inform user.

def save_sales_data():
    """Saves the sales data to a text file."""
    with open(SALES_DATA_FILE, 'w', encoding='utf-8') as f:
        for transaction in sales_data:
            f.write(f"{repr(transaction)}\n")  # write transaction.
    print("Sales data saved successfully.")  # inform user.

def load_sales_data():
    """Loads the sales data from a text file."""
    sales_data.clear()  # clear existing data.
    if os.path.exists(SALES_DATA_FILE):  # check if file exists.
        with open(SALES_DATA_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    transaction = ast.literal_eval(line.strip())  # parse transaction.
                    if isinstance(transaction, dict):
                        sales_data.append(transaction)  # store transaction.
                    else:
                        print("Invalid transaction data encountered and skipped.")  # inform user.
                except (SyntaxError, ValueError):
                    print("Failed to parse transaction data. Line skipped.")  # inform user.
        print("Sales data loaded successfully.")  # inform user.
    else:
        print("No existing sales data found.")  # inform user.

def main_menu():
    """Main menu for interacting with the vehicle management system."""
    load_inventory()  # load inventory at startup.
    load_user_data()  # load user data at startup.
    load_user_vehicles()  # load user vehicles at startup.
    load_sales_data()  # load sales data at startup.

    atexit.register(save_inventory)  # register save functions.
    atexit.register(save_user_data)
    atexit.register(save_user_vehicles)
    atexit.register(save_sales_data)

    while True:
        print_welcome_banner()  # display welcome banner.
        main_actions = {
            "1": lambda: login(),
            "2": create_account,
            "3": lambda: admin_login(),
            "4": lambda: (print("Exiting the program.\n"), sys.exit()),
        }  # define main actions.

        print("1. Login")  # option 1.
        print("2. Create Account")  # option 2.
        print("3. Admin Login")  # option 3.
        print("4. Exit")  # option 4.

        choice = input("Select an option (1-4): ")  # get user choice.
        action = main_actions.get(
            choice, lambda: print("Invalid choice. Please try again.\n")
        )  # get action.
        action()  # execute action.

def user_options():
    """Displays options available to the user after login."""
    user_actions = {
        "1": add_vehicle,
        "2": Vehicle.display_inventory,
        "3": buy_vehicle,
        "4": manage_vehicle,
        "5": logout_user,
    }  # define user actions.

    while True:
        print("\nOptions:")  # display options.
        print("1. Add a Vehicle")  # option 1.
        print("2. List All Vehicles")  # option 2.
        print("3. Buy a Vehicle")  # option 3.
        print("4. Manage My Vehicles")  # option 4.
        print("5. Logout")  # option 5.

        choice = get_choice()  # get user choice.
        action = user_actions.get(
            choice, lambda: print("Invalid choice. Please select again.")
        )  # get action.
        if choice == "5":
            action()  # logout action.
            break  # exit loop.
        action()  # execute action.

def get_choice():
    """Prompts the user for a valid menu choice."""
    while True:
        choice = input("Choose an option: ")  # prompt for choice.
        if choice.isdigit() and 1 <= int(choice) <= 5:
            return choice  # return valid choice.
        print("Invalid choice. Please select again.")  # inform user.

@log_action
def buy_vehicle():
    """Allows the user to purchase a vehicle."""
    if not Vehicle.all_vehicles:
        print("No vehicles available for purchase.")  # inform user.
        return  # exit function.

    print("\nAvailable Vehicles:")  # display header.
    Vehicle.display_inventory()  # display inventory.

    try:
        index = int(
            input("Enter the index of the vehicle you wish to purchase: ")
        ) - 1  # get vehicle index.
        if index < 0 or index >= len(Vehicle.all_vehicles):
            print("Invalid index selected.")  # inform user.
            return  # exit function.
    except ValueError:
        print("Invalid input. Please enter a valid index.")  # inform user.
        return  # exit function.

    vehicle = Vehicle.all_vehicles[index]  # get selected vehicle.
    vehicle_price = vehicle.price  # get vehicle price.
    total_price = vehicle_price  # initialize total price.

    print(f"\nYou have selected:\n{vehicle.get_info()}")  # display vehicle info.

    insurance_options = [
        "1. Comprehensive Insurance",
        "2. Third-Party Insurance",
        "3. Collision Insurance",
        "4. No Insurance",
    ]  # define insurance options.
    print("\nWould you like to add insurance to your purchase?")  # prompt user.
    print("Each insurance option costs 10% of the vehicle's price.")  # inform user.
    for option in insurance_options:
        print(option)  # display options.

    insurance_choice = input("Select an insurance option (1-4): ").strip()  # get choice.
    if insurance_choice in ["1", "2", "3"]:
        insurance_cost = vehicle_price * 0.10  # calculate insurance cost.
    else:
        insurance_cost = 0.0  # no insurance.

    total_price += insurance_cost  # update total price.
    selected_insurance = (
        insurance_options[int(insurance_choice) - 1][3:].strip()
        if insurance_choice in ["1", "2", "3"]
        else "No Insurance"
    )  # get insurance name.
    if insurance_choice in ["1", "2", "3"]:
        print(
            f"Added {selected_insurance} to your purchase for "
            f"${insurance_cost:.2f}"
        )  # inform user.
    elif insurance_choice == "4":
        print("No insurance selected.")  # inform user.
    else:
        print("Invalid choice. No insurance will be added.")  # inform user.

    print(f"\nTotal price: ${total_price:.2f}")  # display total price.

    if process_payment(total_price):
        purchased_vehicle = Vehicle.all_vehicles.pop(index)  # remove vehicle from inventory.
        user_vehicles.setdefault(LOGGED_IN_USER, []).append(purchased_vehicle)  # assign to user.
        save_inventory()  # save inventory.
        print("\nTransaction successful! Printing receipt...")  # inform user.
        purchase_time = time.strftime("%Y-%m-%d %H:%M:%S")  # get purchase time.
        print_receipt(
            purchased_vehicle,
            selected_insurance,
            vehicle_price,
            insurance_cost,
            total_price,
            purchase_time,
        )  # print receipt.
        transaction = {
            'transaction_type': 'Purchase',
            'date_time': purchase_time,
            'user': LOGGED_IN_USER,
            'details': {
                'vehicle_type': vehicle.__class__.__name__,
                'brand': vehicle.brand,
                'model': vehicle.model,
                'year': vehicle.year,
                'color': vehicle.color,
                'price': vehicle_price,
                'insurance': selected_insurance,
                'insurance_cost': insurance_cost,
                'total_price': total_price,
            },
        }  # record transaction.
        sales_data.append(transaction)  # add to sales data.
        save_sales_data()  # save sales data.
    else:
        print("Transaction cancelled.")  # inform user.

def process_payment(amount_due):
    """Processes the payment for the given amount."""
    print("\nPlease enter your payment details:")  # prompt user.
    input("Name on Card: ").strip()  # get name.
    card_number = input("Card Number (16 digits): ").strip()  # get card number.
    cvv = input("CVV (3 digits): ").strip()  # get CVV.

    if not (len(card_number) == 16 and card_number.isdigit()):
        print("Invalid card number.")  # inform user.
        return False  # return failure.
    if not (len(cvv) == 3 and cvv.isdigit()):
        print("Invalid CVV.")  # inform user.
        return False  # return failure.

    confirm = input(
        f"Confirm payment of ${amount_due:.2f}? (yes/no): "
    ).strip().lower()  # prompt for confirmation.
    if confirm == "yes":
        return True  # return success.
    return False  # return failure.

def print_receipt(
    vehicle,
    insurance,
    vehicle_price,
    insurance_cost,
    total_price,
    purchase_time,
):
    """Prints the receipt for the purchase."""
    print("\n" + "=" * 49)  # print separator.
    print(f"{COMPANY_NAME.center(49)}")  # print company name.
    print("=" * 49)  # print separator.
    print(f"{'RECEIPT OF PURCHASE'.center(49)}")  # print header.
    print("=" * 49)  # print separator.

    print(f"\nLogin Time: {LOGIN_TIME}")  # print login time.
    print(f"Date and Time of the Purchase: {purchase_time}")  # print purchase time.
    print(f"Purchased by: {LOGGED_IN_USER}")  # print purchaser.
    print(f"Vehicle Type: {vehicle.__class__.__name__}")  # print vehicle type.

    vehicle_detail_funcs = {
        Car: lambda v: (
            f"{v.brand} {v.model}, Year: {v.year}, Color: {v.color}, "
            f"Fuel Type: {v.fuel_type}, Fuel Level: {v.fuel_level:.2f}"
        ),
        ElectricCar: lambda v: (
            f"{v.brand} {v.model}, Year: {v.year}, Color: {v.color}, "
            f"Battery Level: {v.battery_level:.2f}"
        ),
        Bike: lambda v: (
            f"{v.brand} {v.model}, Year: {v.year}, Color: {v.color}, "
            f"Type: {v.bike_type}, Distance Covered: {v.distance_covered:.2f} km"
        ),
    }  # define vehicle detail functions.

    vehicle_details = vehicle_detail_funcs.get(
        type(vehicle), lambda v: v.get_info()
    )(vehicle)  # get vehicle details.

    print(f"Vehicle Details: {vehicle_details}")  # print vehicle details.
    print(f"Insurance Selected: {insurance}")  # print insurance.
    print(f"Price of the Vehicle: ${vehicle_price:.2f}")  # print vehicle price.
    print(f"Price of the Insurance: ${insurance_cost:.2f}")  # print insurance cost.
    print(f"Total Amount Paid: ${total_price:.2f}")  # print total amount.
    print("=" * 49)  # print separator.
    print(f"{'THANK YOU FOR YOUR PURCHASE!'.center(49)}")  # print thank you.
    print("=" * 49 + "\n")  # print separator.

def manage_vehicle():
    """Allows the user to manage their purchased vehicles."""
    user_owned_vehicles = user_vehicles.get(LOGGED_IN_USER, [])  # get the list of vehicles owned by the logged-in user.
    if not user_owned_vehicles:
        print("You do not own any vehicles.")  # inform the user if they don't own any vehicles.
        return  # exit the function.

    print("\nYour Vehicles:")  # display header.
    for idx, vehicle in enumerate(user_owned_vehicles, 1):
        print(f"{idx}. {vehicle.get_info()}")  # list the user's vehicles.

    # Select a vehicle to manage
    try:
        choice = int(
            input(
                "Enter the number of the vehicle you wish to manage "
                "(or 0 to return): "
            )
        )  # prompt the user to select a vehicle.
        if choice == 0:
            return  # return to the previous menu.
        vehicle = user_owned_vehicles[choice - 1]  # get the selected vehicle.
        if isinstance(vehicle, ElectricCar):
            manage_electric_car(vehicle)  # manage electric car.
        elif isinstance(vehicle, Car):
            manage_car(vehicle)  # manage car.
        elif isinstance(vehicle, Bike):
            manage_bike(vehicle)  # manage bike.
        else:
            print("Unknown vehicle type.")  # inform the user if the vehicle type is unknown.
    except (ValueError, IndexError):
        print("Invalid selection.")  # inform the user of an invalid selection.


def manage_car(car):
    """Allows the user to manage their car."""
    while True:
        print("\nCar Management Options:")  # display options.
        print("1. Drive the Car")  # option 1.
        print("2. Refuel the Car")  # option 2.
        print("3. View Car Info")  # option 3.
        print("4. Return")  # option 4.
        choice = input("Choose an option: ")  # prompt for choice.
        if choice == "1":
            try:
                distance = float(input("Enter distance to drive (km): "))  # prompt for distance.
                car.drive(distance)  # drive the car.
            except ValueError:
                print("Invalid input.")  # inform user.
        elif choice == "2":
            try:
                current_fuel = car.fuel_level  # get current fuel level.
                max_additional_fuel = 100 - current_fuel  # calculate maximum additional fuel.
                print(
                    f"Current fuel level: {current_fuel:.2f}. You can add up to "
                    f"{max_additional_fuel:.2f} units."
                )  # inform user.
                amount = float(input("Enter amount of fuel to add: "))  # prompt for amount.
                if amount <= 0 or amount > max_additional_fuel:
                    print(
                        f"Invalid amount. You can add up to "
                        f"{max_additional_fuel:.2f} units."
                    )  # inform user of invalid amount.
                    continue  # continue to next iteration.
                # Calculate cost
                if car.fuel_type == "PETROL":
                    cost_per_unit = 4.50  # set cost per unit for petrol.
                elif car.fuel_type == "DIESEL":
                    cost_per_unit = 3.75  # set cost per unit for diesel.
                else:
                    print("Unknown fuel type.")  # inform user.
                    continue  # continue to next iteration.
                total_cost = amount * cost_per_unit  # calculate total cost.
                print(f"Total cost for refueling: ${total_cost:.2f}")  # display total cost.
                # Process payment
                if process_payment(total_cost):
                    car.refuel(amount)  # refuel the car.
                    save_user_vehicles()  # save user vehicles.
                    print("Refueling successful! Printing receipt...")  # inform user.
                    print_refuel_receipt(car, amount, total_cost)  # print receipt.
                    # Record the refueling transaction
                    transaction = {
                        'transaction_type': 'Refuel',
                        'date_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': LOGGED_IN_USER,
                        'details': {
                            'vehicle_type': car.__class__.__name__,
                            'brand': car.brand,
                            'model': car.model,
                            'year': car.year,
                            'fuel_type': car.fuel_type,
                            'amount_fueled': amount,
                            'total_cost': total_cost,
                        },
                    }  # create transaction record.
                    sales_data.append(transaction)  # add transaction to sales data.
                    save_sales_data()  # save sales data.
                else:
                    print("Payment cancelled.")  # inform user.
            except ValueError:
                print("Invalid input.")  # inform user.
        elif choice == "3":
            print(car.get_info())  # display car info.
        elif choice == "4":
            break  # exit loop.
        else:
            print("Invalid choice.")  # inform user.


def manage_electric_car(electric_car):
    """Allows the user to manage their electric car."""
    while True:
        print("\nElectric Car Management Options:")  # display options.
        print("1. Drive the Electric Car")  # option 1.
        print("2. Charge the Battery")  # option 2.
        print("3. View Car Info")  # option 3.
        print("4. Return")  # option 4.
        choice = input("Choose an option: ")  # prompt for choice.
        if choice == "1":
            try:
                distance = float(input("Enter distance to drive (km): "))  # prompt for distance.
                electric_car.drive(distance)  # drive the electric car.
            except ValueError:
                print("Invalid input.")  # inform user.
        elif choice == "2":
            try:
                current_battery = electric_car.battery_level  # get current battery level.
                max_additional_charge = 100 - current_battery  # calculate maximum additional charge.
                print(
                    f"Current battery level: {current_battery:.2f}. You can add up to "
                    f"{max_additional_charge:.2f} units."
                )  # inform user.
                amount = float(input("Enter amount to charge (up to 100): "))  # prompt for amount.
                if amount <= 0 or amount > max_additional_charge:
                    print(
                        f"Invalid amount. You can add up to "
                        f"{max_additional_charge:.2f} units."
                    )  # inform user of invalid amount.
                    continue  # continue to next iteration.
                # Calculate cost
                cost_per_unit = 2.50  # set cost per unit for charging.
                total_cost = amount * cost_per_unit  # calculate total cost.
                print(f"Total cost for charging: ${total_cost:.2f}")  # display total cost.
                # Process payment
                if process_payment(total_cost):
                    electric_car.charge_battery(amount)  # charge the battery.
                    save_user_vehicles()  # save user vehicles.
                    print("Charging successful! Printing receipt...")  # inform user.
                    print_charge_receipt(electric_car, amount, total_cost)  # print receipt.
                    # Record the charging transaction
                    transaction = {
                        'transaction_type': 'Charge',
                        'date_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': LOGGED_IN_USER,
                        'details': {
                            'vehicle_type': electric_car.__class__.__name__,
                            'brand': electric_car.brand,
                            'model': electric_car.model,
                            'year': electric_car.year,
                            'amount_charged': amount,
                            'total_cost': total_cost,
                        },
                    }  # create transaction record.
                    sales_data.append(transaction)  # add transaction to sales data.
                    save_sales_data()  # save sales data.
                else:
                    print("Payment cancelled.")  # inform user.
            except ValueError:
                print("Invalid input.")  # inform user.
        elif choice == "3":
            print(electric_car.get_info())  # display car info.
        elif choice == "4":
            break  # exit loop.
        else:
            print("Invalid choice.")  # inform user.


def manage_bike(bike):
    """Allows the user to manage their bike."""
    while True:
        print("\nBike Management Options:")  # display options.
        print("1. Ride the Bike")  # option 1.
        print("2. Refuel the Bike")  # option 2.
        print("3. View Bike Info")  # option 3.
        print("4. Return")  # option 4.
        choice = input("Choose an option: ")  # prompt for choice.
        if choice == "1":
            try:
                time_hours = float(input("Enter time to ride (hours): "))  # prompt for time.
                bike.ride(time_hours)  # ride the bike.
            except ValueError:
                print("Invalid input.")  # inform user.
        elif choice == "2":
            try:
                current_fuel = bike.fuel_level  # get current fuel level.
                max_additional_fuel = 100 - current_fuel  # calculate maximum additional fuel.
                print(
                    f"Current fuel level: {current_fuel:.2f}. You can add up to "
                    f"{max_additional_fuel:.2f} units."
                )  # inform user.
                amount = float(input("Enter amount of fuel to add: "))  # prompt for amount.
                if amount <= 0 or amount > max_additional_fuel:
                    print(
                        f"Invalid amount. You can add up to "
                        f"{max_additional_fuel:.2f} units."
                    )  # inform user of invalid amount.
                    continue  # continue to next iteration.
                # Bikes can only be refueled with petrol
                cost_per_unit = 4.50  # set cost per unit for petrol.
                total_cost = amount * cost_per_unit  # calculate total cost.
                print(f"Total cost for refueling: ${total_cost:.2f}")  # display total cost.
                # process payment.
                if process_payment(total_cost):
                    bike.refuel(amount)  # refuel the bike.
                    save_user_vehicles()  # save user vehicles.
                    print("Refueling successful! Printing receipt...")  # inform user.
                    print_refuel_receipt(bike, amount, total_cost)  # print receipt.
                    # record the refueling transaction.
                    transaction = {
                        'transaction_type': 'Refuel',
                        'date_time': time.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': LOGGED_IN_USER,
                        'details': {
                            'vehicle_type': bike.__class__.__name__,
                            'brand': bike.brand,
                            'model': bike.model,
                            'year': bike.year,
                            'fuel_type': 'PETROL',
                            'amount_fueled': amount,
                            'total_cost': total_cost,
                        },
                    }  # create transaction record.
                    sales_data.append(transaction)  # add transaction to sales data.
                    save_sales_data()  # save sales data.
                else:
                    print("Payment cancelled.")  # inform user.
            except ValueError:
                print("Invalid input.")  # inform user.
        elif choice == "3":
            print(bike.get_info())  # display bike info.
        elif choice == "4":
            break  # exit loop.
        else:
            print("Invalid choice.")  # inform user.


def print_refuel_receipt(vehicle, amount, total_cost):
    """Prints the receipt for refueling."""
    print("\n" + "=" * 49)  # print separator.
    print(f"{COMPANY_NAME.center(49)}")  # print company name.
    print("=" * 49)  # print separator.
    print(f"{'REFUEL RECEIPT'.center(49)}")  # print header.
    print("=" * 49)  # print separator.

    print(f"\nDate and Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")  # print date and time.
    print(f"Customer: {LOGGED_IN_USER}")  # print customer name.
    print(f"Vehicle: {vehicle.brand} {vehicle.model}, Year: {vehicle.year}")  # print vehicle details.

    if isinstance(vehicle, Bike):
        fuel_type = "PETROL"  # set fuel type for bike.
    else:
        fuel_type = vehicle.fuel_type  # get fuel type from vehicle.

    print(f"Fuel Type: {fuel_type}")  # print fuel type.
    print(f"Amount of Fuel Added: {amount:.2f} units")  # print amount added.
    print(f"Total Amount Paid: ${total_cost:.2f}")  # print total cost.
    print("=" * 49)  # print separator.
    print(f"{'THANK YOU!'.center(49)}")  # print thank you message.
    print("=" * 49 + "\n")  # print separator.


def print_charge_receipt(electric_car, amount, total_cost):
    """Prints the receipt for charging the battery."""
    print("\n" + "=" * 49)  # print separator.
    print(f"{COMPANY_NAME.center(49)}")  # print company name.
    print("=" * 49)  # print separator.
    print(f"{'CHARGING RECEIPT'.center(49)}")  # print header.
    print("=" * 49)  # print separator.
    print(f"\nDate and Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")  # print date and time.
    print(f"Customer: {LOGGED_IN_USER}")  # print customer name.
    print(
        f"Vehicle: {electric_car.brand} {electric_car.model}, Year: {electric_car.year}"
    )  # print vehicle details.
    print(f"Amount Charged: {amount:.2f} units")  # print amount charged.
    print(f"Total Amount Paid: ${total_cost:.2f}")  # print total cost.
    print("=" * 49)  # print separator.
    print(f"{'THANK YOU!'.center(49)}")  # print thank you message.
    print("=" * 49 + "\n")  # print separator.


if __name__ == "__main__":
    main_menu()  # start the main menu.