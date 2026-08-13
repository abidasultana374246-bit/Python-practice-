students = {}


def main():
    name = input("Enter Your name: ")

    while True:
        try:
            bangla = int(input("Bangla Mark: "))
            english = int(input("English Mark: "))
            math = int(input("Math Mark: "))
            break
        except ValueError:
            print("Plz enter a valid number")

    total = calculate_total(bangla, english, math)
    average = calculate_average(total)
    grade = get_grade(average)

    add_student(name, bangla, english, math, average, total, grade)


def add_student(name, bangla, english, math, average, total, grade):
    students[name] = {
        "Bangla": bangla,
        "English": english,
        "Math": math,
        "Total": total,
        "Average": average,
        "Grade": grade
    }

    print("Student Added Successfully!")


def calculate_total(bangla, english, math):
    return bangla + english + math


def calculate_average(total):
    return total / 3


def get_grade(average):
    if average >= 85:
        return "A+"
    elif average >= 60:
        return "A-"
    elif average >= 40:
        return "D"
    else:
        return "Fail"


def search_student():
    srch = input("Search student: ")

    if srch in students:
        for key, value in students[srch].items():
            print(key, ":", value)
    else:
        print("Not found")


def show_all_students():
    if not students:
        print("No students found!")
    else:
        for key, value in students.items():
            print("Name:", key)

            for subject, mark in value.items():
                print(subject, ":", mark)

            print()


def delete_student():
    name = input("Delete student name: ")

    if name not in students:
        print("Student Not Found!")
        return

    ch = input("Confirm? (yes/no): ").lower()

    if ch == "yes":
        del students[name]
        print("Student Deleted!")

    elif ch == "no":
        print("Okay, not deleted.")

    else:
        print("Invalid choice.")


print("""====== Student Management ======

1. Add Student
2. Search Student
3. Show All Student
4. Delete Student
5. Exit
""")


while True:
    c = input("Enter choice: ")

    if c == "1":
        main()

    elif c == "2":
        search_student()

    elif c == "3":
        show_all_students()

    elif c == "4":
        delete_student()

    elif c == "5":
        print("Welcome.. Bye")
        break

    else:
        print("Invalid choice")
