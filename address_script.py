import copy
import itertools
import pandas
import ast
import nltk
from nltk.tokenize import RegexpTokenizer

from fuzzywuzzy import fuzz

threshold = 60
trade_off = 2
address_set = set()
tokenizer = RegexpTokenizer(r'\w+')

sample_file = pandas.ExcelFile("Return Address Analysis_v15122016.xlsx")
sheets = sample_file.sheet_names
for sheet in sheets:
    curent_sheet = sample_file.parse(sheet)
    try:
        sample_addresses = curent_sheet['Return Address']
    except KeyError:
        sample_addresses = curent_sheet['radd']
    for add in sample_addresses:
        if add:
            try:
                curr_add = ast.literal_eval(add)
            except ValueError:
                continue
            cleaned_value = ''.join(curr_add).encode('ascii', 'ignore').decode('ascii')
            tokenize_data = tokenizer.tokenize(cleaned_value)
            tokenize_value = ' '.join(sorted(tokenize_data))
            address_set.add(tokenize_value)
unique_addresses = list(address_set)
clusters = [unique_addresses[0]]
for address in unique_addresses:
    for cluster in clusters:
        insert_flag = False
        token_ratio = 0
        for clus in cluster:
            token_ratio += fuzz.token_sort_ratio(clus, address)
        if (token_ratio/len(cluster)) > threshold:
            insert_flag = True
            cluster.append(address)
            break
    if not insert_flag:
        clusters.append([address])

# Combinations approach (Slow)
"""
address_combinations = itertools.combinations(unique_addresses, 2)
for address in address_combinations:
    token_ratio = fuzz.token_sort_ratio(address[0], address[1])
    if token_ratio < threshold:
        continue
    if not clusters:
        clusters[str(token_ratio)] = [address]
        continue
    clusters_copy = copy.deepcopy(clusters)
    for key in clusters_copy.keys():
        if token_ratio - trade_off <= int(key) < token_ratio + trade_off:
            if clusters.get(key):
                clusters[key].append(address)
            else:
                clusters[key] = [address]
        else:
            clusters[str(token_ratio)] = [address]
        break
"""
