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
            ledger_data.update(new_ledger.name)   # updates to active ledger on creation
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
            active_ledger = filename.get()
            ledger_data.update(active_ledger)

        # set up window objects 
        # checks if any ledger data exists, if not, prompts to create one
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
        def create_bt_cmd():
            # command for create_bt Button instance
            window.destroy()
            CreateLedgerWindow()
        create_bt = tk.Button(
            window,
            text = 'Create New',
            command = create_bt_cmd
        ).pack()


class AccountEntry():
    def update_dataframe(self):
        pass

    def __init__(self):
        window = tk.Toplevel()
        window.geometry("400x300")
        new_name = tk.StringVar(window)
        new_type = tk.StringVar(window)
        new_num = tk.StringVar(window)
        name_label = tk.Label(window, text="Name").grid(row=0, column=0)
        type_label = tk.Label(window, text="Account Type").grid(row=0, column=1)
        num_label = tk.Label(window, text="Card No").grid(row=0, column=2)
        name_entry = tk.Entry(window, textvariable=new_name).grid(row=1, column=0)
        type_entry = tk.Entry(window, textvariable=new_type).grid(row=1, column=1)
        num_entry = tk.Entry(window, textvariable=new_num).grid(row=1, column=2)
        def submit():
            window.destroy()
            accounts_df = init_accounts()
            new_row = pd.Series({
                "Account Name": new_name.get(),
                "Account Type": new_type.get(),
                "Card No": new_num.get()})
            accounts_df = accounts_df.append(new_row, ignore_index=True)
            save_accounts(accounts_df)
            AccountEntry()  # reloads window to enter more
        submit_bt = tk.Button(
            window, text = "Submit", command = submit
        ).grid(row=2, column=0)
        cancel_bt = tk.Button(
            window, text = "Cancel", command=window.destroy
        ).grid(row=2, column=1)

# create "Edit Accounts" window for managing accounts
class EditAccountsWindow():
    def __init__(self):
        window = tk.Toplevel()
        window.geometry("400x300")
        # Initialize accounts
        accounts_df = init_accounts()
        for index, row in accounts_df.iterrows():
            name_label = tk.Label(
                window, text=row["Account Name"], borderwidth=1, relief="solid"
                ).grid(row = index+1, column = 0)
            type_label = tk.Label(
                window, text=row["Account Type"], borderwidth=1, relief="solid"
                ).grid(row = index+1, column = 1)
            num_label = tk.Label(
                window, text=row["Card No"], borderwidth=1, relief="solid"
                ).grid(row = index+1, column = 2)
        def create_acct_btcmd():
            window.destroy()
            AccountEntry()
        create_acct_bt = tk.Button(
            window,
            text = "Create New Account",
            command = create_acct_btcmd
        ).grid(row=0, column=0)


class AccountSelectWindow():
    def __init__(self):
        window = tk.Toplevel()
        account = tk.StringVar(window)
        om = tk.OptionMenu(window, account, *accounts_df["Account Name"]).pack()
        def submit():
            # gets active ledger
            window.destroy()
            active_ledger = ledger_data.return_ledger()
            # gets account attributes
            accounts_df = init_accounts()
            account_index = get_account_index(accounts_df, account.get())
            try:
                upload_df = active_ledger.upload_csv(account_index)
            except AttributeError:
                print("No active ledger selected, please select an active ledger")
        submit_bt = tk.Button(
            window, text = "Submit", command = submit
        ).pack()
            


class ApplicationWindow():
    def __init__(self, root):
        root.geometry("400x300")    # sets window size
        root.title("Budgeting Manager")

        # Upload CSV to ledger button
        # def upload_button_command():
        #     '''includes try/except block to check for no ledger selected'''
        #     # gets active ledger
        #     active_ledger = ledger_data.return_ledger()
        #     # opens account select window
        #     try:
        #         upload_df = active_ledger.upload_csv()
        #     except AttributeError:
        #         print("No active ledger selected, please select an active ledger")
        #     AccountSelectWindow(upload_df = upload_df)
        '''
            col in upload_df.columns:
                if col in self.cleaned_header:
                    # cleans unused columns
                    self.ledger_df[col] = upload_df[col]
            self.save() '''

        upload_button = tk.Button(
            root,
            text = "Upload CSV",
            command = AccountSelectWindow
        ).pack()

        # Change ledger button
        ledger_button = tk.Button(
            root,
            text = "Select Ledger",
            command = SelectLedgerWindow
        ).pack()
        # Edit Accounts button
        edit_accounts_bt = tk.Button(
            root,
            text = "Edit Accounts",
            command = EditAccountsWindow
        ).pack()


def main():
    # root = tk.Tk()
    # app = ApplicationWindow(root)
    # root.mainloop()
    pass

if __name__ == "__main__":
    main()