#Handles all the data reading and manipulation tasks. Uses Pandas to categorize transactions and calculate financial metrics.
import os
import pandas as panda
import re
from datetime import datetime
from transactionDictionary import transactionDict


def readBankData(fileName):
    #filePath = os.path.join(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\{datetime.now().strftime('%B')}", fileName)
    filePath = os.path.join(f"C:\\Users\\Nick\\Documents\\Finances\\Main\\Data\\December", fileName)
    return panda.read_csv(filePath)

def categorizeTransactions(bankDataframe):
    bankDataframe = bankDataframe[~bankDataframe['Description'].apply(regexSearch_Simmons)] #Exclude simmons statements from transactions
    bankDataframe = bankDataframe[bankDataframe['Status'] != "Pending"]
    bankDataframe['Category'] = bankDataframe['Description'].apply(lambda x: transactionDict.get(x, "Unknown"))
    return bankDataframe

def calculatePositiveCashFlow(bankDataframe):
    positiveCashFlow = bankDataframe[bankDataframe['Amount'] > 0]['Amount'].sum()
    return round(positiveCashFlow, 2)

def calculateNegativeCashFlow(bankDataframe):
    negativeCashFlow = bankDataframe[bankDataframe['Amount'] < 0]['Amount'].sum()
    return round(negativeCashFlow, 2)

def calculateNetCashFlow(bankDataframe):
    positiveCashFlow = calculatePositiveCashFlow(bankDataframe)
    negativeCashFlow = calculateNegativeCashFlow(bankDataframe)
    netCashFlow = positiveCashFlow + negativeCashFlow
    return round(netCashFlow, 2)

def calculateIncomeToExpenseRatio(bankDataframe):
    positiveCashFlow = calculatePositiveCashFlow(bankDataframe)
    negativeCashFlow = calculateNegativeCashFlow(bankDataframe)
    incomeToExpenseRatio = abs(negativeCashFlow / positiveCashFlow)
    return round(incomeToExpenseRatio, 2)

def processData():
    bankDataframe = readBankData("bk_download(27).csv")
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions_dataframe = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    unknownTransactions_dataframe = categorizedTransactions[categorizedTransactions['Category'] == "Unknown"]

    knownTransactionsDictionaryionary = {}
    unknownTransactionsDictionary = {}

    for index, row in knownTransactions_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']
        category = transactionDict.get(description)

        if category in knownTransactionsDictionaryionary:
            knownTransactionsDictionaryionary[category] += amount
        else:
            knownTransactionsDictionaryionary[category] = amount

    for index, row in unknownTransactions_dataframe.iterrows():
        description = row['Description']
        amount = row['Amount']

        if description in unknownTransactionsDictionary:
            unknownTransactionsDictionary[description] += amount
        else:
            unknownTransactionsDictionary[description] = amount       

    # Sort the known dictionary by value in descending order
    knownTransactionsDictionaryionary = {k: v for k, v in sorted(knownTransactionsDictionaryionary.items(), key=lambda item: item[1], reverse=True)}

    for category, amount in knownTransactionsDictionaryionary.items():
        # Round to 2 decimal places
        knownTransactionsDictionaryionary[category] = round(amount, 2)
    
    return knownTransactionsDictionaryionary, unknownTransactionsDictionary

def createCategoryDataTable():
    bankDataframe = readBankData("bk_download(27).csv")
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]

    positiveCashFlow = calculatePositiveCashFlow(knownTransactions)
    categoriesSum = knownTransactions.groupby('Category')['Amount'].sum().reset_index()
    categoriesSum['Percentage'] = (categoriesSum['Amount'] / positiveCashFlow * 100).round(2)
    categoriesSum = categoriesSum.sort_values(by='Amount', ascending=False)

    categoriesColumns = [{"name": col, "id": col} for col in categoriesSum.columns]

    categoriesData = categoriesSum.to_dict('records')

    return categoriesColumns, categoriesData

def createPositiveCashFlowDictionary():

    bankDataframe = readBankData("bk_download(27).csv")
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    positiveCashFlow = calculatePositiveCashFlow(knownTransactions)

    return {'positiveCashFlow': positiveCashFlow}

def createNegativeCashFlowDictionary():

    bankDataframe = readBankData("bk_download(27).csv")
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    negativeCashFlow = calculateNegativeCashFlow(knownTransactions)

    return {'negativeCashFlow': negativeCashFlow}

def createNetCashFlowDictionary():

    bankDataframe = readBankData("bk_download(27).csv")
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    netCashFlow = calculateNetCashFlow(knownTransactions)

    return {'netCashFlow': netCashFlow}

def createIncomeToExpenseRatioDictionary():

    bankDataframe = readBankData("bk_download(27).csv")
    categorizedTransactions = categorizeTransactions(bankDataframe)

    knownTransactions = categorizedTransactions[categorizedTransactions['Category'] != "Unknown"]
    incomeToExpenseRatio = calculateIncomeToExpenseRatio(knownTransactions)

    return {'incomeToExpenseRatio': incomeToExpenseRatio}

def regexSearch_Simmons(description):
    return bool(re.search(r'(?i)simmons?', description))