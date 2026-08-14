# Login System 🔐

A simple command-line Login System built with Python.

This project allows users to create an account and log in using a username and password.

## ✨ Features

- User Signup
- User Login
- Username availability check
- Password verification
- Prevent duplicate usernames
- Automatic data folder creation
- Automatic user data file creation
- Simple command-line interface
- Local user data storage

## 🔄 Updated Version

This is an improved version of my earlier Login System project.

### Improvements Made

In the earlier version, the program used a fixed file path to store user data.

In this updated version, I used Python's `os` module to make the project more flexible and portable.

The program now automatically:

1. Creates a `data` folder if it doesn't exist.
2. Creates the `user_save.txt` file if it doesn't exist.
3. Uses a relative path instead of depending on a specific Android storage path.

### Important ⚠️

The `data` folder and `user_save.txt` file are created automatically when the program runs.

You don't need to create them manually.

## 🛠️ Technologies Used

- Python
- `os` module
- File Handling

## 📚 Python Concepts Practiced

This project helped me practice:

- Functions
- Dictionaries
- `if / elif / else`
- `while` loops
- `for` loops
- `try / except`
- File Handling
- `os.path.exists()`
- `os.makedirs()`
- `os.path.join()`
- User Input
- String Processing

## 🚀 How It Works

### 1. Signup

The user enters a username and password.

The program checks whether the username already exists.

If the username is available, the account information is saved locally.

### 2. Login

The user enters their username and password.

The program checks the saved user data.

If the username and password match, the login is successful.

### 3. Automatic File Setup

The program checks whether the required folder and file exist.

If they don't exist, they are automatically created.

This makes the project easier to use on a new device.

## 💻 Project Type

Command-Line Application

## 🔮 Future Improvements

- Password hashing
- Better error handling
- Edit account information
- Change password
- Multiple user roles
- JSON or database storage
- Better user interface

## 👨‍💻 Author

**Abdullah**

This is a learning project created while learning Python, file handling, and automation concepts.
## 📁 Project Structure

```text
Login-System/
│
├── login.py
│
└── data/
    └── user_save.txt
