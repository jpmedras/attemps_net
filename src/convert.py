from submissions import SubmissionList

PATH = "data/"
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

if __name__ == "__main__":
    for file_name in FILE_NAMES:
        s = SubmissionList.from_json(PATH + file_name)
        df = s.to_df()
        df = df.drop(columns=['timestamp', 'lesson_id'])
        df = df.rename(columns={'beginning_timestamp_diff': 'spent_time', 'correct': 'is_correct'})
        df.to_csv(path_or_buf=PATH + file_name.replace('.json', '.csv'), index=False, decimal=',')