from pandas import DataFrame, read_csv

if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    INPUT_PATH = 'data/attemps/'
    OUTPUT_PATH = 'data/analysis/'

    data = {
        'year': [],
        'n_attemps': [],
        'n_students': [],
        'n_exercises': [],
    }

    for year in YEARS:
        file_path = INPUT_PATH + 'attemps_' + str(year) + '_3' + '.csv'
        df = read_csv(filepath_or_buffer=file_path)
        
        data['year'].append(year)
        data['n_attemps'].append(len(df.index))
        data['n_students'].append(len(set(df['student_id'].unique().tolist())))
        data['n_exercises'].append(len(set(df['exercise_id'].unique().tolist())))

    df = DataFrame.from_dict(data)
    df = df.set_index('year')
    df.to_csv(OUTPUT_PATH + 'attemps_analysis.csv', decimal=',')