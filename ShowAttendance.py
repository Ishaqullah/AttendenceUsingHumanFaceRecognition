import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
import pandas as pd
import datetime
import os

class AttendanceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Attendance Tracker")
        
        
        self.cal = Calendar(self.root, selectmode='day', date_pattern='yyyy-mm-dd')
        self.cal.pack(pady=10)
        
        
        self.select_btn = ttk.Button(self.root, text="Select Date", command=self.select_date)
        self.select_btn.pack(pady=10)
        
       
        self.table = ttk.Treeview(self.root)
        self.table.pack(pady=10)
        
    def select_date(self):
        selected_date = self.cal.selection_get().strftime('%Y-%m-%d')
        print(f"Selected date: {selected_date}")
        
        
        filename = f"{selected_date}.csv"
        if not os.path.isfile(filename):
            print("File does not exist")
            return
        
        
        df = pd.read_csv(filename)
        df_columns = list(df.columns)
        self.table["columns"] = df_columns
        self.table.column("#0", width=0, stretch=tk.NO)
        for col in df_columns:
            self.table.column(col, anchor=tk.CENTER, width=100)
            self.table.heading(col, text=col, anchor=tk.CENTER)
        for i, row in df.iterrows():
            self.table.insert(parent='', index='end', iid=i, text='', values=list(row))
        
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceGUI(root)
    root.mainloop()
