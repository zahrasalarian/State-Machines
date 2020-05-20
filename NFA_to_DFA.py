# opening the NFA with lambda transitions file
f = open("NFA_input_2.txt","r")
lines = f.readlines()

# getting alphabet
alphabet = lines[0].rstrip().split()

# getting states
nfa_states = lines[1].rstrip().split()

# getting starting state
nfa_starting_state = lines[2].rstrip()

# getting final states
nfa_final_states = lines[3].rstrip().split()

# getting nfa delta
nfa_delta = []
for line in lines[4:]:
    part = line.rstrip().split()
    nfa_delta.append(part)

# closing the file
f.close()

# the function returns next state by taking current state and the move that has been made
def get_next_state(curr_state, move):
    possible_states = []
    for state in nfa_delta:
        # check if the current state and the move are equal to any of the parts of the nfa_delta
        if state[0] == curr_state and state[1] == move:
            possible_states.append(state[2])
    # if no answer is available
    if len(possible_states) == 0:
        return None
    else:
        return possible_states

# ************* transfer from lambda-NFA to NFA without lambda transition ***************

# finds lambda Closure of the given state
def lambda_closure(state):
    # a state is always a part of its lambda_closure
    related_states = [state]

    # Array history is used to prevent duplication
    history = [state]

    # repeat the loop until no new state is added
    while len(history) != 0:

        # get all the states we can go to with a lambda edge
        next_states = get_next_state(history[0], 'Î»')
        # print(next_states)
        if next_states is not None:

            # add every state if it's not in related_states array yet
            for state in next_states:
                if state not in related_states:
                    related_states.append(state)
                    history.append(state)
        history.pop(0)
    return related_states


# returns next states by neutralizing the lambda transitions
def next_state_without_lambda(cur_state,move):
    possible_states = []

    # get lambda_closure of the cur_state
    lambda_cl = lambda_closure(cur_state)
    temp_states = []

    # print(lambda_cl)
    # find next_state of all the members of the lambda_closure when the move has been made
    for state in lambda_cl:
        # print()
        next_states = get_next_state(state, move)
        # print(next_states)
        if next_states is not None:
            for s in next_states:
                if s not in temp_states:
                    temp_states.append(s)

    # find the states that are the lambda_closures of every next_state
    for state in temp_states:
        temp_states = lambda_closure(state)
        if temp_states is not None:
            for s in temp_states:
                if s not in possible_states:
                    possible_states.append(s)
   
    # check if no possible state is available
    if len(possible_states) != 0:
        return possible_states
    else:
        return None



# ************* transfer from NFA without lambda transition to DFA ***************

# assign lambda_closure of starting_state to dfa_starting_state
dfa_starting_state = lambda_closure(nfa_starting_state)

# sorting the array to prevent duplication
dfa_starting_state.sort()

# assign lambda_closure of starting_state to start process from this state
dfa_states = [dfa_starting_state]
dfa_delta = []
dfa_final_states = []

# check if any of final_states are starting_state too and add it
for f in nfa_final_states:
    if f in dfa_starting_state:
        dfa_final_states.append(dfa_starting_state)

# remaining states
re_states = [dfa_starting_state]

# Array history is used to prevent duplication
history = [dfa_starting_state]

# repeat the loop until no new state is added
while len(re_states) != 0 :
    # loop over the letters of the word given to check all of them
    for letter in alphabet:
        states = []
        for re_state in re_states[0]:

            # find all next states by that letter
            next_states = next_state_without_lambda(re_state,letter)
            if next_states is not None:
                for next_state in next_states:
                    if next_state not in states:
                        states.append(next_state)

        # add pre and next states and the move to dfa_delta
        if len(states) != 0:
            dfa_delta.append([re_states[0], letter, states])
            states.sort()

            # check if states was repetitious
            if states not in dfa_states:
                dfa_states.append(states)
                re_states.append(states)

            # add states if they included the final states
            for f_state in nfa_final_states:
                if (f_state in states) and (states not in dfa_final_states):
                    dfa_final_states.append(states)
        else:
            # if no next_state is available it gets stuck in a trap
            dfa_delta.append([re_states[0], letter, 'trap'])
    re_states.pop(0)

# print(dfa_delta)
# print(dfa_final_states)
# print(dfa_starting_state)
# print(dfa_states)
# *********** writing to the txt file **********
f = open("DFA_Output_2.txt","w+")
# alphabet
for s in alphabet:
    f.write(f"{s} ")
f.write('\n')
# states
for st in dfa_states:
    f.write(f"{''.join(list(st))} ")
f.write('\n')
# starting state
f.write(f"{''.join(list(dfa_starting_state))}")
f.write('\n')
# final states
for fs in dfa_final_states:
    f.write(f"{''.join(list(fs))} ")
f.write('\n')
# edges
for state in dfa_delta:
    f.write(f"{''.join(list(state[0]))} {state[1]} {''.join(list(state[2]))}")
    f.write('\n')
f.close()