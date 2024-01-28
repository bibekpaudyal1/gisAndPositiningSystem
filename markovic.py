import networkx as nx
import matplotlib.pyplot as plt

class MarkovModel:
    def __init__(self, transitions):
        self.transitions = transitions

    def calculate_forward_backward_probabilities(self):
        states = list(self.transitions.keys())

        forward_matrix = [[0.0] * (len(states) + 3) for _ in range(len(states) + 1)]
        backward_matrix = [[0.0] * (len(states) + 3) for _ in range(len(states) + 1)]

        for i, state in enumerate(states):
            forward_matrix[i][0] = state
            backward_matrix[i][0] = state

            for j, next_state in enumerate(states):
                forward_matrix[i][j + 1] = self.transitions[state].count(next_state) / len(self.transitions[state]) if next_state in self.transitions[state] else 0.0
                backward_matrix[i][j + 1] = self.transitions[next_state].count(state) / len(self.transitions[next_state]) if state in self.transitions[next_state] else 0.0

            forward_matrix[i][-2] = sum(forward_matrix[i][1:-2])
            forward_matrix[i][-1] = sum(1 for cell in forward_matrix[i][1:-2] if cell > 0)

            backward_matrix[i][-2] = sum(backward_matrix[i][1:-2])
            backward_matrix[i][-1] = 0  

        forward_matrix[-1][-2] = sum(forward_matrix[i][-2] for i in range(len(states)))
        forward_matrix[-1][-1] = sum(forward_matrix[i][-1] for i in range(len(states)))

    
        total_percentage_backward = [0] * (len(states) + 1)  
        total_steps_backward = 0  

        for j in range(1, len(states) + 1):
            column_values = [backward_matrix[i][j] for i in range(len(states))]
            total_percentage_backward[j] = sum(1 for cell in column_values if cell > 0)
            total_steps_backward += total_percentage_backward[j]

    
        backward_matrix[-1][1:-2] = total_percentage_backward[1:]
        backward_matrix[-1][-2] = total_steps_backward
        backward_matrix[-1][-1] = 0  

        return forward_matrix, backward_matrix


transitions = {
    0: [1],
    1: [1, 2, 3, 4],
    2: [3],
    3: [1, 3],
    4: [],
}

markov_model = MarkovModel(transitions)

start_state = int(input("Enter the starting point: "))
end_state = int(input("Enter the ending point: "))

forward_matrix, backward_matrix = markov_model.calculate_forward_backward_probabilities()

# forward matrix with percentages, total number of steps, and count of probabilities greater than 0
print("Forward Matrix:")
num_rows_greater_than_zero_forward = 0
for row in forward_matrix[:-1]:
    row_str = "\t".join(f"{cell * 100:.2f}%" for cell in row[1:-2])
    total_steps = int(row[-2])
    count_greater_than_zero = int(row[-1])
    if count_greater_than_zero > 0:
        num_rows_greater_than_zero_forward += 1
        row_str += f"\t{total_steps}\t{count_greater_than_zero}"
    print(f"{row[0]}\t{row_str}")


print(" Backward Matrix:")
num_rows_greater_than_zero_backward = 0
for row in backward_matrix:
    row_str = "\t".join(str(cell) for cell in row[1:-2])
    total_steps = int(row[-2])
    if total_steps > 0:
        num_rows_greater_than_zero_backward += 1
        row_str += f"\t{total_steps}"
    print(f"{row[0]}\t{row_str}")

graph_forward = nx.DiGraph()
graph_backward = nx.DiGraph()

for state in transitions.keys():
    graph_forward.add_node(state)
    graph_backward.add_node(state)

for state, next_states in transitions.items():
    for next_state in next_states:
        graph_forward.add_edge(state, next_state)
        graph_backward.add_edge(next_state, state)
layout_forward = nx.spring_layout(graph_forward)
layout_backward = nx.spring_layout(graph_backward)


plt.figure()
nx.draw(graph_forward, pos=layout_forward, with_labels=True, node_color='lightblue', node_size=500, font_size=12, edge_color='gray')
plt.title("Forward Markov Model")


plt.figure()
nx.draw(graph_backward, pos=layout_backward, with_labels=True, node_color='lightcoral', node_size=500, font_size=12, edge_color='gray')
plt.title(" Backward Markov Model")

plt.show()
