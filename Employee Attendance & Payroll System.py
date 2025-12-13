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
        while True:
            try:
                print("To update a employee, please add the following: ")
                id = int(input("Enter the id of the employee you would like to update:"))
                break
            except ValueError:
                print("Uh-oh! Please enter a number!")

        cursor.execute("SELECT 1 from employees WHERE id = ? LIMIT 1", (id,))
        exists = cursor.fetchone()

        if not exists:
            print("Uh-oh! There is no employee with that id!") 
            continue

        while True:
            choice = input("What woudl you like to update:\n- Name\n- Position\n- Hourly Rate").strip().lower()

            if choice not in ["name", "position", "hourly_rate"]:
                print("Uh-oh! Please enter a valid option!")
                continue
            
            update = input(f"Enter the new information for {choice}: ")

            if choice == "name":
                cursor.execute("UPDATE employees SET name = ? WHERE id = ?", (update.strip().lower().capitalize(), id))







def main():
    sql_database()

if __name__ == "__main__":
    main()