import json

years = [2018, 2019, 2021, 2022, 2023]
modules = [1, 2, 3]

path = 'data/by_year_module/'
new_path = 'data/by_year/'

for year in years:
    prefix = path + f'{year}_module'

    subs = []

    for module in modules:
        filepath = prefix + f'{module}.json'

        with open(filepath, 'r') as file:
            s = json.load(file)
            subs += s
    
    new_filepath = new_path + f'{year}.json'
    with open(new_filepath, 'w') as new_file:
        json.dump(subs, new_file, indent=2)