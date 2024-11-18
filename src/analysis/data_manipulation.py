from pandas import DataFrame

def check_attemps_df(attemps_df:DataFrame) -> bool:
    columns = ['timestamp', 'student_id', 'exercise_id', 'is_correct', 'spent_time']

    if not (sorted(attemps_df.columns) == sorted(columns)):
        raise ValueError('DataFrame is in an unexpected format.')

def check_solving_df(solving_df:DataFrame) -> bool:
    index_names = ['student_id', 'exercise_id']
    columns = ['solving_time']

    if not ((solving_df.index.names == index_names) and (sorted(solving_df.columns) == sorted(columns))):
        raise ValueError('DataFrame is in an unexpected format.')
    
def check_solving_df(trying_df:DataFrame) -> bool:
    index_names = ['student_id', 'exercise_id']
    columns = ['trying_time']

    if not ((trying_df.index.names == index_names) and (sorted(trying_df.columns) == sorted(columns))):
        raise ValueError('DataFrame is in an unexpected format.')

def attemps_to_solving(attemps_df:DataFrame) -> DataFrame:
    
    check_attemps_df(attemps_df)
    
    data = []
    for student_id, group in attemps_df.groupby('student_id'):
        solved_exercises = group.loc[group['is_correct'] == True, 'exercise_id'].unique().tolist()
        
        filtered_group = group[group['exercise_id'].isin(solved_exercises)]
        
        for exercise_id, attempts_group in filtered_group.groupby('exercise_id'):
            solving_time = attempts_group['spent_time'].sum()

            data.append({
                'student_id': student_id,
                'exercise_id': exercise_id,
                'solving_time': solving_time
            })
            
    df = DataFrame(data)
    df = df.set_index(['student_id', 'exercise_id'])

    return df

def attemps_to_trying(attemps_df:DataFrame) -> DataFrame:
    
    check_attemps_df(attemps_df)
    
    data = []
    for student_id, group in attemps_df.groupby('student_id'):
        exercise_ids = group['exercise_id'].unique().tolist()
        solved_exercises = group.loc[group['is_correct'] == True, 'exercise_id'].unique().tolist()
        tried_exercises = [exercise_id for exercise_id in exercise_ids if exercise_id not in solved_exercises]
        
        filtered_group = group[group['exercise_id'].isin(tried_exercises)]
        
        for exercise_id, attempts_group in filtered_group.groupby('exercise_id'):
            trying_time = attempts_group['spent_time'].sum()

            data.append({
                'student_id': student_id,
                'exercise_id': exercise_id,
                'trying_time': trying_time
            })
            
    df = DataFrame(data)
    df = df.set_index(['student_id', 'exercise_id'])

    return df
