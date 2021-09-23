# Controls all GUI parameters and classes
import tkinter as tk
import os

from ledger import *


# initialize GUI Errors
class MissingLedgersError(Exception):
    '''Raises if no ledgers are present'''
    pass

# initialize ledgers and ActiveLedger class to pass active_ledger
class ActiveLedger():
    def __init__(self):
        self.active_ledger = None
        self.ledgers = init_ledgers()
    
    def update(self, active_ledger):
        # changes active_ledger
        self.active_ledger = active_ledger
        print("'" + active_ledger + "' selected as active ledger")
    
    def return_ledger(self):
        # matches ledgers to active ledger and returns instance and methods
        for ledger in self.ledgers:
            if ledger.name == self.active_ledger:
                return ledger

ledger_data = ActiveLedger()   # creates instance to change active ledger


# initializes class for tk window for creating new ledger
class CreateLedgerWindow():
    def __init__(self):
        # creates window with settings
        window = tk.Toplevel()
        window.geometry("400x300")
        label = tk.Label(window, text = "Enter a name for new ledger").pack()

        # creates submit function for new ledger
        filename = tk.StringVar()
        def submit(filename):
            new_filename = filename.get()
            window.destroy()
            # sets new active ledger and calls create function
            new_ledger = create_ledger(new_filename, ledger_data.ledgers)
            ledger_data.ledgers.append(new_ledger)  # updates ledger list to include new ledger
            ledger_data.update(new_filename)   # updates to active ledger on creation
        new_ledger_entry = tk.Entry(window, textvariable=filename).pack()
        submit_bt = tk.Button(
            window,
            text = "Submit",
            command= lambda: submit(filename)
        ).pack()


# open window to select the active ledger
class SelectLedgerWindow():
    def __init__(self):
        window = tk.Toplevel()
        window.geometry("400x300")

        # define function to select active_ledger
        filename = tk.StringVar(window)
        def submit(filename):
            window.destroy()
            # active_ledger = ledgers(name=filename)
            # print (filename.get())
            active_ledger = filename.get()
            ledger_data.update(active_ledger)

        # set up window objects 
        try:
            if len(ledger_data.ledgers) < 1:
                raise MissingLedgersError
            else:
                om = tk.OptionMenu(window, filename, *ledger_data.ledgers).pack()
                submit_bt = tk.Button(
                    window,
                    text = "Submit",
                    command= lambda: submit(filename)
                ).pack()
        except MissingLedgersError:
            # if no ledger found, goes straight to create new ledger
            window.destroy()
            CreateLedgerWindow()
            print ("No ledgers, please create a new ledger")


class ApplicationWindow():
    def __init__(self, root):
        root.geometry("400x300")    # sets window size
        root.title("Budgeting Manager")

        # Upload CSV to ledger button
        def upload_button_command():
            '''includes try/except block to check for no ledger selected'''
            # gets active ledger
            active_ledger = ledger_data.return_ledger()
            try:
                active_ledger.upload_csv()
            except AttributeError:
                print("No active ledger selected, please select an active ledger")
        upload_button = tk.Button(
            root,
            text = "Upload CSV",
            command = upload_button_command
        ).pack()

        # Change ledger button
        ledger_button = tk.Button(
            root,
            text = "Select Ledger",
            command = SelectLedgerWindow
        ).pack()


def main():
    root = tk.Tk()
    app = ApplicationWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()