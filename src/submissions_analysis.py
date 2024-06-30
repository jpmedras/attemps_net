from submissions import SubmissionList
import pandas as pd


if __name__ == '__main__':
    YEARS = [2018, 2019, 2021, 2022, 2023]
    OUTPUT_PATH = 'assets/data_analysis.csv'

    data = {
        'year': [],
        'n_submissions': [],
        'n_students': [],
        'n_questions': [],
    }

    for year in YEARS:
        file_path = 'private_data/by_year/' + str(year) + '.json'

        submissions = SubmissionList.from_json(file_path)
        
        data['year'].append(year)
        data['n_submissions'].append(len(submissions))
        data['n_students'].append(len(submissions.get_students()))
        data['n_questions'].append(len(submissions.get_questions()))

    df = pd.DataFrame.from_dict(data)
    df = df.set_index('year')
    df.to_csv(OUTPUT_PATH, decimal=',')