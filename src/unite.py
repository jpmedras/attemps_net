import pandas as pd

YEARS = [2018, 2019, 2021, 2022, 2023]

dfs = []
qs = []
for YEAR in YEARS:
    ANALYSIS_PATH = 'assets/students/' + str(YEAR) + '/' + 'analysis_' + str(YEAR) + '.csv'
    QUESTIONS_PATH = 'assets/students/' + str(YEAR) + '/' + 'questions_' + str(YEAR) + '.csv'

    df = pd.read_csv(ANALYSIS_PATH)
    column = [YEAR for _ in df.index]
    df['year'] = column

    dfs.append(df)

    q = pd.read_csv(QUESTIONS_PATH)
    column = [YEAR for _ in q.index]
    q['year'] = column

    qs.append(q)

df_ = pd.concat(dfs, axis=0)
df_.to_csv('assets/students/carac.csv', decimal=',')

qs_ = pd.concat(qs, axis=0)
qs_.to_csv('assets/students/questiones.csv', decimal=',')