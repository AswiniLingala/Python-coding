import json
from datetime import datetime
import os

class User:
    def __init__(self, username, password, balance=0):
        self.username = username
        self.password = password
        self.balance = balance
        self.transactions = []
        self.profile = {
            'name': '',
            'email': '',
            'phone': ''
        }
    def to_dict(self):
        return {
            "password": self.password,
            "balance": self.balance,
            "transactions": self.transactions,
            "profile": self.profile
        }

    @staticmethod
    def from_dict(username, data):
        user = User(username, data["password"], data["balance"])
        user.transactions = data["transactions"]
        user.profile = data["profile"]
        return user

class WalletApp:
    USER_DATA_FILE = "wallet_data.json"

    def __init__(self):
        self.users = self.load_users()
        self.current_user = None

    def load_users(self):
        if os.path.exists(self.USER_DATA_FILE):
            with open(self.USER_DATA_FILE, "r") as file:
                data = json.load(file)
                return {username: User.from_dict(username, user_data) for username, user_data in data.items()}
        return {}

    def save_users(self):
        with open(self.USER_DATA_FILE, "w") as file:
            json.dump({username: user.to_dict() for username, user in self.users.items()}, file, indent=4)

    def register(self, username, password, initial_balance=0):
        if username in self.users:
            print("User already exists! Try with a new username.")
            return
        new_user = User(username, password, initial_balance)
        # Record the initial balance in the transaction history
        if initial_balance >= 0:
            new_user.transactions.append({
                "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": "Initial Deposit",
                "amount": initial_balance,
                "balance": initial_balance
            })
        self.users[username] = new_user
        self.save_users()
        print("User Registered Successfully!")
    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            print("Login Successful!")
            return True
        else:
            print("Login failed, try again.")
            return False

    def check_balance(self):
        if self.current_user:
            print(f"Current Balance: ₹{self.current_user.balance}")
        else:
            print("No user logged in!")

    def deposit_money(self, amount):
        if self.current_user and amount > 0:
            self.current_user.balance += amount
            self.current_user.transactions.append({
                "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": "Deposit",
                "amount": amount,
                "balance": self.current_user.balance
            })
            self.save_users()
            print(f"Balance Updated! New Balance: ₹{self.current_user.balance}")
        else:
            print("Invalid operation!")

    def withdraw_money(self, amount):
        if self.current_user and 0 < amount <= self.current_user.balance:
            self.current_user.balance -= amount
            self.current_user.transactions.append({
                "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": "Withdraw",
                "amount": -amount,
                "balance": self.current_user.balance
            })
            self.save_users()
            print(f"Transaction Successful! New Balance: ₹{self.current_user.balance}")
        else:
            print("Error: Insufficient Balance or Invalid Amount!")

    def apply_coupon(self, coupon_code):
        coupons = {
            "SAVE10": 0.10,
            "BONUS20": 0.20,
            "DISCOUNT15": 0.15,
            "SUMMER25": 0.25,
            "NEWYEAR30": 0.30,
        }
        if self.current_user and coupon_code in coupons:
            bonus = self.current_user.balance * coupons[coupon_code]
            self.current_user.balance += bonus
            self.current_user.transactions.append({
                "date_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "type": "Coupon",
                "amount": bonus,
                "balance": self.current_user.balance
            })
            self.save_users()
            print(f"Coupon Applied! Bonus: ₹{bonus:.2f}. New Balance: ₹{self.current_user.balance:.2f}")
        else:
            print("Invalid Coupon Code!")

    def view_transaction_history(self):
        if self.current_user:
            print("Date & Time | Type | Amount | Balance")
            print("------------------------------------------------------")
            for txn in self.current_user.transactions:
                print(f"{txn['date_time']} | {txn['type']} | ₹{txn['amount']} | ₹{txn['balance']}")
        else:
            print("No user logged in!")

    def update_profile(self, name, email, phone):
        if self.current_user:
            self.current_user.profile["name"] = name
            self.current_user.profile["email"] = email
            self.current_user.profile["phone"] = phone
            self.save_users()
            print("Profile Updated Successfully!")
        else:
            print("No user logged in!")

    def view_profile(self):
        if self.current_user:
            profile = self.current_user.profile
            print("Profile Information:")
            print(f"Name: {profile['name']}")
            print(f"Email: {profile['email']}")
            print(f"Phone: {profile['phone']}")
        else:
            print("No user logged in!")

if __name__ == "__main__":
    app = WalletApp()
    print("Welcome to Wallet Application")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            app.register(input("Username: "), input("Password: "), float(input("Initial Balance: ")))
        elif choice == "2":
            if app.login(input("Username: "), input("Password: ")):
                while True:
                    print("\n4. Check Balance\n5. Deposit Money\n6. Withdraw Money\n7. Apply Coupon\n8. View Transaction History\n9. Update Profile\n10. View Profile\n11. Logout")
                    sub_choice = input("Select an option: ")
                    if sub_choice == "4":
                        app.check_balance()
                    elif sub_choice == "5":
                        app.deposit_money(float(input("Enter amount: ")))
                    elif sub_choice == "6":
                        app.withdraw_money(float(input("Enter amount: ")))
                    elif sub_choice == "7":
                        app.apply_coupon(input("Enter coupon code: "))
                    elif sub_choice == "8":
                        app.view_transaction_history()
                    elif sub_choice == "9":
                        app.update_profile(input("Enter new Name: "), input("Enter new Email: "), input("Enter new Phone: "))
                    elif sub_choice == "10":
                        app.view_profile()
                    elif sub_choice == "11":
                        app.current_user = None
                        print("User Logged out from the App")
                        break
                    else:
                        print("Invalid choice selected!")
        elif choice == "3":
            print("Thank you\n User Exited from the Application")
            break
        else:
            print("Invalid choice selected")
