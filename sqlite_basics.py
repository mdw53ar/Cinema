import sqlite3


def create_table():
    connection = sqlite3.connect("cinema.db")
    connection.execute("CREATE TABLE Seat (seat_id	TEXT, taken	INTEGER, price REAL)")
    connection.commit()
    connection.close()


def insert_record():
    connection = sqlite3.connect("cinema.db")
    connection.execute("INSERT INTO Seat (seat_id, taken, price) VALUES ('A1', '0', 90),('A2', '1', 100), ('A3', '0', 80)")
    connection.commit()
    connection.close()

def select_all():
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor() # because its a read operation
    cursor.execute("SELECT * FROM Seat")
    result = cursor.fetchall()  # the cursor contains the queried data from above.
                                #  however cursor is not the final object to get the data
    connection.close()
    return result


def update_value(occupied, seat):
    connection = sqlite3.connect("cinema.db")
    connection.execute("UPDATE Seat SET taken = ? WHERE seat_id = ?", [occupied, seat])
    connection.commit()
    connection.close()


def delete_record():
    connection = sqlite3.connect("cinema.db")
    connection.execute("DELETE FROM Seat WHERE seat_id = 'A3'")
    connection.commit()
    connection.close()


def seat_value_lookup(column, seat_id):
    connection = sqlite3.connect("cinema.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT {column} FROM Seat WHERE seat_id = ? ", [seat_id])
    result = cursor.fetchall()
    connection.close()

    return result[0][0]



print(seat_value_lookup("taken", "A1"))