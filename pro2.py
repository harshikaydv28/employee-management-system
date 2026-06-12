import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk


class EmployeeCRUD:

    def __init__(self):

        # DATABASE CONNECTION
        self.con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="harshika",
            database="company"
        )

        self.cur = self.con.cursor()

        # CREATE TABLE
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS employee(
            id INT PRIMARY KEY,
            name VARCHAR(100),
            salary FLOAT,
            department VARCHAR(100)
        )
        """)

        # GUI WINDOW
        self.root = Tk()
        self.root.title("Employee Management System")
        self.root.geometry("850x500")
        self.root.configure(bg="lightblue")

        title = Label(
            self.root,
            text="EMPLOYEE CRUD SYSTEM",
            font=("Arial", 20, "bold"),
            bg="navy",
            fg="white",
            pady=10
        )
        title.pack(fill=X)

        # ================= FORM =================

        form_frame = Frame(self.root, bg="lightblue")
        form_frame.pack(pady=20)

        Label(form_frame, text="Employee ID", font=("Arial", 12),
              bg="lightblue").grid(row=0, column=0, padx=10, pady=10)

        self.id_entry = Entry(form_frame, font=("Arial", 12))
        self.id_entry.grid(row=0, column=1, padx=10)
        Label(form_frame, text="Name", font=("Arial", 12),
              bg="lightblue").grid(row=1, column=0, padx=10, pady=10)

        self.name_entry = Entry(form_frame, font=("Arial", 12))
        self.name_entry.grid(row=1, column=1, padx=10)

        Label(form_frame, text="Salary", font=("Arial", 12),
              bg="lightblue").grid(row=2, column=0, padx=10, pady=10)

        self.salary_entry = Entry(form_frame, font=("Arial", 12))
        self.salary_entry.grid(row=2, column=1, padx=10)

        Label(form_frame, text="Department", font=("Arial", 12),
              bg="lightblue").grid(row=3, column=0, padx=10, pady=10)

        self.dept_entry = Entry(form_frame, font=("Arial", 12))
        self.dept_entry.grid(row=3, column=1, padx=10)

        # ================= BUTTONS =================

        btn_frame = Frame(self.root, bg="lightblue")
        btn_frame.pack(pady=10)

        Button(
            btn_frame,
            text="Add Employee",
            font=("Arial", 12, "bold"),
            bg="green",
            fg="white",
            width=15,
            command=self.add_employee
        ).grid(row=0, column=0, padx=10)

        Button(
            btn_frame,
            text="Update Employee",
            font=("Arial", 12, "bold"),
            bg="orange",
            fg="white",
            width=15,
            command=self.update_employee
        ).grid(row=0, column=1, padx=10)

        Button(
            btn_frame,
            text="Delete Employee",
            font=("Arial", 12, "bold"),
            bg="red",
            fg="white",
            width=15,
            command=self.delete_employee
        ).grid(row=0, column=2, padx=10)

        Button(
            btn_frame,
            text="Clear",
            font=("Arial", 12, "bold"),
            bg="gray",
            fg="white",
            width=15,
            command=self.clear_fields
        ).grid(row=0, column=3, padx=10)

        # ================= TABLE =================

        self.table = ttk.Treeview(
            self.root,
            columns=("ID", "Name", "Salary", "Department"),
            show="headings"
        )

        self.table.heading("ID", text="ID")
        self.table.heading("Name", text="Name")
        self.table.heading("Salary", text="Salary")
        self.table.heading("Department", text="Department")

        self.table.column("ID", width=100)
        self.table.column("Name", width=200)
        self.table.column("Salary", width=150)
        self.table.column("Department", width=200)

        self.table.pack(fill=BOTH, expand=True, pady=20)

        self.table.bind("<ButtonRelease-1>", self.get_data)

        self.show_employee()

        self.root.mainloop()

    # ================= ADD =================

    def add_employee(self):

        try:
            query = "INSERT INTO employee VALUES(%s,%s,%s,%s)"

            values = (
                int(self.id_entry.get()),
                self.name_entry.get(),
                float(self.salary_entry.get()),
                self.dept_entry.get()
            )

            self.cur.execute(query, values)
            self.con.commit()

            messagebox.showinfo("Success", "Employee Added Successfully")

            self.show_employee()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= SHOW =================

    def show_employee(self):

        for data in self.table.get_children():
            self.table.delete(data)

        self.cur.execute("SELECT * FROM employee")

        rows = self.cur.fetchall()

        for row in rows:
            self.table.insert("", END, values=row)

    # ================= GET DATA =================

    def get_data(self, event):

        cursor_row = self.table.focus()

        content = self.table.item(cursor_row)

        row = content['values']

        if row:

            self.clear_fields()

            self.id_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.salary_entry.insert(0, row[2])
            self.dept_entry.insert(0, row[3])

    # ================= UPDATE =================

    def update_employee(self):

        try:
            query = """
            UPDATE employee
            SET name=%s, salary=%s, department=%s
            WHERE id=%s
            """

            values = (
                self.name_entry.get(),
                float(self.salary_entry.get()),
                self.dept_entry.get(),
                int(self.id_entry.get())
            )

            self.cur.execute(query, values)
            self.con.commit()

            messagebox.showinfo("Success", "Employee Updated Successfully")

            self.show_employee()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= DELETE =================

    def delete_employee(self):

        try:
            query = "DELETE FROM employee WHERE id=%s"

            self.cur.execute(query, (int(self.id_entry.get()),))
            self.con.commit()

            messagebox.showinfo("Success", "Employee Deleted Successfully")

            self.show_employee()
            self.clear_fields()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ================= CLEAR =================

    def clear_fields(self):

        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.salary_entry.delete(0, END)
        self.dept_entry.delete(0, END)


# RUN PROGRAM
EmployeeCRUD()