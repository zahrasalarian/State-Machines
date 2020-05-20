import sys
# opening the DFA file
f = open("DFA_input_1.txt","r")
lines = f.readlines()

# getting alphabet
alphabet = lines[0].rstrip().split()

# getting states
dfa_states = lines[1].rstrip().split()

# getting starting state
dfa_starting_state = lines[2].rstrip()

# getting final states
dfa_final_states = lines[3].rstrip().split()

# getting dfa delta
dfa_delta = []
for line in lines[4:]:
    part = line.rstrip().split()
    dfa_delta.append(part)

# closing the file
f.close()

# get the word out for testing
w = input()

# assign starting_state to start testing from this state
state = dfa_starting_state

# loop over the letters of the word given to check all of them
for letter in w:
    # check if the letter is in the alphabet of the dfa machine
    if letter in alphabet:
        for part in dfa_delta:
            # check if the current state and the move are equal to any of the parts of the dfa_delta
            if part[0] == state and part[1] == letter:
                # if true the letter is accepted and we go to the next state and move on to the next letter
                state = part[2]
                break
    else:
        # if it's not, we finish testing and inform the user of the authorized letters
        print("sorry, some letters of the word you have entered are not in the alphabet of the dfa machine")
        print(f"you can only use these lettes: {','.join(list(alphabet))} ")
        sys.exit()

# check if the last state that we are in after the loop is finished was a member of the final_states of the dfa machine
if state in dfa_final_states:
    # if yes it's accepted
    print("yes, it is accepted")
else:
    # if not it's not accepted
    print("no, it is not accepted")