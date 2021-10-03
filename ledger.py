from tkinter import filedialog
import pandas as pd
from pandas.errors import EmptyDataError
import os


# Set up ledgers directory
parent_dir = os.getcwd()
ledger_dir = os.path.join(parent_dir, "data\\ledgers")
ledger_filepath = os.path.join(ledger_dir, "transaction_database.csv")
if not os.path.isdir(ledger_dir):
    os.mkdir(ledger_dir) # create folder if non exists
account_dir = os.path.join(parent_dir, "data")

# Initialize ledger variables
ledger_cols = [
    "Account Name",
    "Account Type",
    "Card No",
    "Transaction Date",
    "Posted Date",
    "Description",
    "Category",
    "Sub-category",
    "Amount",
    "MCC",
    "Cashback Reward",
    "Notes"
]

# Define error classes
class Error(Exception):
    # Base class for errors
    pass


class InvalidCharacterError(Error):
    # Raised when input string contains invalid Windows character
    pass


# access accounts.csv to create accounts_df
# accounts_df stores data on credit cards for easy upload
def init_accounts():
    acct_file_path = os.path.join(account_dir, "accounts.csv")
    acct_columns = ["Account Name", "Account Type", "Card No"]
    # creates new account.csv file if none exists
    if not os.path.exists(acct_file_path):
        accounts_df = pd.DataFrame(columns=acct_columns)
        accounts_df.to_csv(acct_file_path)
        print ("New 'accounts.csv' file created")
        return accounts_df
    else:
        with open(acct_file_path) as f:
            accounts_df = pd.read_csv(f, header=0, index_col=0)
        print ("Accounts data imported from 'accounts.csv'")
        return accounts_df

# initialize accounts
accounts_df = init_accounts()

def save_accounts(accounts_df):
    acct_file_path = os.path.join(account_dir, "accounts.csv")
    accounts_df.to_csv(acct_file_path)
    print ("'Accounts.csv' updated!")

def get_account_index(accounts_df, account_name):
    for index, name in accounts_df["Account Name"].iteritems():
        if name == account_name:
            return index


# define methods for manipulating and loading ledger data
class TransactionDatabase():
    def download(self, ledger_df, *args, **kwargs):
        # download data to dataframe
        with open(ledger_filepath) as f:
            df = pd.read_csv(f, index_col=0, header=0)
        ledger_df = ledger_df.append(df)
        print ('Ledger data has been downloaded')

    def save(self, *args, **kwargs):
        # save dataframe to a csv file under ledger filepath
        self.ledger_df.to_csv(ledger_filepath)

    def upload_csv(self, account_index, *args, **kwargs):
        file_name = filedialog.askopenfilename()
        print("Uploading: " + file_name)

        with open(file_name) as f:
            upload_df = pd.read_csv(f, header=0)
        """parse data to match headers so it can be merged with csv
        with different formatting"""
        # adds account data to df
        accounts_df = init_accounts()
        upload_df['Account Name'] = accounts_df.iloc[account_index]["Account Name"]
        upload_df['Account Type'] = accounts_df.iloc[account_index]["Account Type"]
        upload_df['Card No'] = accounts_df.iloc[account_index]["Card No"]
        # cleans amount charged
        if "Amount" not in upload_df.columns:
            # if no amount column, create new column
            # for statements that use debit/credit columns
            upload_df['Credit'] = upload_df.fillna(0)['Credit']
            upload_df['Debit'] = upload_df.fillna(0)['Debit']
            new_amount = upload_df["Credit"] - upload_df["Debit"]
            upload_df["Amount"] = new_amount
        # changes 'category' to 'MCC' for clearer ledger columns
        upload_df = upload_df.rename(columns={"Category": "MCC"})
        # either set credit card account or allow entry

        # change "Post Date" to "Posted Date"
        if "Post Date" in upload_df.columns:
            upload_df["Posted Date"] = upload_df["Post Date"]

        # Cleans upload data for merge
        for col in self.ledger_cols:
            if col not in upload_df.columns:
                # adds missing columns
                upload_df[col] = None
        for col in upload_df.columns:
            if col not in self.ledger_cols:
                # removes unuseds columns
                upload_df = upload_df.drop(columns=col)
        # appends to ledger dataframe
        self.ledger_df = self.ledger_df.append(upload_df, ignore_index=True)
        self.save()

    def __init__(self, ledger_cols):
        self.ledger_cols = ledger_cols
        try:
            self.ledger_df = pd.DataFrame(columns=self.ledger_cols)
            self.download(self.ledger_df)
        except EmptyDataError:
            pass
        except FileNotFoundError:
            self.ledger_df = pd.DataFrame(columns=self.ledger_cols)
            self.ledger_df.to_csv(ledger_filepath)
        print("Ledger initialized.")


def main():
    pass

if __name__ == "__main__":
    main()
