import early_algo
def get_data(filename: str):
    file = open(filename, 'r')
    grammar = early_algo.Grammar()
    for line in file:
        grammar.add_rule(line)
    return grammar

def InitEarlyParser(filename):
    grammar = get_data(filename)
    return early_algo.Early_algo(grammar)


document = input('Please, enter filename with grammar-rules (Example: test.txt):')
if InitEarlyParser(document).has_word(input('Please, enter your word:')):
    print('Yes')
else:
    print('No')
