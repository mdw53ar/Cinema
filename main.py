import sqlite3


class BankCard:

    def __init__(self, card_type, card_number, cvc, card_holder_name):
        self.card_type = card_type
        self.card_number = card_number
        self.cvc = cvc
        self.card_holder_name = card_holder_name


class CinemaSeat:

    def __init__(self, full_name, seat_number):
        self.full_name = full_name
        self.seat_number = seat_number

    def purchase(self, bank):

        if self.is_bank_verified(bank):
            print("Card successfully verified")
        else:
            raise ValueError("Card verification Failed")

        if self.is_seat_free():
            print("Seat still available")
        else:
            raise ValueError("Seat already taken")

        print("--> Verification successful")

        self.update_balance(bank)

        self.set_seat_to_taken()

        print("Purchase successful!")

    def update_balance(self, bank):
        price_lookup = self.seat_value_lookup("price", self.seat_number)
        connection = sqlite3.connect("banking.db")
        connection.execute(f"UPDATE Card SET balance = balance - {price_lookup} WHERE holder = ?", [bank.card_holder_name])
        connection.commit()
        connection.close()
        print("Updating balance")

    def set_seat_to_taken(self):
        connection = sqlite3.connect("cinema.db")
        connection.execute(f"UPDATE Seat SET taken = 1 WHERE seat_id = ?", [self.seat_number])
        connection.commit()
        connection.close()
        print("Setting seat to taken")

    def is_bank_verified(self, bank):
        holder = bank.card_holder_name
        type_lookup = self.card_value_lookup("type", holder)
        number_lookup = self.card_value_lookup("number", holder)
        cvc_lookup = self.card_value_lookup("cvc", holder)
        balance_lookup = self.card_value_lookup("balance", holder)
        price_lookup = self.seat_value_lookup("price", self.seat_number)

        return (type_lookup == bank.card_type) and (number_lookup == bank.card_number) and (cvc_lookup == bank.cvc) and (balance_lookup >= price_lookup)

    def is_seat_free(self):
        seat_lookup = self.seat_value_lookup("taken", self.seat_number)
        return seat_lookup == 0


    @staticmethod
    def card_value_lookup(column, card_holder_name):

        connection = sqlite3.connect("banking.db")
        cursor = connection.cursor()
        cursor.execute(f"SELECT {column} FROM Card WHERE holder = ? ", [card_holder_name])
        result = cursor.fetchall()
        connection.close()

        return result[0][0]

    @staticmethod
    def seat_value_lookup(column, seat_id):
        connection = sqlite3.connect("cinema.db")
        cursor = connection.cursor()
        cursor.execute(f"SELECT {column} FROM Seat WHERE seat_id = ? ", [seat_id])
        result = cursor.fetchall()
        connection.close()

        return result[0][0]


bank = BankCard("Visa", "12345678", "123", "John Smith")
cinema = CinemaSeat("John Smith", "A2")

cinema.purchase(bank)