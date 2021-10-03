# Controls all GUI parameters and classes
import tkinter as tk
import os

from ledger import *


# initialize GUI Errors


# Initialize Transaction Database
ledger_db = TransactionDatabase()


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
            window.destroy()
            # gets account attributes
            accounts_df = init_accounts()
            account_index = get_account_index(accounts_df, account.get())
            ledger_db.upload_csv(account_index)
            # try:
            #     ledger_db.upload_csv(account_index)
            # except AttributeError:
            #     print("No active ledger selected, please select an active ledger")
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
        #Upload CSV button
        upload_button = tk.Button(
            root,
            text = "Upload CSV",
            command = AccountSelectWindow
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