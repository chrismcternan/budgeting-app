# Controls all GUI parameters and classes
import tkinter as tk
import os

from ledger import *

# Creates window for adding a new ledger
def open_create_ledger():
    create_ledger_window = tk.Toplevel()
    create_ledger_window.geometry("400x300")
    label1 = tk.Label(create_ledger_window, text="Create a new ledger").pack()
    filename = tk.StringVar()
    def submit():
        new_filename = filename.get()
        create_ledger_window.destroy()
        create_ledger(new_filename)
    # Initialize Tkinter window
    new_ledger_entry = tk.Entry(create_ledger_window, textvariable=filename).pack()
    submit_bt = tk.Button(create_ledger_window, text="Submit", command=submit).pack()

# Initilize root window for mainloop
def init_root():
    # Initialize Tkinter window
    root = tk.Tk()
    root.geometry("400x300")
    # Header display
    root.title("Budgeting Manager")
    header = tk.Label(root, text="Select a ledger").pack()
    # Upload CSV button
    # upload_button = tk.Button(
    #     window,
    #     text = "Upload CSV",
    #     command = upload_csv()
    # ).pack()
    create_ledger_bt = tk.Button(
        root,
        text = "Create Ledger",
        command = open_create_ledger
    ).pack()
    # Download ledgers button
    dl_ledgers_bt = tk.Button (
        root,
        text = "Download Ledgers",
        command = init_ledgers
    ).pack()
    root.mainloop()

def main():
    init_root()

if __name__ == "__main__":
    main()