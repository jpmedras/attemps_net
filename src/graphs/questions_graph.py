# from models.graph_abc import GraphABC
# from networkx import Graph

# class GraphQuestions(GraphABC):
#     def to_graph(self, student_prefix:str='S', question_prefix:str='') -> Graph:
#         g = Graph()

#         question_students = {}

#         for s in self._subs:
#             if s.question not in question_students:
#                 question_students[s.question] = []

#             if s.result:
#                 question_students[s.question].append(s.student)
        
#         for question_u in question_students:
#             question_node_u = question_prefix + str(question_u)

#             for question_v in question_students:
#                 question_node_v = question_prefix + str(question_v)
                
#                 if question_u != question_v:
#                     weight = len(set(question_students[question_u]) & set(question_students[question_v]))

#                     if not g.has_node(question_node_u):
#                         g.add_node(question_node_u, size=len(question_students[question_u]))

#                     if not g.has_node(question_node_v):
#                         g.add_node(question_node_v, size=len(question_students[question_v]))

#                     if weight > 0 and not g.has_edge(question_node_u, question_node_v):
#                         g.add_edge(question_node_u,
#                                 question_node_v,
#                                 label=f'{weight}')
                    
#         return g

from graphs.graph_abc import GraphABC
from networkx import Graph

class QuestionsGraph(GraphABC):
    def _student_questions(self):
        student_questions = {}

        for s in self._submissions:
            if s.question not in student_questions:
                student_questions[s.question] = set()
            
            if s.result:
                student_questions[s.question].add(s.student)

        return student_questions

    def _commom_students(self, student_questions):
        commom = {}

        for question_u, students_u in student_questions.items():
            for question_v, students_v in student_questions.items():
                if question_u not in commom:
                    commom[question_u] = {}

                commom[question_u][question_v] = len(students_u & students_v)

        return commom

    def to_graph(self) -> Graph:
        G = Graph()

        student_by_question = self._student_questions()
        commom = self._commom_questions(student_by_question)
        
        for u, selections in commom.items():
            for v in selections:
                if not G.has_node(u):
                    G.add_node(u)

                if not G.has_node(v):
                    G.add_node(v)

                if not (G.has_edge(u, v) or G.has_edge(v, u)):
                    G.add_edge(u, v, weight=commom[u][v])
                    
        return G