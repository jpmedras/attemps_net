def _unite_pseu_communities(communities):
    to_unite = []
    to_keep = []

    for comminity in communities:
        if len(comminity) == 1:
            to_unite.append(comminity)
        else:
            to_keep.append(comminity)

    merged = set([community for communities in to_unite for community in communities])

    return to_keep + [merged]

def group_communities(df, communities):
    communities = _unite_pseu_communities(communities)

    student_communities = {}
    for idx, community in enumerate(communities):
        for student in community:
            student_communities[student] = idx

    column = [student_communities[student] for student in df.index]
    df['community'] = column

    grouped = df.groupby('community')

    return grouped