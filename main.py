from classes import BankCard, CinemaSeat

bank = BankCard("Visa", "12345678", "123", "John Smith")
cinema = CinemaSeat("John Smith", "A3")

cinema.purchase(bank)