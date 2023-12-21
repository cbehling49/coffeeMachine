"""
Project 3 - Coffee Machine
Cody Behling
CS-1410-602

I declare that the following source code was written solely by me.
I understand that copying any source code, in whole or in part, constitutes cheating.
I will receive a zero on this project if I am found in violation of this policy.
"""


class CoffeeMachine:
    """
    Outside interface to user.
    Puts coins in the CashBox.
    Tells the Selector to process the user's selection.
    """

    # constructor / initializer
    def __init__(self):
        self.cashBox = CashBox()
        self.selector = Selector(self.cashBox)

    # allows user to interact with the coffee machine
    def one_action(self):
        # user commands
        print("\n______________________________________\n\tPRODUCT LIST: all 35 cents, except bouillon (25 cents)\n\t1=black, 2=white, 3=sweet, 4=white & sweet, 5=bouillon\n\tSample commands: insert 25, select 1.")
        response = input("Your command: ").lower()
        response = response.split()

        # user can insert coins
        if response[0] == 'insert':
            if not len(response) > 1:
                print("No coin entered. Please try again.")
            coinValue = int(response[1])
            self.cashBox.deposit(coinValue)
        # user can select product
        elif response[0] == 'select':
            if 1 <= int(response[1]) <= 5:
                selection = int(response[1])
                self.selector.select(selection)
            else:
                print("Please select one of the five available options.")
        # user can cancel transaction
        elif response[0] == 'cancel':
            self.cashBox.return_coins()
        # user can quit the session
        elif response[0] == 'quit':
            return False
        # user will be informed of invalid commands
        else:
            print("Invalid command.")

        return True

    # keeps track of all money deposited during this session
    def total_cash(self):
        total = float(self.cashBox.total())
        return total


class CashBox:
    """
    Knows how much it has received from previous transactions.
    Knows how much has been inserted from the current transaction.
    """

    # constructor / initializer
    def __init__(self):
        self.credit = 0
        self.totalReceived = 0

    # deposits money into the cash box
    def deposit(self, amount):
        # users may only enter one of four coin options at a time
        if amount not in [50, 25, 10, 5]:
            print("INVALID AMOUNT >>>\nWe only take half-dollars, quarters, dimes, and nickels.")
        else:
            self.credit += amount
            self.totalReceived += amount
            if self.credit < 100:
                print(f"Depositing {amount} cents. You have {self.credit} cents credit.")
            elif self.credit >= 100:
                print(f"Depositing {amount} cents. You have ${self.credit / 100:.2f} credit.")

    # returns any coins that were not spent on a product
    def return_coins(self):
        if 0 < self.credit < 100:
            print(f"Returning {self.credit} cents.")
        elif self.credit >= 100:
            print(f"Returning ${self.credit / 100:.2f}.")
        # returned change is subtracted from total coins deposited
        self.totalReceived -= self.credit
        # credits are reset to zero since excess coins were returned
        self.credit = 0
        return self.credit

    # checks to see if credit balance is enough to cover item price
    def have_you(self, amount):
        itemPrice = amount
        if self.credit >= itemPrice:
            return True
        else:
            return False

    # deducts cost from credit balance for current session
    def deduct(self, amount):
        itemPrice = amount
        self.credit -= itemPrice
        return self.credit

    # net value of all money deposited during this session
    def total(self):
        return self.totalReceived


class Selector:
    """
    Validates that enough money has been inserted for the selected Product.
    Initiates the dispensing of Product.
    """

    # constructor / initializer
    def __init__(self, cash_box):
        self.cashBox = cash_box
        self.products = []
        self.products.append(Product("Black", 35, f"Making black:\n\tDispensing cup\n\tDispensing coffee\n\tDispensing water"))
        self.products.append(Product("White", 35, f"Making white:\n\tDispensing cup\n\tDispensing coffee\n\tDispensing creamer\n\tDispensing water"))
        self.products.append(Product("Sweet", 35, f"Making sweet:\n\tDispensing cup\n\tDispensing coffee\n\tDispensing sugar\n\tDispensing water"))
        self.products.append(Product("White & Sweet", 35, f"Making white & sweet:\n\tDispensing cup\n\tDispensing coffee\n\tDispensing sugar\n\tDispensing creamer\n\tDispensing water"))
        self.products.append(Product("Bouillon", 25, f"Making bouillon:\n\tDispensing cup\n\tDispensing bouillon powder\n\tDispensing water"))

    # user's selection
    def select(self, choice_index):
        i = choice_index - 1
        if self.cashBox.have_you(self.products[i].price):
            print(self.products[i].recipe)
            self.cashBox.deduct(self.products[i].price)
            self.cashBox.return_coins()
        else:
            print("Sorry. Not enough money deposited.")


class Product:
    """
    Abstraction of the drink.
    Knows its recipe.
    Can dispense Product for the customer.
    """

    # constructor / initializer
    def __init__(self, name, price, recipe):
        self.name = name
        self.price = price
        self.recipe = recipe

    # gets the price for the user's selection
    def get_price(self):
        return self.price

    # uses recipe and makes the drink
    def make(self):
        return self.recipe


def main():
    # user's current session
    m = CoffeeMachine()
    while m.one_action():
        pass

    # print net coins deposited before session ended
    total = m.total_cash()
    print(f"Total cash received: ${total / 100:.2f}")


if __name__ == "__main__":
    main()
