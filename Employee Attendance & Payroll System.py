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
    name = input("Enter the name of the new employee: ").strip().title()
    position = input("Enter the position of the new employee: ").strip().title()
    hourly_rate = float(input("Enter the hourly rate of the new employee:  "))    

    cursor.execute("INSERT INTO employees (name, position, hourly_rate) VALUES (?, ?, ?) ", (name, position, hourly_rate))

    database.commit()
    print("\nNew employee added successfully!\n")

def update_employee():
    while True:
        try:
            print("To update a employee, please add the following: ")
            id = int(input("Enter the id of the employee you would like to update:"))
        except ValueError:
            print("\nUh-oh! Please enter a number!\n")
            continue

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("\nUh-oh! There is no employee with that id!\n") 
            continue

        while True:
            print("What would you like to update:")
            print("- Name")
            print("- Position")
            print("- Hourly Rate: ")
            choice = input("Enter your choice: ").strip().lower()

            if choice not in ["name", "position", "hourly rate"]:
                print("\nUh-oh! Please enter a valid option!\n")
                continue
            
            while True:
                update = input(f"Enter the new information for {choice}: ")

                if choice == "hourly rate":
                    try:
                        update = float(update)
                        cursor.execute("UPDATE employees SET hourly_rate = ? WHERE id = ?", (update, id))
                    except ValueError:
                        print("\nUh-oh! Please enter a number!\n")
                        continue
                else:
                    cursor.execute(f"UPDATE employees SET {choice} = ? WHERE id = ?", (update.strip().lower().title(), id))
                
                database.commit()
                print("\nThe record was updated successfully!\n")
                break
            break
        break

def remove_employee():
    while True:
        try:
            print("To remove an employee, please add the following: ")
            id = int(input("Enter the id of the employee you would like to remove: "))
        except ValueError:
            print("\nUh-oh! Please enter a number!\n")
            continue

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("\nUh-oh! There is no employee with that id!\n") 
            continue

        cursor.execute("DELETE FROM employees WHERE id = ?", (id,))
        database.commit()
        print("\nEmployee removed successfully!\n")
        break

def record_attendance():
    while True:
        try:
            print("To record an attendance, please add the following: ")
            id = int(input("Enter the id of the employee you would like to record attendance: "))
        except ValueError:
            print("\nUh-oh! Please enter a number!\n")
            continue

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("\nUh-oh! There is no employee with that id!\n") 
            continue
        
        while True:
            date = input("Enter date of attendance (YYYY-MM-DD): ")
            try:
                hours = float(input("Enter the hours worked: "))
                break
            except ValueError:
                print("\nUh-oh! Please enter a number!\n")
                continue
        
        cursor.execute("INSERT INTO attendance (employee_id, date, hours) VALUES (?, ?, ?)", (id, date, hours))
        database.commit()
        print("\nAttendance added successfully!\n")
        break

def update_attendance():
    while True:
        try:
            print("To update an attendance, please add the following: ")
            id = int(input("Enter the id of the attendance you would like to update: "))
        except ValueError:
            print("\nUh-oh! Please enter a number!\n")
            continue
        
        cursor.execute("SELECT 1 from attendance WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("\nUh-oh! There is no attendance with that id!\n") 
            continue

        while True:
            print("What would you like to update:")
            print("- Employee ID")
            print("- Date")
            print("- Hours ")
            choice = input("Enter your choice: ").strip().lower()
            
            if choice not in ["employee id", "date", "hours"]:
                print("\nUh-oh! Please enter a valid option!\n")
                continue

            while True:
                if choice == "employee id":
                    try:
                        update = int(input("Enter the new employee id: "))
                    except ValueError:
                        print("\nUh-oh! Please enter a number!\n")
                        continue
                elif choice == "hours":
                    try:
                        update = float(input("Enter the new hours: "))
                    except ValueError:
                        print("\nUh-oh! Please enter a number!\n")
                        continue
                else:
                    update = input("Enter the new date (YYYY-MM-DD): ")
                break
            break

        cursor.execute(f"UPDATE attendance SET {choice} = ? WHERE id = ?", (update, id))
        database.commit()
        print("\nAttendance updated successfully!\n")
        break

def search():
    while True:
        print("To search for an employee, please add the following: ")
        name = input("Enter the id of the employee you want to search for: ").strip()
        
        cursor.execute("SELECT * from employees WHERE name LIKE ?", (f"%{name}%",))
        exists = cursor.fetchall()

        if not exists:
            print("\nUh-oh! There is no employee with that name!\n") 
            continue

        print(f"Employee names that match *{name}*:\n")

        cursor.execute("SELECT * FROM employees")
        header = [description[0] for description in cursor.description]
        print(header)
        
        for results in exists:
            print(results)

        break

def reports():
    while True:
        try:
            print("To view an employee's report, please add the following: ")
            id = int(input("Enter the id of the attendance you would like to update: "))
        except ValueError:
            print("\nUh-oh! Please enter a number!\n")
            continue

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("\nUh-oh! There is no employee with that id!\n") 
            continue

        cursor.execute("SELECT hours, date from attendance WHERE employee_id = ?", (id,))
        attendances = cursor.fetchall()

        while True:
            months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            year = input("Enter the year you want to calculate monthly payroll: ")
            date = input("Enter the month you want to calculate monthly payroll (01-12): ")

            if date not in months:
                print("\nUh-oh! Invalid month! Please enter the month (01-12)\n") 
                continue
            
            attendances = list(
                filter(lambda attendance: attendance[1][:7] == year + "-" + date, attendances)
                )

            hours = sum(hour[0] for hour in attendances)
            cursor.execute("SELECT hourly_rate from employees WHERE id = ?", (id,))
            hourly_rate = cursor.fetchone()[0]

            monthly_payroll = round(hours * hourly_rate, 2)
            break

        cursor.execute("SELECT name from employees WHERE id = ?", (id,))
        name = cursor.fetchone()[0]         

        print(f"Employee ID: {id} | Monthly Payroll for {name}: £{monthly_payroll}\n")
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