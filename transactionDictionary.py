import json

file_path = "C:\\Users\\Nick\\Documents\\Finances\\Main\\JSON\\transaction_dict.json"

try:
    with open(file_path, "r") as file:
        transaction_dict = json.load(file)
except FileNotFoundError:
    transaction_dict = {}  # Create an empty dictionary if the file doesn't exist

def add_transaction(description, category):
    transaction_dict[description] = category

    # Write the dictionary to the file
    with open(file_path, "w") as file:
        json.dump(transaction_dict, file)