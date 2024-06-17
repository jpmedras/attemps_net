import json
import pandas as pd

years = [2018, 2019, 2021, 2022, 2023]
modules = [1, 2, 3]

path = 'data/by_year_module/'
new_path = 'data/by_year/'

df_dict = {}
csv_filepath = 'assets/data_analysis.csv'

for year in years:
    prefix = path + f'{year}_module'

    df_dict[year] = []

    for module in modules:
        filepath = prefix + f'{module}.json'

        with open(filepath, 'r') as file:
            s = json.load(file)

            df_dict[year].append(len(s))

    content_filepath = path + f'{year}_module3.json'
    with open(content_filepath, 'r') as content_file:
        content = json.load(content_file)
            
    new_filepath = new_path + f'{year}.json'
    with open(new_filepath, 'w') as new_file:
        for idx, sub in enumerate(content):
            sub['time'] = sub['datediff']
            del sub['datediff']

            content[idx] = sub

        json.dump(content, new_file, indent=2)

    df = pd.DataFrame.from_dict(df_dict, orient='index',
                           columns=['module_1', 'module_2', 'module_3'])
    df.index.name = 'year'
    
    # Module are cumulative
    df['module_3'] = df['module_3'] - df['module_2']
    df['module_2'] = df['module_2'] - df['module_1']

    df['total'] = df.sum(axis=1)
    df.to_csv(csv_filepath)