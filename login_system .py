import os


DATA_FOLDER = "data"
USER_FILE = os.path.join(DATA_FOLDER, "user_save.txt")


def setup_file():
    # Create data folder if it doesn't exist
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    # Create user_save.txt if it doesn't exist
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, "w") as file:
            pass


def signup():
    username = input("Enter username: ")

    if username_exists(username):
        print("Username already taken")
        return

    password = input("Enter password: ")

    with open(USER_FILE, "a") as file:
        file.write(f"{username},{password}\n")

    print("Signup successful!")


def username_exists(username):
    with open(USER_FILE, "r") as f:
        data = f.readlines()

    for line in data:
        if line.strip() == "":
            continue

        parts = line.strip().split(",")

        saved_user = parts[0]

        if username == saved_user:
            return True

    return False


def login():
    login_user = input("Enter username: ")
    login_pass = input("Enter your password: ")

    with open(USER_FILE, "r") as f:
        login_data = f.readlines()

    for data in login_data:
        if data.strip() == "":
            continue

        parts = data.strip().split(",")

        saved_user = parts[0]
        saved_pass = parts[1]

        if login_user == saved_user and login_pass == saved_pass:
            print("Login successful!")
            return

    print("Wrong username or password!")


# Setup folder and file automatically
setup_file()


while True:
    print("""
1. Signup
2. Login
3. Exit
""")

    c = input("Choice: ")

    if c == "1":
        signup()

    elif c == "2":
        login()

    elif c == "3":
        print("Bye")
        break

    else:
        print("Invalid choice")