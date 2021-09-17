import tkinter as tk
from ledger import TransactionDatabase

def main():
    ledger1 = TransactionDatabase("name")
    window = tk.Tk()
    header = tk.Label(text="Budgeting Manager")
    header.pack()
    upload_button = tk.Button(
        window,
        text = "Upload CSV",
        command = ledger1.upload
    )
    upload_button.pack()
    window.mainloop()

if __name__ == "__main__":
    main()
