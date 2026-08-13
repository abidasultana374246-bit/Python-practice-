import os

# Expense data file
FILE_NAME = "Expense_tracker.txt"

# Create the file automatically if it doesn't exist.
if not os.path.exists(FILE_NAME):
    open(FILE_NAME, "w").close()


# Check the current working directory.
print(os.getcwd())


# Add a new expense and save it to the file.
def add_expense():
    user = input("Expense name: ")

    # Keep asking until the user enters a valid number.
    while True:
        try:
            amount = int(input("Amount: "))
            break
        except ValueError:
            print("Plz enter a valid number")

    # Allow the user to skip the category.
    category = input("Category (or type skip): ").lower()

    if category == "skip":
        category = "No Category"

    # Append the new expense to the file.
    with open(FILE_NAME, "a") as file:
        file.write(user + "," + str(amount) + "," + category + "\n")

    print("Expense add")


# Display all saved expenses.
def show_expense():
    with open(FILE_NAME, "r") as file:
        show = file.read()

    print(show)


# Search for an expense by name.
def search_expense():
    src = input("Search expense: ")

    with open(FILE_NAME, "r") as file:
        data = file.readlines()

    found = False

    for i in data:
        line = i.split(",")

        if line[0] == src:
            print("Expense:", line[0])
            print("Amount:", line[1])
            print("Category:", line[2].strip())

            found = True

    if found == False:
        print("Not found")


# Calculate the total amount of all expenses.
def total_expense():
    total = 0

    with open(FILE_NAME, "r") as file:
        data = file.readlines()

    for i in data:
        line = i.split(",")

        amount = int(line[1])
        total = total + amount

    print("Total Expense:", total)


# Remove an expense from the file.
def remove_expense():
    delet = input("Remove: ")

    with open(FILE_NAME, "r") as file:
        data = file.readlines()

    new_data = []
    found = False

    for i in data:
        if delet in i:
            found = True
        else:
            new_data.append(i)

    if found == False:
        print("Data not found")
        return

    with open(FILE_NAME, "w") as file:
        file.writelines(new_data)

    print("Expense removed!")


# Main menu.
print("""====== Expense Tracker ======

1. Add Expense
2. Show All Expense
3. Search Expense
4. Total Expense
5. Remove Expense
6. Exit
""")


# Keep the program running until the user chooses Exit.
while True:
    c = input("Choice: ")

    if c == "1":
        add_expense()

    elif c == "2":
        show_expense()

    elif c == "3":
        search_expense()

    elif c == "4":
        total_expense()

    elif c == "5":
        remove_expense()

    elif c == "6":
        print("Exit")
        break

    else:
        print("Invalid choice")
