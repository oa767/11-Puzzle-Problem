# The heapq module is used for re-sorting the frontier to assure the state with the smallest
# f-value is at the front. 
import heapq

# The function below reads the initial and goal states from the input file provided and returns
# them both as lists.
def create_states(file_name):

  initial_state = []
  goal_state = []

  with open(file_name) as file:
    for line_number, line in enumerate(file):
      if line_number < 3:
        initial_state.append([int(num) for num in line.split()])
      elif line_number > 3:
        goal_state.append([int(num) for num in line.split()])
 
  return initial_state, goal_state

# The function below creates a copy of a state.
def copy_state(state):

    copy = []

    for y in range(3):
        row = []  
        for x in range(4):
            row.append(state[y][x])
        copy.append(row)
   
    return copy

# The function below checks if the two given states are the same. It returns a boolean.
def same_state(first_state, second_state):

    for y in range(3):
        for x in range(4):
            if first_state[y][x] != second_state[y][x]:
                return False

    return True

# The function below converts a state to a tuple. This is used for checking if a state has been visited or not during the search. 
def state2tuple(state):

    temp_list = []

    for y in range(3):
        for x in range(4):
            temp_list.append(state[y][x])

    result = tuple(temp_list)
    return result

# The function below generates all the possible legal states from a state given.
def get_legal_states(state):
    
    legal_states = []
    index_of_blank_space = (0, 0)
    
    #The two for loops below find the blank space in the state given.
    for y in range(3):
        for x in range(4):
            if state[y][x] == 0:
                index_of_blank_space = (y, x)
   
    if index_of_blank_space[0] > 0: # The if-statement here checks if the blank space is in the top row. If it is, then moving the blank space up is NOT a legal state.
        temp_state = copy_state(state)
        temp_state.append([0, 'Move:', 'Up'])
        temp_state[index_of_blank_space[0] - 1][index_of_blank_space[1]], temp_state[index_of_blank_space[0]][index_of_blank_space[1]] = temp_state[index_of_blank_space[0]][index_of_blank_space[1]], temp_state[index_of_blank_space[0] - 1][index_of_blank_space[1]]
        legal_states.append(temp_state)

    if index_of_blank_space[0] < 2: # The if-statement here checks if the blank space is in the bottom row. If it is, then moving the blank space down is NOT a legal state.
        temp_state = copy_state(state)
        temp_state.append([0, 'Move:', 'Down'])
        temp_state[index_of_blank_space[0] + 1][index_of_blank_space[1]], temp_state[index_of_blank_space[0]][index_of_blank_space[1]] = temp_state[index_of_blank_space[0]][index_of_blank_space[1]], temp_state[index_of_blank_space[0] + 1][index_of_blank_space[1]]
        legal_states.append(temp_state)

    if index_of_blank_space[1] > 0: # The if-statement here checks if the blank space is in the left-most column. If it is, then moving the blank space left is NOT a legal state.
        temp_state = copy_state(state)
        temp_state.append([0, 'Move:', 'Left'])
        temp_state[index_of_blank_space[0]][index_of_blank_space[1] - 1], temp_state[index_of_blank_space[0]][index_of_blank_space[1]] = temp_state[index_of_blank_space[0]][index_of_blank_space[1]], temp_state[index_of_blank_space[0]][index_of_blank_space[1] - 1]
        legal_states.append(temp_state)
   
    if index_of_blank_space[1] < 3: # The if-statement here checks if the blank space is in the right-most column. If it is, then moving the blank space right is NOT a legal state.
        temp_state = copy_state(state)
        temp_state.append([0, 'Move:', 'Right'])
        temp_state[index_of_blank_space[0]][index_of_blank_space[1] + 1], temp_state[index_of_blank_space[0]][index_of_blank_space[1]] = temp_state[index_of_blank_space[0]][index_of_blank_space[1]], temp_state[index_of_blank_space[0]][index_of_blank_space[1] + 1]
        legal_states.append(temp_state)

    return legal_states

# The function below finds the index position of each value in the goal state and returns a list of tuples of the index positions.
# The index position for each value in the goal state can be searched easily by indexing the list returned with the value needed.
# EX: result[5] = (0,2) <<<< (0,2) is the value 5's index position in the goal state.
def get_goal_coordinates(goal_state):
  result = [i for i in range(12)]
  for y in range(3):
    for x in range(4):
      result[goal_state[y][x]] = (y, x)
  return result

# The function below finds the g-value of the current state. In this case, the g-value is the depth level. 
def g(state, initial_state):
  count = 0
  for y in range(3):
    for x in range(4):
      if state[y][x] != initial_state[y][x]:
        count += 1
  return count

# The function below finds the heuristic value of the current state by adding the horizontal and vertical distances between every
# value in the initial state and the goal state.
def h(state, coordinates_list):
    total_distance = 0
    for y in range(3):
        for x in range(4):
            current_distance = abs(coordinates_list[state[y][x]][0] - y) + abs(coordinates_list[state[y][x]][1] - x)
            total_distance += current_distance
    return total_distance

# The function below creates a node which includes a state and its f-value. The nodes are used to keep the frontier in order from the smallest to the biggest f-value.
def create_node(initial_state, coordinates_list, state, W):

    return (g(state, initial_state) + W * h(state, coordinates_list), state)

