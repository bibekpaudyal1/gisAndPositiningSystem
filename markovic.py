# import random

# class MarkovModel:
#     def __init__(self, transitions):
#         self.transitions = transitions
#         self.transition_probabilities = self.calculate_probabilities()

#     def calculate_probabilities(self):
#         probabilities = {}
#         for state, possible_transitions in self.transitions.items():
#             total_transitions = len(possible_transitions)
#             transition_counts = {next_state: (possible_transitions.count(next_state) / total_transitions) * 100
#                                  for next_state in set(possible_transitions)}
#             probabilities[state] = transition_counts
#         return probabilities

#     def predict_next_state(self, current_state):
#         possible_transitions = self.transitions.get(current_state, [])
#         if possible_transitions:
#             probabilities = self.transition_probabilities.get(current_state, {})
#             next_state = random.choices(list(probabilities.keys()), weights=probabilities.values())[0]
#             return next_state
#         else:
#             return None

#     def print_transition_matrix(self):
#         print("Transition Matrix:")
#         for state, probabilities in self.transition_probabilities.items():
#             print(f"From State {state}: {probabilities}")

# # Define transitions between states
# transitions = {
#     0: [1],      # State 0 can transition to 1
#     1: [1, 2, 3, 4],  # State 1 can transition to 1, 2, 3, or 4
#     2: [3],      # State 2 can transition to 3
#     3: [1, 3],   # State 3 can transition to 1 or stay in 3
#     4: [5],      # State 4 can transition to 5 (exit state)
#     5: []        # State 5 is an exit state with no outgoing transitions
# }

# # Create a Markov model with defined transitions
# markov_model = MarkovModel(transitions)

# # Print the transition matrix
# markov_model.print_transition_matrix()

# # Simulate movements starting from the entry point (state 0)
# current_state = 0
# for _ in range(5):  # Simulate 5 movements
#     print(f"Current State: {current_state}")
#     current_state = markov_model.predict_next_state(current_state)

# print("Simulation completed.")




# from flask import Flask, render_template

# app = Flask(__name__)

# class MarkovModel:
#     def __init__(self, transitions):
#         self.transitions = transitions
#         self.transition_probabilities = self.calculate_probabilities()

#     def calculate_probabilities(self):
#         probabilities = {}
#         for state, possible_transitions in self.transitions.items():
#             total_transitions = len(possible_transitions)
#             transition_counts = {next_state: (possible_transitions.count(next_state) / total_transitions) * 100
#                                  for next_state in set(possible_transitions)}
#             probabilities[state] = transition_counts
#         return probabilities

# markov_model = MarkovModel({
#     0: [1],      
#     1: [1, 2, 3, 4],  
#     2: [3],      
#     3: [1, 3],   
#     4: [5],      
#     5: []        
# })

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/page<int:state>')
# def page(state):
#     transition_probabilities = markov_model.transition_probabilities.get(state, {})
#     return render_template('page.html', state=state, probabilities=transition_probabilities)

# if __name__ == '__main__':
#     app.run(debug=True)




from flask import Flask, render_template

app = Flask(__name__)

class MarkovModel:
    def __init__(self, transitions):
        self.transitions = transitions
        self.transition_probabilities = self.calculate_probabilities()

    def calculate_probabilities(self):
        probabilities = {}
        for state, possible_transitions in self.transitions.items():
            total_transitions = len(possible_transitions)
            transition_counts = {next_state: possible_transitions.count(next_state) for next_state in set(possible_transitions)}
            probabilities[state] = {next_state: count / total_transitions for next_state, count in transition_counts.items()}
        return probabilities

markov_model = MarkovModel({
    0: [1],
    1: [1, 2, 3, 4],
    2: [3],
    3: [1, 3],
    4: [5],
    5: []
})

def get_transition_info(state):
    transition_probabilities = markov_model.transition_probabilities.get(state, {})
    return transition_probabilities




def generate_matrix_entry(start_state, end_state):
    states = sorted(set(markov_model.transitions.keys()))
    matrix = []

    for row_state in states:
        transition_info = get_transition_info(row_state)
        row = []
        total_steps = 0
        for col_state in states:
            steps = 0 if col_state not in transition_info else transition_info[col_state]
            row.append(steps)
            total_steps += steps

        row.append(total_steps)
        matrix.append(row)

    return matrix, states





def print_matrix(matrix, states):
    print("Transition Steps Matrix:")
    print("   ", end="")
    for state in states + ["Total Steps"]:
        print(f"{state:<12}", end="")
    print("\n" + "-" * (12 * (len(states) + 1) + 3))

    for i, row in enumerate(matrix):
        print(f"{states[i]}|", end="")
        total_steps = sum(1 for steps in row[:-1] if steps > 0)  # Count non-zero values
        for steps in row[:-1]:  # Exclude the last element (total probability) from the sum
            print(f"{steps:<12}", end="")
        print(f"{total_steps:<12}", end="")
        print("\n" + "-" * (12 * (len(states) + 1) + 3))


def run_program():
    while True:
        start_state = input("Enter the starting position (0 to 5), or 'q' to quit: ")
        
        if start_state.lower() == 'q':
            print("Quitting program.")
            break
        
        end_state = input("Enter the ending position (0 to 5): ")
        
        try:
            start_state = int(start_state)
            end_state = int(end_state)
            
            if 0 <= start_state <= 5 and 0 <= end_state <= 5:
                matrix, steps = generate_matrix_entry(start_state, end_state)
                print_matrix(matrix, steps)
            else:
                print("Invalid input. Please enter numbers from 0 to 5.")
        except ValueError:
            print("Invalid input. Please enter valid numbers or 'q'.")


if __name__ == '__main__':
    run_program()
