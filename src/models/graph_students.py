from models.graph_abc import GraphABC
from networkx import Graph

class GraphStudents(GraphABC):
    def _student_questions(self):
        student_questions = {}

        for s in self._subs:
            if s.student not in student_questions:
                student_questions[s.student] = set()
            
            if s.result:
                student_questions[s.student].add(s.question)

        return student_questions
    
    def _commom_questions(self, student_questions):
        commom = {}

        for student_u, questions_u in student_questions.items():
            for student_v, questions_v in student_questions.items():
                if student_u not in commom:
                    commom[student_u] = {}

                commom[student_u][student_v] = len(questions_u & questions_v)

        return commom
    
    def _student_selections(self, commom_questions, k=0.5):

        selections = {}

        for student_u, students in commom_questions.items():
            student_keys = list(students.keys())
            student_keys.remove(student_u)

            n_questions = students[student_u]

            selected = []

            if n_questions > 0:
                for key in student_keys:
                    if (students[key] / n_questions) >= k:
                        selected.append(key)

            selections[student_u] = selected

        return selections
    
    def _filtered_selecions(self, student_selections):
        filtered_selections = {}
        for student_u, selections in student_selections.items():
            filtered = [student_v for student_v in selections if student_u in student_selections[student_v]]
            filtered_selections[student_u] = filtered

        return filtered_selections

    def to_graph(self, student_prefix:str='S', question_prefix:str='') -> Graph:
        G = Graph()

        student_questions = self._student_questions()
        commom = self._commom_questions(student_questions)
        selections = self._student_selections(commom, k=0.8)
        filtered = self._filtered_selecions(selections)

        opa = []
        for u, selections in filtered.items():
            opa.append(u)
            for v in selections:
                if not G.has_node(u):
                    G.add_node(u)

                if not G.has_node(v):
                    G.add_node(v)

                if not (G.has_edge(u, v) or G.has_edge(v, u)):
                    G.add_edge(u, v, weight=commom[u][v])

        print(len(opa))

        
        # for u in student_questions:
        #     student_node_u = student_prefix + str(u)

        #     for v in student_questions:
        #         student_node_v = student_prefix + str(v)
                
        #         if u != v:
        #             weight = len(set(student_questions[u]) & set(student_questions[v]))

        #             if not g.has_node(student_node_u):
        #                 g.add_node(student_node_u, Size=len(student_questions[u]))

        #             if not g.has_node(student_node_v):
        #                 g.add_node(student_node_v, Size=len(student_questions[v]))

        #             if weight > 0 and not g.has_edge(student_node_u, student_node_v):
        #                 g.add_edge(student_node_u,
        #                         student_node_v,
        #                         Label=f'{weight}')
                    
        return G