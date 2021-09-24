from tkinter import filedialog
import pandas as pd
from pandas.errors import EmptyDataError
import os


# Set up ledgers directory
parent_dir = os.getcwd()
ledger_dir = os.path.join(parent_dir, "data\\ledgers")
if not os.path.isdir(ledger_dir):
    os.mkdir(ledger_dir) # create folder if non exists
account_dir = os.path.join(parent_dir, "data")

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
    cleaned_header = [
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
    ledger_df = pd.DataFrame(columns=cleaned_header)

    def download(self, *args, **kwargs):
        # download data to dataframe
        with open(os.path.join(ledger_dir, self.name)) as f:
            df = pd.read_csv(f, index_col=0, header=0)
        self.ledger_df = self.ledger_df.append(df)

    def save(self, *args, **kwargs):
        # save dataframe to a csv file under ledger.name
        path = os.path.join(ledger_dir, self.name)
        self.ledger_df.to_csv(path)

    def upload_csv(self, account_index, *args, **kwargs):
        self.download()
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
            print (upload_df.head(5))
        # changes 'category' to 'MCC' for clearer ledger columns
        upload_df = upload_df.rename(columns={"Category": "MCC"})
        # either set credit card account or allow entry

        # Merge cleaned data with ledger_df
        for col in upload_df.columns:
            if col in self.cleaned_header:
                # cleans unused columns
                self.ledger_df[col] = upload_df[col]
        self.save()

    def __init__(self, name):
        self.name = name
        try:
            with open(os.path.join(ledger_dir, name)) as f:
                df = pd.read_csv(f, index_col=0, header=0)
            self.ledger_df = self.ledger_df.append(df)
        except EmptyDataError:
            pass
        print("Ledger '" + name + "' initialized.")

    def __str__(self):
        return self.name    # set name of objects, don't think it does anything

def init_ledgers():
    '''defines functions to initialize ledgers based on found files'''
    ledgers = []
    active_ledger = None
    for file in os.listdir(ledger_dir):
        ledgers.append(TransactionDatabase(name = file))
    return ledgers

def create_ledger(filename, ledgers):
    """create new object of class Transaction Database with 
    filename defined from tkinter window"""
    
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '.']
    valid_name = True
    try:
        for char in filename:
            if char in invalid_chars:
                raise InvalidCharacterError
    except InvalidCharacterError:
        print ("Error: Selected file name contains invalid character.")
        valid_name = False
    if valid_name == True:
        filename = filename + ".csv"
        filepath = os.path.join(ledger_dir, filename)
        with open(filepath, 'w+') as fp:
            pass
        return TransactionDatabase(name = filename)

def select_ledger():
    '''no longer being used'''
    file_name = filedialog.askopenfilename()
    # Check if valid file then create dataframe of data

    with open(file_name) as f:
        df = pd.read_csv(f, header=0)


def main():
    pass
    # ledgers = init_ledgers()
    # for ledger in ledgers:
    #     ledger.upload_csv()
    #     ledger.save()
    #     # print (ledger)
    #     # ledger.download()
    #     break

if __name__ == "__main__":
    main()
