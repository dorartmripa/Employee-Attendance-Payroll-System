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
        
        cursor.execute("INSERT INTO attendance (employee_id, date, hours), VALUES (?, ?, ?)", (id, date, hours))
        database.commit()
        print("Attendance added successfully!")
        break

def update_attendance():
    while True:
        try:
            print("To update an attendance, please add the following: ")
            id = int(input("Enter the id of the employee you would like to record attendance: "))
        except ValueError:
            print("Uh-oh! Please enter a number!")
            continue
        
        cursor.execute("SELECT 1 from attendance WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("Uh-oh! There is no attendance with that id!") 
            continue








def main():
    sql_database()
    
if __name__ == "__main__":
    main()