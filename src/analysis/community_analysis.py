from dataclasses import make_dataclass
from numpy import mean, std
from pandas import DataFrame

StudentClass = make_dataclass("Student", [("student_id", any), ("correct_exercise_ids", list), ("solving_times", list), ("attempted_exercise_ids", list), ("attemping_times", list), ("results", list)])

def caracterize_communities(students_df:DataFrame) -> DataFrame:
    data = {
        'community': [],
        'n_students': [],
        'student_ids': [],
        'n_students_with_correct_exercises': [],
        'n_correct_exercises': [],
        'correct_exercise_ids': [],
        'mean_ns_correct_exercises': [],
        'std_ns_correct_exercises': [],
        'n_attempted_exercises': [],
        'attempted_exercise_ids': [],
        'mean_ns_attempted_exercises': [],
        'std_ns_attempted_exercises': [],
        'n_attemps': [],
        'mean_ns_attemps': [],
        'std_ns_attemps': [],
        'n_correct_attemps': [],
        'mean_ns_correct_attemps': [],
        'std_ns_correct_attemps': [],
        'mean_ps_correct_attemps_min_one': [],
        'std_ps_correct_attemps_min_one': [],
        'mean_mean_solving_times': [],
        'std_mean_solving_times': []
    }

    for name, group in students_df.groupby('community'):
        data["community"].append(name)

        # IDs dos estudantes da comunidade
        student_ids = [student_id for student_id in group.index]
        data["n_students"].append(len(student_ids))
        data["student_ids"].append(student_ids)

        # Números (maiores que zero) de exercícios corretos para cada estudante da comunidade
        ns_students_with_correct_exercises = [len(exercise_ids) for exercise_ids in group['correct_exercise_ids'] if len(exercise_ids) > 0]
        data["n_students_with_correct_exercises"].append(len(ns_students_with_correct_exercises))

        # IDs dos exercícios corretos dos estudantes da comunidade
        correct_exercise_ids = list(set([exercise_id for exercise_ids in group['correct_exercise_ids'] for exercise_id in exercise_ids]))
        data["n_correct_exercises"].append(len(correct_exercise_ids))
        data["correct_exercise_ids"].append(correct_exercise_ids)

        # Números de exercícios corretos para cada estudante da comunidade
        ns_correct_exercises = [len(exercise_ids) for exercise_ids in group['correct_exercise_ids']]
        data["mean_ns_correct_exercises"].append(mean(ns_correct_exercises))
        data["std_ns_correct_exercises"].append(std(ns_correct_exercises))

        # IDs dos exercícios tentados dos estudantes da comunidade
        attempted_exercise_ids = list(set([exercise_id for exercise_ids in group['attempted_exercise_ids'] for exercise_id in exercise_ids]))
        data["n_attempted_exercises"].append(len(attempted_exercise_ids))
        data["attempted_exercise_ids"].append(attempted_exercise_ids)

        # Números de exercícios tentados para cada estudante da comunidade
        ns_attempted_exercises = [len(exercise_ids) for exercise_ids in group['attempted_exercise_ids']]
        data["mean_ns_attempted_exercises"].append(mean(ns_attempted_exercises))
        data["std_ns_attempted_exercises"].append(std(ns_correct_exercises))

        # Número de tentativas e tentivas corretas de todos os estudantes da comunidade
        ns_attemps = [len(results) for results in group['results']]
        data["n_attemps"].append(sum(ns_attemps))
        data["mean_ns_attemps"].append(mean(ns_attemps))
        data["std_ns_attemps"].append(std(ns_attemps))

        # Número de tentativas corretas de todos os estudantes da comunidade
        ns_correct_attemps = [results.count(True) for results in group['results']]
        data["n_correct_attemps"].append(sum(ns_correct_attemps))
        data["mean_ns_correct_attemps"].append(mean(ns_correct_attemps))
        data["std_ns_correct_attemps"].append(std(ns_correct_attemps))
        
        # Porcentagens de tentativas corretas em relação ao total de tentativas para cada estudante da comunidade (se tiver ao menos uma tentativa)
        ps_correct_attemps_min_one = [results.count(True)/len(results) for results in group['results'] if len(results) > 0]
        if len(ps_correct_attemps_min_one) > 0:
            data["mean_ps_correct_attemps_min_one"].append(mean(ps_correct_attemps_min_one))
            data["std_ps_correct_attemps_min_one"].append(std(ps_correct_attemps_min_one))
        else:
            data["mean_ps_correct_attemps_min_one"].append(None)
            data["std_ps_correct_attemps_min_one"].append(None)

        # Médias do tempo de resolução dos exercícios para cada estudante da comunidade (se tiver ao menos um exercício correto)
        means_solving_times = [mean(solving_times) for solving_times in group['solving_times'] if len(solving_times) > 0]
        if len(means_solving_times) > 0:
            data["mean_mean_solving_times"].append(mean(means_solving_times))
            data["std_mean_solving_times"].append(std(means_solving_times))
        else:
            data["mean_mean_solving_times"].append(None)
            data["std_mean_solving_times"].append(None)

    df = DataFrame(data)
    df = df.set_index('community')

    return df