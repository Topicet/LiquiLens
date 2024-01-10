import json

file_path = "C:\\Users\\joebe\\Documents\\Finance\\LiquiLens\\JSON\\transaction_dict.json"

try:
    with open(file_path, "r") as file:
        transactionDict = json.load(file)

except FileNotFoundError:
    transactionDict = {}  # Create an empty dictionary if the file doesn't exist

def add_transaction(description, category):
    transactionDict[description] = category

    # Write the dictionary to the file
    with open(file_path, "w") as file:
        json.dump(transactionDict, file)

        