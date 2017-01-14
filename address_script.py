import copy
import itertools
import pandas
import ast

from fuzzywuzzy import fuzz

threshold = 60
trade_off = 2
clusters = {}
address_list = []

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
            if cleaned_value not in address_list:
                address_list.append(cleaned_value)
unique_addresses = list(set(address_list))
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
