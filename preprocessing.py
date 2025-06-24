#!/usr/bin/env python3
'''
Preprocessing of cancer dataset
'''

import sys
from json import dump
from pandas import read_excel, cut, get_dummies


def create_transaction(entry):
    return entry[entry == 1].index.to_list()


def process_group(data):
    encoded_data = get_dummies(data)
    transactions = encoded_data.apply(create_transaction, axis=1).to_list()
    return transactions


if __name__ == '__main__':
    min_support = sys.argv[1]
    min_confidence = sys.argv[2]
    max_length = sys.argv[3]

    with open('cancer patient data sets.xlsx', 'rb') as afile:
        data = read_excel(afile)

    data.dropna(axis=0)

    # Removing the patient Id column
    data = data.drop(labels='Patient Id', axis=1)

    # Bucketizing the Age column
    data['Age'] = cut(data['Age'], bins=5)

    data = data.astype(str)
    data['Age'] = data['Age'].str.replace('(', '_')
    data['Age'] = data['Age'].str.replace(']', '_')

    # Grouping data based on Level attribute
    grouped_data = data.groupby(by=['Level'])
    groups = grouped_data.groups.keys()
    grouped_data = grouped_data.apply(process_group).to_list()
    for id, key in enumerate(groups):
        grouped_data[id].append(key)
    grouped_data = [str(item) for item in grouped_data]

    input_data = {
        'transactions': grouped_data,
        'min_support': float(min_support),
        'min_confidence': float(min_confidence),
        'max_length': int(max_length)
    }

    # Saving the JSON file
    with open('./deployment/apriori/demoInput/input.json', 'w') as json_file:
        dump(input_data, json_file)

    sys.exit('Preprocessing is done')
