import re

#Used for removing simmons payments from USAA data
def regexSearch_Simmons(description):
    return bool(re.search(r'(?i)simmons?', description))

#Used for classifying simmons transaction names.
def simplify_transaction_name(description):
    mapping = {
        'steam': 'Steam',
        '7-eleven': '7-ELEVEN',
        'vapor': 'Vape',
        'amzn': 'Amazon',
        'shell' : 'shellGas',
        'star' : 'vape',
        # Add more mappings as necessary
    }
    
    description = description.lower()
    
    for keyword, simple_name in mapping.items():
        if re.search(keyword, description):
            return simple_name
    
    return keyword