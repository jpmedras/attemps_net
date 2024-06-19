from models.graph_abc import GraphABC
from networkx import Graph

class GraphSimplified(GraphABC):
    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> Graph:
        g = Graph()

        student_questions = {}
        student_last_times = {}

        for s in self._subs:
            if s.student not in student_questions:
                student_questions[s.student] = {}

            if s.question not in student_questions[s.student]:
                student_questions[s.student][s.question] = []

            if s.student in student_last_times:
                # TODO: Calculate according to timestamp
                student_questions[s.student][s.question].append(s.time)
            else:
                student_questions[s.student][s.question].append(s.time)

            student_last_times[s.student] = s.time

        for student in student_questions:
            student_node = student_prefix + str(student)

            for question in student_questions[student]:
                question_node = question_prefix + str(question)

                g.add_node(student_node, shape='circle')
                g.add_node(question_node, shape='box', fontcolor='white', style='filled', fillcolor='black')

                g.add_edge(student_node,
                        question_node,
                        color='green' if s.result else 'red',
                        sign='+' if s.result else '-',
                        time=s.time,
                        label=f'{sum(student_questions[student][question])}')
                
        return g