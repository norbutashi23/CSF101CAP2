#######################################
# Tashi Norbu
# First Year Electronics and Communication Engineering
# 02230108
#######################################
# Reference 
# https://www.youtube.com/watch?v=xTh-ln2XhgU
# https://www.youtube.com/watch?v=2TrDIbwasw8
# https://www.w3schools.com/python/python_classes.asp



import os
import random
import string

# Functions for creating a password and bank ID by generating randomly 7 digit bank id number and 5 character password
def create_default_bank_id_number():
    return ''.join(random.choices(string.digits, k=7))

def create_default_pass_ac2():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=5))

# Bank Account Class
class BankAccount:
    # pass_ac2 (password) and typo_ac2 (account type)
    def __init__(self, bank_id_number, pass_ac2, typo_ac2, remaining_money=0):
        # initialize a bank ac with account type, password, bank ID number, and amount of money left to a bank account.
        self.bank_id_number = bank_id_number
        self.pass_ac2 = pass_ac2
        self.typo_ac2 = typo_ac2
        self.remaining_money = remaining_money

    def deposit(self, teru_gamchi):
        # adding money to the account
        self.remaining_money += teru_gamchi
        print(f"Added Nu {teru_gamchi}. New balance is Nu {self.remaining_money}.")

    def withdraw(self, teru_gamchi):
        # Takes money out of the account if there is enough amount
        if teru_gamchi > self.remaining_money:
            print("Not enough money.")
        else:
            self.remaining_money -= teru_gamchi
            print(f"Withdrew Nu {teru_gamchi}. New balance is Nu {self.remaining_money}.")

    def check_balance(self):
        print(f"Account balance is Nu {self.remaining_money}.")

class PersonalAccount(BankAccount):
    def __init__(self, bank_id_number, pass_ac2, remaining_money=0):
        super().__init__(bank_id_number, pass_ac2, "Personal", remaining_money)

class BusinessAccount(BankAccount):
    def __init__(self, bank_id_number, pass_ac2, remaining_money=0):
        super().__init__(bank_id_number, pass_ac2, "Business", remaining_money)

class Bank:
    def __init__(self, filepath="accounts.txt"):
        self.filepath = filepath
        self.accounts = self.load_accounts()

    def load_accounts(self):
        accounts = {}
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as file:
                for line in file:
                    bank_id_number, pass_ac2, typo_ac2, remaining_money = line.strip().split(',')
                    remaining_money = float(remaining_money)
                    account_class = PersonalAccount if typo_ac2 == "Personal" else BusinessAccount
                    accounts[bank_id_number] = account_class(bank_id_number, pass_ac2, remaining_money)
        return accounts

    def save_accounts(self):
        with open(self.filepath, 'w') as file:
            for account in self.accounts.values():
                file.write(f"{account.bank_id_number},{account.pass_ac2},{account.typo_ac2},{account.remaining_money}\n")

    def open_account(self, typo_ac2):
        # Launches a new account of the chosen account type.
        typo_ac2 = typo_ac2.lower()
        if typo_ac2 not in ["personal", "business"]:
            print("Invalid account type. Please enter 'Personal' or 'Business'.")
            return

        bank_id_number = create_default_bank_id_number()
        pass_ac2 = create_default_pass_ac2()
        account_class = PersonalAccount if typo_ac2 == "personal" else BusinessAccount
        account = account_class(bank_id_number, pass_ac2)
        self.accounts[bank_id_number] = account
        self.save_accounts()
        print(f"Account created. Account Number: {bank_id_number}, Password: {pass_ac2}")

    def login(self, bank_id_number, pass_ac2):
        account = self.accounts.get(bank_id_number)
        if account and account.pass_ac2 == pass_ac2:
            print("Login successful.")
            return account
        print("Invalid account number or password.")
        return None

    def delete_account(self, bank_id_number):
        # deletes an existing bank account
        if bank_id_number in self.accounts:
            del self.accounts[bank_id_number]
            self.save_accounts()
            print("Account deleted.")
        else:
            print("Account not found.")

    def transfer_money(self, from_account, to_bank_id_number, teru_gamchi):
        # Sends money to other account
        to_account = self.accounts.get(to_bank_id_number)
        if not to_account:
            print("There is no receiving account.")
            return
        if from_account.remaining_money < teru_gamchi:
            print("Not enough money.")
            return

        from_account.withdraw(teru_gamchi)
        to_account.deposit(teru_gamchi)
        self.save_accounts()
        print(f"Transferred Nu {teru_gamchi} to account {to_bank_id_number}.")

def main():
    # main function given
    bank = Bank()
    while True:
        print("\nWelcome to DAZ Banking.")
        print("1. Create Account")
        print("2. Login to your existing account")
        print("3. Delete your Account")
        print("4. Exit")
        choice = input("Enter your option: ")

        if choice == '1':
            account_type = input("Choose the type of account you want (Personal/Business): ").lower()
            bank.open_account(account_type)

        elif choice == '2':
            bank_id_number = input("Enter account number: ")
            pass_ac2 = input("Enter password: ")
            account = bank.login(bank_id_number, pass_ac2)
            if account:
                while True:
                    print("\n--- Account Options ---")
                    print("1. Check your Balance")
                    print("2. Deposit your money")
                    print("3. Withdraw your money")
                    print("4. Transfer Money to another")
                    print("5. Logout")
                    action = input("Enter your option: ")

                    if action == '1':
                        account.check_balance()
                    elif action == '2':
                        teru_gamchi = float(input("Put in the amount you want to deposit: "))
                        account.deposit(teru_gamchi)
                        bank.save_accounts()
                    elif action == '3':
                        teru_gamchi = float(input("Enter the amount you want to withdraw: "))
                        account.withdraw(teru_gamchi)
                        bank.save_accounts()
                    elif action == '4':
                        to_bank_id_number = input("Type in the account number to make the transfer: ")
                        teru_gamchi = float(input("Enter your amount to transfer: "))
                        bank.transfer_money(account, to_bank_id_number, teru_gamchi)
                    elif action == '5':
                        break
                    else:
                        print("Invalid choice.")
        elif choice == '3':
            bank_id_number = input("To remove, enter your account number: ")
            bank.delete_account(bank_id_number)
        elif choice == '4':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
    