# The function below is the A* Search algorithm.
def Algorithm(initial_state, goal_state, coordinates_list, W, solution):

  visited_states = set() # Creates an empty set which will include tuples of the states that have already been visited during the search.
  frontier = [] # Creates a frontier that will include all the states that have not been visited.
  frontier.append(create_node(initial_state, coordinates_list, initial_state, W)) # Appends the initial state to the frontier. 
  path = [] # Creates an empty list that will include the states on the path to the optimal solution.
  i = 0

  # The if-statement below checks if the goal state has already been reached from the start.
  if same_state(initial_state, goal_state):
      print("The goal state has already been reached.")
      return True, 1

  while len(frontier) != 0: # A while loop that keeps looping if the frontier is not empty. 
      heapq.heapify(frontier) # The heapq module is used here to re-sort the frontier to assure that all the states are in order of increasing f-value.
      current_node = heapq.heappop(frontier) # The state with the lowest f-value is extracted from the frontier.
      current_state = current_node[1]

      # The if-statement below checks if the goal state has been reached. If it has, the program will
      # track back to the root node, adding the current state and every state to the solution list
      # along the way. It returns a boolean indicating whether a solution has been found and the number
      # of nodes generated.
      if same_state(current_state, goal_state):
          solution.append(current_node)
          j = current_state[3][0]
          while j > 0:
              solution.append(path[j])
              j = path[j][1][3][0]
          solution.append(path[0][1])
          return True, len(frontier) + len(visited_states)
      else:
          # If the goal state has not been reached, the program will add all the current state's
          # legal children to the frontier.
          current_state_tuple = state2tuple(current_state)
          if not(current_state_tuple in visited_states):
              visited_states.add(current_state_tuple)
              path.append(current_node)
              legal_states = get_legal_states(current_state)
              for state in legal_states:
                if not (state2tuple(state) in visited_states):
                  state[3][0] = i
                  frontier.append(create_node(initial_state, coordinates_list, state, W))
              i = i + 1
  return False, 0

# The function below takes a number and returns a nicely formatted string.
def print_nicely(num):
  if (num / 1) == (num // 1):
    return str(int(num))
  else:
    return "{:.1f}".format(num)

def A_Star_Search(file, DEBUG_MODE):

  initial_state, goal_state = create_states(file)
  coordinates_list = get_goal_coordinates(goal_state) # The get_goal_coordinates function is called with the goal state to get the coordinates of every value in the goal state.
  W = float(input("Enter a value for W : ")) # The weight value is inputted from the user here.
  solution = []
  result, number_of_nodes = Algorithm(initial_state, goal_state, coordinates_list, W, solution)
  # The A* Search algorithm is called above with the initial state, goal state, coordinates list, W value, and the solution list. A boolean indicating whether a solution has
  # been found and the number of nodes generated are returned.

  with open("output.txt",'w') as file: # Opens the output file to write.
    
    # The two for loops below output the initial state to the file.
    for y in range(3):
      for x in range(4):
        file.write(str(initial_state[y][x]) + " ")
      file.write("\n")
    file.write("\n")

    if(DEBUG_MODE):
      g_value = g(initial_state, initial_state)
      h_value = h(initial_state, coordinates_list)
      f_value = g_value + h_value
      file.write("G-Value = " + print_nicely(g_value))
      file.write("\n")
      file.write("H-Value = " + print_nicely(h_value))
      file.write("\n")
      file.write("F-Value = " + print_nicely(f_value))
      file.write("\n")
      file.write("\n")
    
    if(DEBUG_MODE):
      # The two for loops below output each node on the solution's path to the file.
      for x in range(len(solution) - 2, 0, -1):
        for i in range(3):
          for j in range(4):
            file.write(str(solution[x][1][i][j]) + " ")
          file.write("\n")
        file.write("\n")
    
        g_value = g(solution[x][1], initial_state) - 1
        h_value = h(solution[x][1], coordinates_list)
        f_value = g_value + h_value
        file.write("G-Value = " + print_nicely(g_value))
        file.write("\n")
        file.write("H-Value = " + print_nicely(h_value))
        file.write("\n")
        file.write("F-Value = " + print_nicely(f_value))
        file.write("\n")
        file.write("\n")

    # The two for loops below output the goal state to the file.
    for y in range(3):
      for x in range(4):
        file.write(str(goal_state[y][x]) + " ")
      file.write("\n")
    file.write("\n")

    if DEBUG_MODE:
      g_value = g(goal_state, initial_state) - 1
      h_value = h(goal_state, coordinates_list)
      f_value = g_value + h_value
      file.write("G-Value = " + print_nicely(g_value))
      file.write("\n")
      file.write("H-Value = " + print_nicely(h_value))
      file.write("\n")
      file.write("F-Value = " + print_nicely(f_value))
      file.write("\n")
      file.write("\n")
    
    file.write(print_nicely(W)) # Outputs the W value to the file.
    file.write("\n")
    file.write(print_nicely(len(solution) - 1)) # Outputs the depth level to the file.
    file.write("\n")
    file.write(print_nicely(number_of_nodes)) # Outputs the number of nodes to the file.
    file.write("\n")

    # The for loop below outputs all the actions from the root node to the goal node.
    for i in range(len(solution) - 2, -1, -1):
      file.write(solution[i][1][3][2][0] + " ")
    file.write("\n")

    #The for loop below outputs all the f-values of the nodes on the solution path.
    file.write(print_nicely(h(solution[-1], coordinates_list) * W + g(solution[-1], initial_state)) + " ")
    for i in range(len(solution) - 2, 0, -1):
      state = solution[i][1]
      if(len(state) > 3):
        state.pop()
      f_value = print_nicely(h(state, coordinates_list) * W + g(state, initial_state) - 1)
      file.write(f_value + " ")
    solution[0][1].pop()
    file.write(print_nicely(h(solution[0][1], coordinates_list) * W + g(solution[0][1], initial_state) - 1) + " ")

# To run the program, put the filename in the first argument of the function.
# The second argument tells the program whether DEBUG_MODE should be on or not.
# If DEBUG_MODE is enabled, the program will additonally output the G, H, and
# F values for every node on the solution path, along wih its state.
A_Star_Search("Input1.txt", False)