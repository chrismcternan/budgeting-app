# Controls all GUI parameters and classes
import tkinter as tk
import os

from ledger import *


# initialize GUI Errors
class NoLedgersError(Error):
    # raises when there are no ledgers, and one must be created
    pass


# initialize ledgers and open ledger selection window
ledgers = init_ledgers()
active_ledger = None      # default active_ledger


# initializes class for tk window for creating new ledger
class CreateLedgerWindow():
    def __init__(self):
        window = tk.Toplevel()
        window.geometry("400x300")
        label = tk.Label(window, text = "Enter a name for new ledger").pack()

        # create submit function for new ledger
        filename = tk.StringVar()
        def submit(filename):
            new_filename = filename.get()
            window.destroy()
            # sets new active ledger and calls create function
            active_ledger = create_ledger(new_filename, ledgers)
            print("'" + active_ledger.name + "' selected as active ledger")
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
            for ledger in ledgers:
                if filename.get() == ledger.name:
                    active_ledger = ledger
                    break
            print("'" + active_ledger.name + "' selected as active ledger")

        # set up window objects 
        try:
            if len(ledgers) < 1:
                raise NoLedgersError
            else:
                om = tk.OptionMenu(window, filename, *ledgers).pack()
                submit_bt = tk.Button(
                    window,
                    text = "Submit",
                    command= lambda: submit(filename)
                ).pack()
        except NoLedgersError:
            # if no ledger found, goes straight to create new ledger
            window.destroy()
            CreateLedgerWindow()
            print ("No ledgers, please create a new ledger")


class ApplicationWindow():
    def __init__(self, master=None):
        root = tk.Tk()              # initialize root window
        root.geometry("400x300")    # sets window size
        root.title("Budgeting Manager")
        # Upload CSV to ledger button
        upload_button = tk.Button(
            root,
            text = "Upload CSV",
            command = lambda: active_ledger.upload_csv
        ).pack()
        # Change Ledger button
        ledger_button = tk.Button(
            root,
            text = "Select Ledger",
            command = SelectLedgerWindow
        ).pack()
        # run mainloop
        root.mainloop()


def main():
    app = ApplicationWindow()

if __name__ == "__main__":
    main()