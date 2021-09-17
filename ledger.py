from tkinter import filedialog
import pandas as pd

class TransactionDatabase():
            
    def upload(self, *args, **kwargs):
        file_name = filedialog.askopenfilename()
        print("Uploading: " + file_name)

        with open(file_name) as f:
            df = pd.read_csv(f, header=0)

    def clean(self, *args, **kwargs):
        print("Code Here")

    def __init__(self, name):
        self.name = name
        print("Hello Ledger! I am " + name)
