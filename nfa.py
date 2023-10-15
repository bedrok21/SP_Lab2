class NFA():
    def __init__(self, source: str = None) -> None:
        self.alphabet_card = 0
        self.states_card = 0
        self.transitions = {}
        self.init_state = None
        self.finals_states = frozenset()
        self.states = frozenset()
        self.current_states = frozenset()
        self.last_gen_state = None
        if source is not None:
            self.load(source)

    def load(self, automaton_file): # завантажує автомат з файлу
        with open(automaton_file, mode='r') as file:
            try:
                self.alphabet_card = int(file.readline())
                self.states_card = int(file.readline())
                self.init_state = str(file.readline().split()[0])
                self.states |= frozenset([self.init_state])
                self.current_states = {self.init_state}
                temp_line = file.readline().split()
                for i in range(len(temp_line) - 1):
                    self.finals_states |= frozenset([temp_line[i+1]])
                    self.states |= frozenset([temp_line[i+1]])
                for temp_line in file:
                    temp_line = temp_line.split()
                    self.states |= frozenset([temp_line[0], temp_line[2]])
                    if (temp_line[0], temp_line[1]) in self.transitions.keys():
                        self.transitions[(temp_line[0], temp_line[1])] |= frozenset([(temp_line[2])])
                    else:
                        self.transitions[(temp_line[0], temp_line[1])] = frozenset([(temp_line[2])])
            except Exception as e:
                print(f"Error while loading automaton: {e}")

    def save(self, automaton_file):# зберігає автомат у файл
        with open(automaton_file, mode='w') as file:
            file.write(f"{self.alphabet_card}\n")
            file.write(f"{len(self.states)}\n")
            file.write(f"{self.init_state}\n")
            file.write(f"{len(self.finals_states)} ")
            for fin in self.finals_states:
                file.write(f"{fin} ")
            file.write("\n")
            for rule in self.transitions.keys():
                for transition in self.transitions[rule]:
                    if type(rule[0]) == frozenset:
                        for r in rule[0]:
                            file.write(f"{r} {rule[1]} {transition}")
                            break
                    else:
                        file.write(f"{rule[0]} {rule[1]} {transition}")
                file.write("\n")

    def reset(self): # встановлює поточний стан автомата в початковий
        self.current_state = {self.init_state}

    def process(self, word) -> bool: # приймає на вхід слово і повертає True якщо допускає це слово
        for symbol in word:
            new_states = frozenset()
            proceed = False
            for state in self.current_states:
                if (state, symbol) in self.transitions.keys():
                    new_states = new_states | (self.transitions[(state, symbol)])
                    proceed = True
            if not proceed:
                return False
            self.current_states = new_states
        return self.is_final()

    def is_final(self) -> bool: # повертає True якщо автомат у фінальному стані
        return bool(self.current_states & self.finals_states)

    def gen_state(self) -> str: # генерує новий стан для автомата
        if self.last_gen_state is not None:
            i = self.last_gen_state + 1
        else: i = 1
        while True:
            if 'q' + str(i) not in self.states:
                self.states |= frozenset(['q' + str(i)])
                self.last_gen_state = i
                return 'q' + str(i)
            i+=1


if __name__ == "__main__":
    automaton = NFA('automata') #створюємо об'єкт класу NFA,
                                #автомат завантажується з файлу 'automata'
    while True:
        print("Введіть слово: ")
        word = str(input())         #введення слова користувачем
        if automaton.process(word): #виведення результату
            print("Слово приймається автоматом")
        else: print("Слово не приймається автоматом")
        automaton.reset()
