from tkinter import filedialog
import pandas as pd
import os

# only run this code when importing modules
# def main():
#     pass

# if __name__ == "__main__":
#     main()

# Set up ledgers directory
dir_name = "ledgers"
parent_dir = os.getcwd()
ledger_dir = os.path.join(parent_dir, dir_name)
if not os.path.isdir(ledger_dir):
    os.mkdir(ledger_dir)

# create folder if non exists


# Define error classes
class Error(Exception):
    # Base class for errors
    pass


class InvalidCharacterError(Error):
    # Raised when input string contains invalid Windows character
    pass


# define methods for manipulating and loading ledger data
class TransactionDatabase():
    
    def download():
        # download data to dataframe
        print("Code Here")

    def save():
        # 
        print("code here")



    def __init__(self, name):
        self.name = name
        print("Ledger '" + name + "' created.")

    def __str__(self):
        return self.name    # set name of objects


def upload_csv():
    file_name = filedialog.askopenfilename()
    print("Uploading: " + file_name)

    with open(file_name) as f:
        upload_df = pd.read_csv(f, header=0)

def init_ledgers():
    ledgers = []
    for file in os.listdir(ledger_dir):
        ledgers.append(TransactionDatabase(name = file))
    return ledgers

def create_ledger(filename):
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

def select_ledger():
        file_name = filedialog.askopenfilename()
        # Check if valid file then create dataframe of data

        with open(file_name) as f:
            df = pd.read_csv(f, header=0)

# ledgers = create_ledger()
# for ledger in ledgers:
#     print (ledger)
