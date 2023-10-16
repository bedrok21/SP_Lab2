from nfa import NFA
import copy
import random

def dfa_from_nfa(nfa: NFA) -> NFA:
    dfa = copy.deepcopy(nfa)
    is_nfa = True
    old_transitions = {}
    while is_nfa:
        transitions_to_add = {}
        for transition_rule in dfa.transitions.keys():
            old_transition = dfa.transitions[transition_rule]
            if len(old_transition) > 1:
                if old_transition in old_transitions.values():
                    for key, value in old_transitions.items():
                        if value == old_transition:
                            dfa.transitions[transition_rule] = key
                else:
                    new_state_str = dfa.gen_state()
                    new_state = frozenset([new_state_str])
                    old_transitions[new_state] = old_transition
                    dfa.transitions[transition_rule] = new_state
                    if bool(old_transition & dfa.finals_states): dfa.finals_states |= new_state
                    for rule in dfa.transitions.keys():
                        for old_state in old_transition:
                            if rule[0] == old_state:
                                states_to_add = frozenset()
                                for check_state in dfa.transitions[(rule[0], rule[1])]:
                                    if frozenset([check_state]) in old_transitions.keys():
                                        states_to_add |= old_transitions[frozenset([check_state])]
                                    else:
                                        states_to_add |= frozenset([check_state])
                                if (new_state_str, rule[1]) in transitions_to_add.keys():
                                    transitions_to_add[(new_state_str, rule[1])] |= states_to_add
                                else:
                                    transitions_to_add[(new_state_str, rule[1])] = states_to_add
        is_nfa = False
        for new_rule in transitions_to_add.keys():
            if len(transitions_to_add[new_rule]) > 1: is_nfa = True
            dfa.transitions[new_rule] = transitions_to_add[new_rule]
    return dfa


def generate_random_string(length):
    letters = ['a', 'b', 'c']
    random_string = ''.join(random.choice(letters) for _ in range(length))
    return random_string

def global_test(n, nfa: NFA, dfa: NFA) -> int:
    mathces = 0
    for _ in range(n):
        random_length = random.randint(1, 1000)
        random_word = generate_random_string(random_length)
        if dfa.process(random_word) == nfa.process(random_word):
            mathces += 1
        dfa.reset()
        nfa.reset()
    return mathces


if __name__ == "__main__":

    nfa = NFA('nfa_automaton')
    dfa = dfa_from_nfa(nfa)
    dfa.save('dfa_automaton')

    tests = 10000
    matches = global_test(tests, nfa, dfa)

    print("Кількість тестів: ", tests)
    print(f"Кількість пройдених тестів: {matches} = {round(matches/tests*100)}%")
