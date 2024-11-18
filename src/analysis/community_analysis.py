from numpy import mean, std
from pandas import DataFrame

def caracterize_communities(student_analysis_df:DataFrame) -> DataFrame:
    data = {
        'year': [],
        'community': [],
        'n_students': [],
        'student_ids': [],
        'n_students_with_solved_exercises': [],
        'n_solved_exercises': [],
        'solved_exercise_ids': [],
        'mean_ns_solved_exercises': [],
        'std_ns_solved_exercises': [],
        'mean_ns_students_solved_each_exercise': [],
        'std_ns_students_solved_each_exercise': [],
        'mean_means_edge_weights': [],
        'std_means_edge_weights': [],
        'n_tried_exercises': [],
        'tried_exercise_ids': [],
        'mean_ns_tried_exercises': [],
        'std_ns_tried_exercises': [],
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

    for year, year_group in student_analysis_df.groupby(level='year'):
        for name, group in year_group.groupby('community'):
            data["year"].append(year)
            
            data["community"].append(name)

            # IDs dos estudantes da comunidade
            student_ids = group.index.get_level_values('student_id').unique().to_list()
            data["n_students"].append(len(student_ids))
            data["student_ids"].append(student_ids)

            # Números (maiores que zero) de exercícios resolvidos para cada estudante da comunidade
            ns_students_with_solved_exercises = [len(exercise_ids) for exercise_ids in group['solved_exercise_ids'] if len(exercise_ids) > 0]
            data["n_students_with_solved_exercises"].append(len(ns_students_with_solved_exercises))

            # IDs dos exercícios resolvidos de todos os estudantes da comunidade 
            solved_exercise_ids_all = [exercise_id for exercise_ids in group['solved_exercise_ids'] for exercise_id in exercise_ids]
            solved_exercise_ids = list(set(solved_exercise_ids_all))
            data["n_solved_exercises"].append(len(solved_exercise_ids))
            data["solved_exercise_ids"].append(solved_exercise_ids)

            # Números de exercícios resolvidos para cada estudante da comunidade
            ns_solved_exercises = [len(exercise_ids) for exercise_ids in group['solved_exercise_ids']]
            data["mean_ns_solved_exercises"].append(mean(ns_solved_exercises))
            data["std_ns_solved_exercises"].append(std(ns_solved_exercises))

            # Números de estudantes que resolveram cada exercício
            ns_students_solved_each_exercise = [solved_exercise_ids_all.count(exercise_id) for exercise_id in solved_exercise_ids]
            data["mean_ns_students_solved_each_exercise"].append(mean(ns_students_solved_each_exercise))
            data["std_ns_students_solved_each_exercise"].append(std(ns_students_solved_each_exercise))
            
            # Médias dos pesos das arestas de cada um dos estudantes da comunidade
            means_edge_weights = [mean(edge_weights) if len(edge_weights) > 0 else 0 for edge_weights in group['edge_weights'].to_list()]
            data["mean_means_edge_weights"].append(mean(means_edge_weights))
            data["std_means_edge_weights"].append(std(means_edge_weights))

            # IDs dos exercícios tentados dos estudantes da comunidade
            tried_exercise_ids = list(set([exercise_id for exercise_ids in group['tried_exercise_ids'] for exercise_id in exercise_ids]))
            data["n_tried_exercises"].append(len(tried_exercise_ids))
            data["tried_exercise_ids"].append(tried_exercise_ids)

            # Números de exercícios tentados para cada estudante da comunidade
            ns_tried_exercises = [len(exercise_ids) for exercise_ids in group['tried_exercise_ids']]
            data["mean_ns_tried_exercises"].append(mean(ns_tried_exercises))
            data["std_ns_tried_exercises"].append(std(ns_tried_exercises))

            # Número de tentativas de todos os estudantes da comunidade
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
    df = df.set_index(['year', 'community'])

    return df