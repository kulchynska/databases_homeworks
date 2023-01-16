import sqlite3

conn = sqlite3.connect(':memory:')

c = conn.cursor()

# create table 'referral_code'
c.execute("""CREATE TABLE referral_code (
            id INTEGER PRIMARY KEY ,
            ref_code TEXT
            )""")

# create table 'users'
c.execute("""CREATE TABLE users (
            id INTEGER PRIMARY KEY ,
            first_name TEXT,
            last_name TEXT,
            email NOT NULL UNIQUE,
            ref_code_id INTEGER,
            FOREIGN KEY (ref_code_id) REFERENCES referral_code (id) 
            ON DELETE CASCADE ON UPDATE NO ACTION
            )""")

# create table 'rooms'
c.execute("""CREATE TABLE rooms (
            id INTEGER PRIMARY KEY ,
            room_type TEXT,
            number_of_children INTEGER,
            number_of_adults INTEGER,
            room_name TEXT
            )""")

# create table 'users_rooms'
c.execute("""CREATE TABLE users_rooms (
            user_id INTEGER,
            room_id INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(room_id) REFERENCES rooms(id)
            )""")


# insert users
def insert_data():
    with conn:
        # insert data into 'users'
        c.execute("INSERT INTO users VALUES (NULL, :first_name, :last_name, :email, NULL)",
                  {'first_name': "Anna", 'last_name': "Kulchynska", 'email': "kumshoyububliki@gmail.com"})
        c.execute("INSERT INTO users VALUES (NULL, :first_name, :last_name, :email, NULL)",
                  {'first_name': "Chris", 'last_name': "Evans", 'email': "chrissyevansy@gmail.com"})

        # insert data into 'rooms'
        c.execute("INSERT INTO rooms VALUES (NULL, :room_type, :number_of_children, :number_of_adults, :room_name)",
                  {'room_type': 'economy', 'number_of_children': 2, 'number_of_adults': 2, 'room_name': 'Mirabella'})
        c.execute("INSERT INTO rooms VALUES (NULL, :room_type, :number_of_children, :number_of_adults, :room_name)",
                  {'room_type': 'presidential luxe', 'number_of_children': 0, 'number_of_adults': 3, 'room_name': 'Eleonora'})

        # insert data into 'users_rooms'
        c.execute("INSERT INTO users_rooms VALUES (:user_id, :room_id)",
                  {'user_id': 1, 'room_id': 2})
        c.execute("INSERT INTO users_rooms VALUES (:user_id, :room_id)",
                  {'user_id': 2, 'room_id': 1})


def get_users():
    c.execute("SELECT * FROM users")
    return c.fetchall()


def get_rooms():
    c.execute("SELECT * FROM rooms")
    return c.fetchall()


def get_users_to_rooms_where_clause():
    c.execute("SELECT users.first_name || ' ' || users.last_name, rooms.room_name FROM users, users_rooms, rooms WHERE users.id = users_rooms.user_id AND rooms.id = users_rooms.room_id")
    return c.fetchall()


def get_users_to_rooms_join():
    c.execute("SELECT users.first_name || ' ' || users.last_name, rooms.room_name FROM users_rooms INNER JOIN users ON users.id =users_rooms.user_id INNER JOIN rooms ON rooms.id = users_rooms.room_id")
    return c.fetchall()


insert_data()
print(get_users())
print(get_rooms())
print(get_users_to_rooms_where_clause())
print(get_users_to_rooms_join())
