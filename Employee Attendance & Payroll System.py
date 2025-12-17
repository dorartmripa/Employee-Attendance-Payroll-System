import sqlite3

database = sqlite3.connect("company.db")
cursor = database.cursor()

def sql_database():
    database.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        position TEXT,
        hourly_rate REAL
    ) 
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        hours REAL NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
    )
    """)

    database.commit()

def add_employee():
    print("To add the new employee, please add the following: ")
    name = input("Enter the name of the new employee: ").strip().capitalize()
    position = input("Enter the position of the new employee: ").strip().capitalize()
    hourly_rate = float(input("Enter the hourly rate of the new employee:  "))    

    cursor.execute("INSERT INTO employees (name, position, hourly_rate) VALUES (?, ?, ?) ", (name, position, hourly_rate))

    database.commit()
    print("New employee added successfully!")

def update_employee():
    while True:
        try:
            print("To update a employee, please add the following: ")
            id = int(input("Enter the id of the employee you would like to update:"))
        except ValueError:
            print("Uh-oh! Please enter a number!")
            continue

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("Uh-oh! There is no employee with that id!") 
            continue

        while True:
            choice = input("""What would you like to update:
                            \n- Name
                            \n- Position
                            \n- Hourly Rate""").strip().lower()

            if choice not in ["name", "position", "hourly_rate"]:
                print("Uh-oh! Please enter a valid option!")
                continue
            
            while True:
                update = input(f"Enter the new information for {choice}: ")

                if update == "hourly_rate":
                    try:
                        update = float(update)
                        cursor.execute("UPDATE employees SET hourly_rate = ? WHERE id = ?", (update, id))
                    except ValueError:
                        print("Uh-oh! Please enter a number!")
                        continue
                else:
                    cursor.execute(f"UPDATE employees SET {choice} = ? WHERE id = ?", (update.strip().lower().capitalize(), id))
                
                database.commit()
                print("The record was updated successfully!")
                break
            break
        break

def remove_employee():
    while True:
        try:
            print("To remove an employee, please add the following: ")
            id = int(input("Enter the id of the employee you would like to remove: "))
        except ValueError:
            print("Uh-oh! Please enter a number!")
            continue

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("Uh-oh! There is no employee with that id!") 
            continue

        cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
        database.commit()
        print("Employee removed successfully!")
        break

def record_attendance():
    while True:
        try:
            print("To record an attendance, please add the following: ")
            id = int(input("Enter the id of the employee you would like to record attendance: "))
        except ValueError:
            print("Uh-oh! Please enter a number!")
            continue

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("Uh-oh! There is no employee with that id!") 
            continue
        
        while True:
            date = input("Enter date of attendance (YYYY-MM-DD): ")
            try:
                hours = float(input("Enter the hours worked: "))
                break
            except ValueError:
                print("Uh-oh! Please enter a number!")
                continue
        
        cursor.execute("INSERT INTO attendance (employee_id, date, hours) VALUES (?, ?, ?)", (id, date, hours))
        database.commit()
        print("Attendance added successfully!")
        break

def update_attendance():
    while True:
        try:
            print("To update an attendance, please add the following: ")
            id = int(input("Enter the id of the attendance you would like to update: "))
        except ValueError:
            print("Uh-oh! Please enter a number!")
            continue
        
        cursor.execute("SELECT 1 from attendance WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("Uh-oh! There is no attendance with that id!") 
            continue

        while True:
            choice = input("""What would you like to update:\n
                        - Employee ID\n
                        - Date\n
                        - Hours\n
                        Enter one of the options: """).strip().lower()
            
            if choice not in ["employee id", "date", "hours"]:
                print("Uh-oh! Please enter a valid option!")
                continue

            while True:
                if choice == "employee id":
                    try:
                        update = int(input("Enter the new employee id: "))
                    except ValueError:
                        print("Uh-oh! Please enter a number!")
                        continue
                elif choice == "hours":
                    try:
                        update = float(input("Enter the new hours: "))
                    except ValueError:
                        print("Uh-oh! Please enter a number!")
                        continue
                else:
                    update = input("Enter the new date (YYYY-MM-DD): ")
                break
            break

        cursor.execute(f"UPDATE attendance SET {choice} = ? WHERE id = ?", (update, id))
        database.commit()
        print("Attendance updated successfully!")
        break

def search():
    while True:
        try:
            print("To search for an employee, please add the following: ")
            id = int(input("Enter the id of the employee you want to search for: "))
        except ValueError:
            print("Uh-oh! Please enter a number!")
            continue
        
        cursor.execute("SELECT * from employees WHERE id = ?", (id,))
        exists = cursor.fetchall()

        if not exists:
            print("Uh-oh! There is no employee with that id!") 
            continue

        cursor.execute("SELECT * FROM employees")
        header = [description[0] for description in cursor.description]
        print(header)
        print(exists, "\n")

        cursor.execute("SELECT * from attendance WHERE employee_id = ?", (id,))
        results = cursor.fetchall()

        print("Employee's attendance record: ")
        for result in results:
            print(result)
        
        break

def main():
    choices = ["add employee", "update employee", "remove employee", "search employee", "record attendance", "update attendance", "view reports"]
    sql_database()

    print("\n--- WELCOME TO EMPLOYEE ATTENDANCE & PAYROLL SYSTEM ---\n")

    while True: #loops until user doesn't want to make any more changes to the database
        print("Please select one of the following options: ")

        print("\nEmployee Management:")
        print("- Add employee")
        print("- Update employee")
        print("- Remove employee")
        print("- Search employee")

        print("\nAttendance Management:")
        print("- Record attendance")
        print("- Update attendance")
        print("- View reports\n")

        action = input("Enter your choice: ").strip().lower()

        if action not in choices: #checks if user entered a valid option
            while True:
                print("\nOops! That's not a valid option. Try again.\n")
                print("Please select one of the following options: ")

                print("\nEmployee Management:")
                print("- Add employee")
                print("- Update employee")
                print("- Remove employee")
                print("- Search employee")

                print("\nAttendance Management:")
                print("- Record attendance")
                print("- Update attendance")
                print("- View reports\n")

                action = input("Enter your choice: ").strip().lower()

                if action in choices: #breaks out of the loop if a valid option was entered
                    break
        
        if action == choices[0]: 
            add_employee()
        elif action == choices[1]:
            update_employee()
        elif action == choices[2]:
            remove_employee()
        elif action == choices[3]:
            search()
        elif action == choices[4]:
            record_attendance()
        elif action == choices[5]:
            update_attendance()
        else:
            reports()

        while True: #loops until user entered yer or no
            yes_or_no = input("Do you want to perform another inventory action? (yes/no): ").strip().lower()

            if yes_or_no in ["yes", "no"]:
                break #Exits loop if user entered a valid option

        if yes_or_no == "no": #ends code if user entered no
            print("\nThank you for using Employee Attendance & Payroll System!\n")
            database.close() #Closes connection to the database
            break #Exits the loop to end the program
    
if __name__ == "__main__":
    main()