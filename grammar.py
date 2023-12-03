CONST_CHAR_ID = 30

def analyze_rules(rule: str) -> list:
    start = rule[:3]
    count = 0
    rules = []
    cur_rule = start
    for i in range(3, len(rule)):
        if rule[i] == ' ' or rule[i] == '\n':
            continue
        else:
            cur_rule += rule[i]
    rules.append(cur_rule)
    count += 1
    return rules


def is_valid_rule(rule: str) -> bool:
    valid = len(rule) > 3 and is_non_terminal(rule[0]) and rule[1] == '-' and rule[2] == '>'
    if not valid:
        return False
    analyze_rules(rule)
    return True


def is_non_terminal(c: str) -> bool:
    return 'A' <= c <= 'Z'


class Grammar:
    _max_char_id = CONST_CHAR_ID
    _size = int()
    _start = str()
    _rules = list()

    class _Iterator:
        char_id = int()
        rule_id = int()
        rules = list()
        _max_char_id = CONST_CHAR_ID

        def get_rule(self):
            return self.rules[self.char_id][self.rule_id]

        def is_valid(self):
            return self._max_char_id > self.char_id >= 0 and \
                   0 <= self.rule_id < len(self.rules[self.char_id])

        def __init__(self, rules, c='A'):
            self.char_id = ord(c) - ord('A')
            self.rule_id = 0
            self.rules = rules

        def __iter__(self):
            return self

        def __next__(self):
            self.rule_id += 1
            if self.rule_id >= len(self.rules[self.char_id]):
                self.rule_id = 0
                self.char_id += 1
                while self.char_id < self._max_char_id and len(self.rules[self.char_id]) == 0:
                    self.char_id += 1
            if not self.is_valid():
                raise StopIteration
            return self.get_rule()

    def __init__(self, start: str = 'S'):
        self._start = start
        self._rules = [[] for _ in range(self._max_char_id)]
        self._size = 0
        self._iter = self.__iter__

    def get_rule(self):
        return self._rules

    def add_rule(self, rule: str) -> bool:
        if is_valid_rule(rule):
            rules_pack = analyze_rules(rule)
            for single_rule in rules_pack:
                self._rules[ord(single_rule[0]) - ord('A')].append(single_rule)
                self._size += 1
            return True
        return False

    def __iter__(self):
        self._iter = self._Iterator(self._rules)
        return self._iter.__iter__()
