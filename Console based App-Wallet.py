import json
import datetime
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
            print("User already exists!,try with new User")
            return
        self.users[username] = User(username, password, initial_balance)
        self.save_users()
        print("User Registered Successfully!")

    def login(self, username, password):
        if username in self.users and self.users[username].password == password:
            self.current_user = self.users[username]
            print("Login Successful!")
        else:
            print("Invalid Credentials!")

    def check_balance(self):
        if self.current_user:
            print(f"Current Balance: ${self.current_user.balance}")
        else:
            print("No user logged in to the App!")

    def deposit_money(self, amount):
        if self.current_user and amount > 0:
            self.current_user.balance += amount
            self.current_user.transactions.append({
                "date": str(datetime.date.today()),
                "type": "Deposit",
                "amount": amount,
                "balance": self.current_user.balance
            })
            self.save_users()
            print(f"Balance Updated! New Balance: ${self.current_user.balance}")
        else:
            print("Invalid operation!")

    def withdraw_money(self, amount):
        if self.current_user and 0 < amount <= self.current_user.balance:
            self.current_user.balance -= amount
            self.current_user.transactions.append({
                "date": str(datetime.date.today()),
                "type": "Withdraw",
                "amount": -amount,
                "balance": self.current_user.balance
            })
            self.save_users()
            print(f"Transaction Successful! New Balance: ${self.current_user.balance}")
        else:
            print("Error: Insufficient Balance or Invalid Amount!")

    def apply_coupon(self, coupon_code):
        coupons = {"SAVE10": 0.10,
                   "BONUS20": 0.20,
                   "DISCOUNT15": 0.15,
                   "SUMMER25": 0.25,
                   "NEWYEAR30": 0.30,
                   "WELCOME50": 0.50,
                   "EXTRA35": 0.35,
                   }
        if self.current_user and coupon_code in coupons:
            bonus = self.current_user.balance * coupons[coupon_code]
            self.current_user.balance += bonus
            self.current_user.transactions.append({
                "date": str(datetime.date.today()),
                "type": "Coupon",
                "amount": bonus,
                "balance": self.current_user.balance
            })
            self.save_users()
            print(f"Coupon Applied! Bonus: ${bonus}. New Balance: ${self.current_user.balance}")
        else:
            print("Invalid Coupon Code or No user logged in to the App!")

    def view_transaction_history(self):
        if self.current_user:
            print("Date | Type | Amount | Balance")
            print("--------------------------------------")
            for txn in self.current_user.transactions:
                print(f"{txn['date']} | {txn['type']} | ${txn['amount']} | ${txn['balance']}")
        else:
            print("No user logged in to the App!")

    def update_profile(self, name, email, phone):
        if self.current_user:
            self.current_user.profile["name"] = name
            self.current_user.profile["email"] = email
            self.current_user.profile["phone"] = phone
            self.save_users()
            print("Profile Updated Successfully!")
        else:
            print("No user logged in to the App!")

if __name__ == "__main__":
    app = WalletApp()
    while True:
        print("\n1. Register\n2. Login\n3. Check Balance\n4. Deposit Money\n5. Withdraw Money\n6. Apply Coupon\n7. View Transactions\n8. Update Profile\n9. Logout\n10. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            app.register(input("Username: "), input("Password: "), float(input("Initial Balance: ")))
        elif choice == "2":
            app.login(input("Username: "), input("Password: "))
        elif choice == "3":
            app.check_balance()
        elif choice == "4":
            app.deposit_money(float(input("Enter amount: ")))
        elif choice == "5":
            app.withdraw_money(float(input("Enter amount: ")))
        elif choice == "6":
            app.apply_coupon(input("Enter coupon code: "))
        elif choice == "7":
            app.view_transaction_history()
        elif choice == "8":
            app.update_profile(input("Enter new Name: "),input("Enter new Email: "),input("Enter new Phone: "))
        elif choice == "9":
            app.current_user = None
            print("Logged out from the App")
        elif choice == "10":
            break
        else:
            print("Invalid choice selected!")
