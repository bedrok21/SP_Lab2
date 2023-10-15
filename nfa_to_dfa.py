from nfa import NFA
import copy

fake_init = 'q0'
fake_final = {'q2'}
fake_trans = {
    ('q0', '0'): {'q3'},
    ('q3', '0'): {'q3'},
    ('q3', '1'): {'q4'},
    ('q4', '0'): {'q3'},
    ('q4', '1'): {'q0'},
    ('q0', '1'): {'q0'},
    ('q1', '1'): {'q2'}
    }

fake_trans = {
    ('q0', '0'): {'q0', 'q1'},
    ('q0', '1'): {'q0'},
    ('q1', '1'): {'q2'}
}
{
    ('q0', '0'): {'q0', 'q1', 'q2'},
    ('q0', '1'): {'q1', 'q2'},
    ('q1', '0'): {'q0', 'q1'},
    ('q1', '1'): {'q2'},
    ('q2', '0'): {'q0', 'q3'},
    ('q2', '1'): {'q2', 'q3'},
}

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


if __name__ == "__main__":

    nfa = NFA('nfa_automaton')
    dfa = dfa_from_nfa(nfa)
    dfa.save('dfa_automaton')

    #word = '010010011111101'
    #print('dfa:', word, dfa.process(word))
    #print('nfa:', word, nfa.process(word))
