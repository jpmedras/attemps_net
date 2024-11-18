from networkx import MultiDiGraph
from pandas import DataFrame

class AttempsMultiDiGraph():
    def __init__(self, attemps_df:DataFrame) -> None:        
        self.__attemps_df = attemps_df

        self.__graph = MultiDiGraph()
        self.__graph.name = 'A'
        
        self.__add_nodes()
        self.__add_edges()
    
    def __add_nodes(self) -> None:
        student_ids = self.__attemps_df['student_id'].unique()
        exercise_ids = self.__attemps_df['exercise_id'].unique()

        for student_id in student_ids:
            self.__graph.add_node(student_id)

        for exercise_id in exercise_ids:
            self.__graph.add_node(exercise_id)
    
    def __add_edges(self) -> None:
        for idx, row in self.__attemps_df.iterrows():
            self.__graph.add_edge(
                row['student_id'],
                row['exercise_id'],
                color=('green' if row['is_correct'] else 'red'),
                label=row['spent_time']
            )

    @property
    def graph(self) -> MultiDiGraph:
        return self.__graph