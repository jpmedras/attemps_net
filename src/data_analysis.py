from pandas import DataFrame, read_csv
from analysis import attemps_to_solving
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

if __name__ == "__main__":
    YEARS = [2018, 2019, 2021, 2022, 2023]
    DATA_PATH = 'data/'
    INPUT_PATH = DATA_PATH + 'attemps/'
    OUTPUT_PATH = DATA_PATH + 'analysis/'

    attemps_metrics_data = {
        'year': [],
        'n_students': [],
        'n_exercises': [],
        'n_attemps': [],
    }

    exercise_metrics_data = {
        'year': [],
        'exercise_id': [],
        'n_students': [],
        'percentage_students': []
    }

    for year in YEARS:
        attemps_filepath = INPUT_PATH + 'attemps' + '_' + str(year) + '.csv'
        attemps_df = read_csv(attemps_filepath)

        n_students = len(attemps_df['student_id'].unique().tolist())
        n_exercises = len(attemps_df['exercise_id'].unique().tolist())
        n_attemps = len(attemps_df)

        solving_df = attemps_to_solving(attemps_df)

        # Salvando métricas das tentativas

        attemps_metrics_data['year'].append(year)
        attemps_metrics_data['n_students'].append(n_students)
        attemps_metrics_data['n_exercises'].append(n_exercises)
        attemps_metrics_data['n_attemps'].append(n_attemps)

        # Salvando métricas dos exercícios

        for exercise_id, group in solving_df.reset_index().groupby('exercise_id'):
            exercise_metrics_data['year'].append(year)
            exercise_metrics_data['exercise_id'].append(exercise_id)
            exercise_metrics_data['n_students'].append(len(group))
            exercise_metrics_data['percentage_students'].append(len(group)/n_students)
        

    # Exportando dados das métricas das tentativas

    attemps_metrics_filepath = OUTPUT_PATH + 'attemps_metrics.csv'
    attemps_metrics_df = DataFrame(attemps_metrics_data)
    attemps_metrics_df.to_csv(attemps_metrics_filepath, index=False, decimal=',')

    # Exportando dados das métricas das tentativas

    exercise_metrics_filepath = OUTPUT_PATH + 'exercise_metrics.csv'
    exercise_metrics_df = DataFrame(exercise_metrics_data)
    exercise_metrics_df.to_csv(exercise_metrics_filepath, index=False, decimal=',')

    # Exportando gráfico de média para os exercícios de cada ano

    mean_percentage = exercise_metrics_df.groupby('year')['percentage_students'].mean()

    plt.figure(figsize=(8, 6))
    mean_percentage.plot(kind='bar', color='skyblue')

    plt.xlabel('Ano')
    plt.ylabel('Média das porcentagens de estudantes')

    plt.xticks(rotation=0)  # Para exibir os anos horizontalmente

    graphic_bar_filename = 'average_percentage_students_by_year.png'
    plt.savefig(OUTPUT_PATH + graphic_bar_filename, bbox_inches='tight')
    plt.close()

    plt.figure(figsize=(10, 6))

    for year in exercise_metrics_df['year'].unique():
        subset = exercise_metrics_df[exercise_metrics_df['year'] == year]
        
        kde = gaussian_kde(subset['percentage_students'])
        
        x = np.linspace(min(subset['percentage_students']), max(subset['percentage_students']), 1000)
        
        plt.plot(x, kde(x), label=f'Ano {year}')

    plt.xlabel('Porcentagem de Estudantes')
    plt.ylabel('Densidade')

    plt.legend(title='Ano')

    graphic_kde_filename = 'distribution_percentages_by_year.png'
    plt.savefig(OUTPUT_PATH + graphic_kde_filename, bbox_inches='tight')
    plt.close()