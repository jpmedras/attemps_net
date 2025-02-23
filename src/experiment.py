from graphs import AttempsMultiGraph, StudentsGraph
from graphs import louvain_grouped_communities, filtering_parameter_analysis
from graphs import add_community_attrs
from analysis import attemps_to_solving, attemps_to_trying
from networkx.algorithms.community import modularity
from pandas import DataFrame, read_csv, concat
from analysis import caracterize_communities
from networkx import write_gml
from scipy.stats import linregress
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import kruskal

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current Axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    # cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    # cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
    cbar = None

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(range(data.shape[1]), labels=col_labels,
                  rotation=-30, ha="right", rotation_mode="anchor")
    ax.set_yticks(range(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("white", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

if __name__ == '__main__':
    DATA_PATH = 'data/'
    INPUT_PATH = DATA_PATH + 'attemps/'
    ANALYSIS_OUTPUT_PATH = DATA_PATH + 'analysis/'
    GRAPHS_OUTPUT_PATH = DATA_PATH + 'graphs/'

    YEARS = [2018, 2019, 2021, 2022, 2023]

    graph_comparison_data = {
        'year': [],
        'n_nodes_a': [],
        'n_edges_a': [],
        'n_nodes_s_g': [],
        'n_edges_s': [],
        'n_edges_g': [],
        'modularity_s': [],
        'modularity_g': [],
        'filtering_parameter': [],
    }

    students_analysis_data = {
        'year': [],
        'student_id': [],
        'community': [],
        'in_pseudocommunity': [],
        'edge_weights': [],
        'n_solved_exercises': [],
        'solved_exercise_ids': [],
        'solving_times': [],
        'n_tried_exercises': [],
        'tried_exercise_ids': [],
        'trying_times': [],
        'results': []
    }

    metrics_correlation_data = []
    metrics_std_data = []

    kruskal_data = []

    for year in YEARS:
        attemps_filepath = INPUT_PATH + 'attemps' + '_' + str(year) + '.csv'
        attemps_df = read_csv(attemps_filepath)

        # Criando DataFrame de exercícios resolvidos

        solving_df = attemps_to_solving(attemps_df=attemps_df)

        # Criando DataFrame de exercícios tentados

        trying_df = attemps_to_trying(attemps_df=attemps_df) 

        # Criando grafo A

        graph_a = AttempsMultiGraph(attemps_df=attemps_df).graph

        # Criando grafo S

        graph_s_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'graph_s' + '.gml'
        graph_s = StudentsGraph(solving_df=solving_df).graph
        graph_s_communities, s_pseudocommunity_idx = louvain_grouped_communities(graph_s, weight='weight')
        graph_s_modularity = modularity(graph_s, communities=graph_s_communities)

        add_community_attrs(graph_s, graph_s_communities)
        write_gml(graph_s, graph_s_filepath)

        # Calculando parâmetro de filtragem

        filtering_parameter_df = filtering_parameter_analysis(solving_df=solving_df)
        filtering_parameter_filepath = ANALYSIS_OUTPUT_PATH + str(year) + '_' + 'filtering_parameter.csv'
        filtering_parameter_df.to_csv(filtering_parameter_filepath, index=False, decimal=',')
        filtering_parameter = float(filtering_parameter_df.loc[filtering_parameter_df['criterion'] == filtering_parameter_df['criterion'].min(), 'filtering_parameter'].squeeze())

        # Criando grafo G
        
        graph_g_filepath = GRAPHS_OUTPUT_PATH + str(year) + '_' + 'graph_g' + '.gml'
        graph_g = StudentsGraph(solving_df=solving_df, filtering_parameter=filtering_parameter).graph
        graph_g_communities, g_pseudocommunity_idx = louvain_grouped_communities(graph_g, weight='weight')
        graph_g_modularity = modularity(graph_g, communities=graph_g_communities)

        add_community_attrs(graph_g, graph_g_communities)
        write_gml(graph_g, graph_g_filepath)

        # Adicionando dados de comparação entre os grafos

        graph_comparison_data['year'].append(year)
        graph_comparison_data['n_nodes_a'].append(len(graph_a.nodes()))
        graph_comparison_data['n_edges_a'].append(len(graph_a.edges()))
        graph_comparison_data['n_nodes_s_g'].append(len(graph_s.nodes))
        graph_comparison_data['n_edges_s'].append(len(graph_s.edges))
        graph_comparison_data['n_edges_g'].append(len(graph_g.edges))
        graph_comparison_data['modularity_s'].append(graph_s_modularity)
        graph_comparison_data['modularity_g'].append(graph_g_modularity)
        graph_comparison_data['filtering_parameter'].append(filtering_parameter)

        # Adicionando dados de análise dos estudantes

        for student_id, group in attemps_df.groupby('student_id'):
            for idx, community in enumerate(graph_g_communities):
                if student_id in community:
                    community_id = idx
                    break

            if community_id == g_pseudocommunity_idx:
                in_pseudocommunity = True
            else:
                in_pseudocommunity = False

            edge_weights = [data['weight'] for u, v, data in graph_g.edges(data=True) if (u == student_id or v == student_id)]

            solved_group = solving_df.loc[solving_df.index.get_level_values('student_id') == student_id]
            solved_exercise_ids = solved_group.index.get_level_values('exercise_id').unique().to_list()
            solving_times = solved_group['solving_time'].to_list()

            tried_group = trying_df.loc[trying_df.index.get_level_values('student_id') == student_id]
            tried_exercise_ids = tried_group.index.get_level_values('exercise_id').unique().to_list()
            trying_times = tried_group['trying_time'].to_list()

            results = group['is_correct'].to_list()

            students_analysis_data['year'].append(year)
            students_analysis_data['student_id'].append(student_id)
            students_analysis_data['community'].append(community_id)
            students_analysis_data['in_pseudocommunity'].append(in_pseudocommunity)
            students_analysis_data['edge_weights'].append(edge_weights)
            students_analysis_data['n_solved_exercises'].append(len(solved_exercise_ids))
            students_analysis_data['solved_exercise_ids'].append(solved_exercise_ids)
            students_analysis_data['solving_times'].append(solving_times)
            students_analysis_data['n_tried_exercises'].append(len(tried_exercise_ids))
            students_analysis_data['tried_exercise_ids'].append(tried_exercise_ids)
            students_analysis_data['trying_times'].append(trying_times)
            students_analysis_data['results'].append(results)

    # Salvando dados da análise dos estudantes

    students_analysis_filepath = ANALYSIS_OUTPUT_PATH + 'students_analysis' + '.csv'
    students_analysis_df = DataFrame(students_analysis_data)

    community_size = students_analysis_df.groupby(['year', 'community']).size().reset_index(name="count")
    community_size = community_size.sort_values(by=["year", "count"], ascending=[True, False])
    community_size["community_letter"] = community_size.groupby("year").cumcount().apply(lambda x: chr(ord('A') + x))
    students_analysis_df = students_analysis_df.merge(community_size[["year", "community", "community_letter"]], on=["year", "community"])

    columns = ['community', 'community_letter']
    students_analysis_df = students_analysis_df[columns + [c for c in students_analysis_df.columns if c not in columns]]

    students_analysis_df = students_analysis_df.sort_values(['year', 'community_letter'])
    students_analysis_df = students_analysis_df.set_index(['year', 'student_id'])

    community_metric_names = ['n_solved_exercises', 'n_attemps', 'mean_edge_weights', 'mean_solving_times']
    community_metric_nicknames = ['Ex. Res.', 'Tent.', 'Peso M. das Ar.', 'Tempo M. de Res.']

    groups = []
    for year, group in students_analysis_df.groupby('year'):

        group['n_attemps'] = [len(r) for r in group['results']]
        group['mean_edge_weights'] = [np.mean(e) if len(e) > 0 else 0 for e in group['edge_weights']]
        group['mean_solving_times'] = [np.mean(s) if len(s) > 0 else None for s in group['solving_times']]       

        groups.append(group)
    students_analysis_df = concat(groups)
    students_analysis_df.to_csv(students_analysis_filepath, decimal=',')

    # Salvando dados da análise das comunidades

    communities_analysis_filepath = ANALYSIS_OUTPUT_PATH + 'communities_analysis' + '.csv'
    communities_analysis_df = caracterize_communities(students_analysis_df)
    communities_analysis_df.to_csv(communities_analysis_filepath, decimal=',')    

    # Salvando dados do teste de Kruskal-Wallis e box plot
    
    fig, axs = plt.subplots(nrows=len(YEARS), ncols=len(community_metric_names), figsize=(10, 10), sharey=True)

    for i, (year, group) in enumerate(students_analysis_df.groupby('year')):

        data = {
            'year': year
        }

        for j, metric in enumerate(community_metric_names):
            community_data = group.groupby('community_letter')[metric].apply(list).to_numpy()

            kruskal_test = kruskal(*community_data, nan_policy='omit')
            data[metric] = kruskal_test.pvalue

            axs[i, j].boxplot(community_data, labels=group['community_letter'].unique())
            if i == 0:
                axs[i, j].set_title(community_metric_nicknames[j], fontsize=10)

        kruskal_data.append(data)

    kruskal_filepath = ANALYSIS_OUTPUT_PATH + 'kruskal' + '.csv'
    kruskal_df = DataFrame(kruskal_data).set_index('year')
    kruskal_df.to_csv(kruskal_filepath, decimal=',')

    for ax in axs.flat:
        ax.set_yticklabels([])
    
    fig.tight_layout()
    fig.subplots_adjust(hspace=0.4)
    fig.subplots_adjust(left=0.07)

    for i, year in enumerate(YEARS):
        fig.text(
            x=0.05  ,  # Posição na horizontal (mais para a esquerda)
            y=1 - (i + 0.5) / len(YEARS),  # Posição vertical centralizada na linha
            s=str(year),  # Texto do ano
            ha='right',  # Alinhamento do texto à direita
            va='center',  # Alinhamento vertical ao centro
            fontsize=10,  # Tamanho da fonte
            fontweight='bold'
        )

    box_filepath = ANALYSIS_OUTPUT_PATH + 'box_plot' + '.png'
    plt.savefig(box_filepath)
    plt.close()

    # Salvando dados da correlações entre métricas das comunidades

    metrics_correlation_filepath = ANALYSIS_OUTPUT_PATH + 'metrics_correlation' + '.csv'
    main_metric_name = 'mean_ns_solved_exercises'
    other_metric_names = ['mean_ns_attemps', 'mean_means_edge_weights', 'mean_mean_solving_times']
    short_other_metric_names = ['Tent.', 'Peso M. das Ar.', 'Tempo M. de Res.']

    for year, group in communities_analysis_df.groupby('year'):

        main_metric = group[main_metric_name].to_list()

        data = {
            'year': year
        }

        for other_metric_name in other_metric_names:
            other_metric = group[other_metric_name].to_list()
            r = linregress(main_metric, other_metric).rvalue

            data['r-squared' + '_' + main_metric_name + '_' + other_metric_name] = r

        metrics_correlation_data.append(data)
    
    metrics_correlation_df = DataFrame(metrics_correlation_data).set_index('year')
    metrics_correlation_df.to_csv(metrics_correlation_filepath, decimal=',')

    # Salvando dados de correlação entre métricas das comunidades em um heatmap

    correlation_array = metrics_correlation_df.to_numpy().T

    fig, ax = plt.subplots()
    im, cbar = heatmap(correlation_array, short_other_metric_names, YEARS, ax=ax,
                    cmap="PRGn")
    texts = annotate_heatmap(im)

    metrics_correlation_heatmap_filepath = ANALYSIS_OUTPUT_PATH + 'metrics_correlation_heatmap' + '.png'
    fig.tight_layout() 
    plt.savefig(metrics_correlation_heatmap_filepath)
    plt.close()

    # Salvando dados de desvios-padrão médio das métricas das comunidades

    metrics_std_filepath = ANALYSIS_OUTPUT_PATH + 'metrics_std' + '.csv'
    for year, group in communities_analysis_df.groupby('year'):
        metrics_names = ['ns_solved_exercises', 'ns_attemps', 'means_edge_weights', 'mean_solving_times']

        data = {
            'year': year
        }

        for metric_name in metrics_names:
            metric = group['std' + '_' + metric_name].to_list()
            value = np.std(metric)

            data['mean_stds' + '_' + metric_name] = value

        metrics_std_data.append(data)
    
    metrics_std_df = DataFrame(metrics_std_data).set_index('year')
    metrics_std_df.to_csv(metrics_std_filepath, decimal=',')

    # Salvando dados da comparação entre os grafos

    graph_comparison_filepath = ANALYSIS_OUTPUT_PATH + 'graph_comparison.csv'
    graph_comparison_df = DataFrame(graph_comparison_data)
    graph_comparison_df.to_csv(graph_comparison_filepath, index=False, decimal=',')
