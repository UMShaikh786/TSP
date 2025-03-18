import mysql.connector as mysql

def connect_db():
    try:
        con = mysql.connect(host="localhost", user="root", passwd="useraryan", database="TODOAPP")
        return con
    except mysql.Error as err:
        print(f"Error: {err}")
        exit()

def create_db_and_table():
    con = mysql.connect(host="localhost", user="root", passwd="useraryan")
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS TODOAPP")
    cursor.execute("USE TODOAPP")
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tb_todo (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task VARCHAR(255) NOT NULL,
            status ENUM('pending', 'completed') DEFAULT 'pending'
        )
        """
    )
    con.close()

def add_task(con):
    task = input("Enter task: ")
    cursor = con.cursor()
    cursor.execute("INSERT INTO tb_todo (task) VALUES (%s)", (task,))
    con.commit()
    print("Task added successfully!")

def view_tasks(con):
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tb_todo")
    tasks = cursor.fetchall()
    if tasks:
        print("\nTasks:")
        for task in tasks:
            print(f"ID: {task[0]}, Task: {task[1]}, Status: {task[2]}")
    else:
        print("No tasks found.")

def update_task(con):
    task_id = input("Enter task ID to update: ")
    new_task = input("Enter new task description: ")
    new_status = input("Enter new status (pending/completed): ")
    cursor = con.cursor()
    cursor.execute("UPDATE tb_todo SET task = %s, status = %s WHERE id = %s", (new_task, new_status, task_id))
    con.commit()
    print("Task updated successfully!")

def delete_task(con):
    task_id = input("Enter task ID to delete: ")
    cursor = con.cursor()
    cursor.execute("DELETE FROM tb_todo WHERE id = %s", (task_id,))
    con.commit()
    print("Task deleted successfully!")

def main():
    create_db_and_table()
    con = connect_db()
    while True:
        print("\nTask Management")
        print("1. Add Task")
        print("2. View Task")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            add_task(con)
        elif choice == "2":
            view_tasks(con)
        elif choice == "3":
            update_task(con)
        elif choice == "4":
            delete_task(con)
        elif choice == "5":
            print("Exiting Task Management...")
            break
        else:
            print("Invalid choice. Please try again.")
    con.close()

if __name__ == "__main__":
    main()
