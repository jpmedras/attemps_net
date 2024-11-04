from submissions import SubmissionList
from submissions.analysis import solving_times
from pandas import DataFrame, MultiIndex

PATH = "data/attemps/"
FILE_NAMES = [
    "2018_module1.json",
    "2018_module2.json",
    "2018_module3.json",
    "2019_module1.json",
    "2019_module2.json",
    "2019_module3.json",
    "2021_module1.json",
    "2021_module2.json",
    "2021_module3.json",
    "2022_module1.json",
    "2022_module2.json",
    "2022_module3.json",
    "2023_module1.json",
    "2023_module2.json",
    "2023_module3.json"
]

def solving_times_df(df):
    # Criar um dicionário com multi-índice
    solving_time_dict = {}

    for student_id, group in df.groupby("student_id"):
        # Filtrar exercícios corretos e agrupar por exercise_id
        exercicios_corretos = (
            group[group["is_correct"] == True]
            .groupby("exercise_id")["spent_time"]
            .sum()
            .rename("solving_time")
        )

        # Adicionar ao dicionário com multi-índice
        for exercise_id, solving_time in exercicios_corretos.items():
            solving_time_dict[student_id, exercise_id] = {"solving_time": solving_time}

    # Converter o dicionário em um DataFrame com multi-índice
    multi_index_df = DataFrame.from_dict(solving_time_dict, orient='index')
    multi_index_df.index.names = ['student_id', 'exercise_id']

    return multi_index_df

if __name__ == "__main__":
    for file_name in FILE_NAMES:
        attemps_file_name = 'attemps_' + file_name.replace('module', '').replace('.json', '.csv')
        solving_times_file_name = 'solving_times_' + file_name.replace('module', '').replace('.json', '.csv')

        s = SubmissionList.from_json(PATH + file_name)
        df_attemps = s.to_df()
        df_attemps = df_attemps.drop(columns=['timestamp', 'lesson_id'])
        df_attemps = df_attemps.rename(columns={'beginning_timestamp_diff': 'spent_time', 'correct': 'is_correct'})
        # df_attemps.to_csv(path_or_buf=PATH + attemps_file_name, index=False, decimal=',')

        multi_index_df = solving_times_df(df_attemps)
        # multi_index_df.to_csv(path_or_buf=PATH + solving_times_file_name, index=False, decimal=',')
