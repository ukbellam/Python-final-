import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime


def initialize_db():
    conn = sqlite3.connect('health_tracker.db')
    cursor = conn.cursor()

   
    cursor.execute('''DROP TABLE IF EXISTS blood_sugar''')
    
   
    cursor.execute('''CREATE TABLE IF NOT EXISTS blood_sugar (
                        date_time TEXT PRIMARY KEY,
                        level REAL
                      )''')
    conn.commit()
    conn.close()


initialize_db()


def add_blood_sugar_data():
    try:
        date = date_entry.get().strip()
        time = time_entry.get().strip()
        level = float(level_entry.get().strip())

        # Check if the date and time are in the correct format (MM-DD-YYYY and HH:MM 24-hour format)
        try:
            datetime_object = datetime.strptime(f"{date} {time}", "%m-%d-%Y %H:%M")
            formatted_date_time = datetime_object.strftime("%m-%d-%Y %H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format. Please use MM-DD-YYYY for date and HH:MM (24-hour format) for time.")
            return

        conn = sqlite3.connect('health_tracker.db')
        cursor = conn.cursor()

        cursor.execute('''INSERT OR REPLACE INTO blood_sugar (date_time, level) VALUES (?, ?)''', (formatted_date_time, level))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Blood sugar data added successfully!")
        date_entry.delete(0, tk.END)
        time_entry.delete(0, tk.END)
        level_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Invalid blood sugar level. Please enter a valid number.")
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", str(e))


def view_blood_sugar_data():
    conn = sqlite3.connect('health_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM blood_sugar ORDER BY datetime(date_time)')
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showwarning("No Data", "No blood sugar data available.")
        return

    view_window = tk.Toplevel(root)
    view_window.title("View Blood Sugar Data")

    tree = ttk.Treeview(view_window, columns=('Date & Time', 'Blood Sugar Level'), show='headings')
    tree.heading('Date & Time', text='Date & Time')
    tree.heading('Blood Sugar Level', text='Blood Sugar Level (mg/dL)')
    for row in data:
        tree.insert('', tk.END, values=row)
    tree.pack(fill=tk.BOTH, expand=True)


def plot_blood_sugar_data():
    conn = sqlite3.connect('health_tracker.db')
    cursor = conn.cursor()

    cursor.execute('SELECT date_time, level FROM blood_sugar ORDER BY datetime(date_time)')
    data = cursor.fetchall()
    conn.close()

    if not data:
        messagebox.showwarning("No Data", "No blood sugar data available for plotting.")
        return

    df = pd.DataFrame(data, columns=['Date & Time', 'Blood Sugar Level'])
    df['Date & Time'] = pd.to_datetime(df['Date & Time'], format='%m-%d-%Y %H:%M')

    plt.figure()
    plt.plot(df['Date & Time'], df['Blood Sugar Level'], color='purple', marker='o')
    plt.xlabel('Date & Time')
    plt.ylabel('Blood Sugar Level (mg/dL)')
    plt.title('Blood Sugar Level Monitoring')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


root = tk.Tk()
root.title("Blood Sugar Tracker")


tk.Label(root, text="Date (MM-DD-YYYY)").grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Time (HH:MM 24-hour format)").grid(row=1, column=0, padx=5, pady=5)
time_entry = tk.Entry(root)
time_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Blood Sugar Level (mg/dL)").grid(row=2, column=0, padx=5, pady=5)
level_entry = tk.Entry(root)
level_entry.grid(row=2, column=1, padx=5, pady=5)


tk.Button(root, text="Add Data", command=add_blood_sugar_data).grid(row=3, column=0, columnspan=2, pady=5)
tk.Button(root, text="View Data", command=view_blood_sugar_data).grid(row=4, column=0, columnspan=2, pady=5)
tk.Button(root, text="Plot Data", command=plot_blood_sugar_data).grid(row=5, column=0, columnspan=2, pady=5)

root.mainloop()
