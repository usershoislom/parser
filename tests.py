from early_algo import *
from unittest import TestCase
class GrammarTests(TestCase):
    def test_non_terminal(self):
        self.assertTrue(is_non_terminal('A'))
        self.assertFalse(is_non_terminal('2'))
        self.assertFalse(is_non_terminal('v'))
        self.assertTrue(is_non_terminal('F'))

    def test_rule(self):
        grammar = Grammar()
        grammar.add_rule('S->AB')
        grammar.add_rule('A->a')
        grammar.add_rule('B->Sa')
        rules = grammar.get_rule()
        self.assertTrue(['S->AB'] in rules)
        self.assertTrue(['A->a'] in rules)
        self.assertTrue(['B->Sa'] in rules)
        self.assertFalse(['B->SA'] in rules)


class UnitTests(TestCase):
    def test_operations(self):
        grammar = Grammar()
        grammar.add_rule('S->aSbS\n')
        grammar.add_rule('S->\n')
        early_parser = Early_algo(grammar)
        word = 'aaabbbababababaaabbb'
        early_parser.init_levels(word)

        self.assertFalse(early_parser.complete(0))  # because all rules are completed   #->*S
        self.assertTrue(early_parser.predict(0))  # New rules: S->*aSbS, S->*_
        self.assertFalse(early_parser.predict(0))  # Not new rules
        self.assertTrue(early_parser.scan(0, word))  # S->a*SbS
        self.assertFalse(early_parser.scan(0, 'b'))  # Not rules to read 'b'
        self.assertTrue(early_parser.predict(1))
        self.assertTrue(early_parser.complete(1))  # S->aS*bS
        self.assertFalse(early_parser.predict(1))  # Not new predicts
        self.assertTrue(early_parser.scan(1, word))  # S->a*(S->*aSbS)SbS
        self.assertFalse(early_parser.scan(1, 'baabbb'))  # Not rules to read 'b'
        self.assertTrue(early_parser.predict(2))
        self.assertTrue(early_parser.complete(2))
        self.assertTrue(early_parser.scan(2, word))  # S->a*(S->a*(S->*aSbS)SbS)SbS
        self.assertFalse(early_parser.scan(3, word))  # predict/complete didn't finish
        self.assertTrue(early_parser.predict(3))
        self.assertTrue(early_parser.complete(3))
        self.assertTrue(early_parser.scan(3, word))  # predict/complete finished themselves work

        self.assertTrue(early_parser.has_word(''))  # True because we have rule #->S* and we can parse empty word
        self.assertTrue(early_parser.has_word(word))


class AlgoTests(TestCase):

    def get_data(self, number):
        filename = 'test/test_' + str(number) + '.txt'
        file = open(filename, 'r')
        grammar = Grammar()
        for line in file:
            grammar.add_rule(line)
        return grammar

    def test_0(self):
        grammar = self.get_data(0)
        self.assertFalse(Early_algo(grammar).has_word("abb"))
        self.assertFalse(Early_algo(grammar).has_word(" "))

    def test_1(self):
        grammar = self.get_data(1)
        self.assertTrue(Early_algo(grammar).has_word("abb"))
        self.assertFalse(Early_algo(grammar).has_word("babba"))
        self.assertTrue(Early_algo(grammar).has_word("ababba"))
        self.assertFalse(Early_algo(grammar).has_word(""))
        self.assertTrue(Early_algo(grammar).has_word("aaabbabbabba"))

    def test_2(self):
        grammar = self.get_data(2)
        self.assertTrue(Early_algo(grammar).has_word("abb"))
        self.assertFalse(Early_algo(grammar).has_word("babba"))
        self.assertFalse(Early_algo(grammar).has_word("ababba"))
        self.assertTrue(Early_algo(grammar).has_word(''))
        self.assertFalse(Early_algo(grammar).has_word("aaabbabbabba"))

    def test_3(self):
        grammar = self.get_data(3)
        self.assertFalse(Early_algo(grammar).has_word("eee"))
        self.assertTrue(Early_algo(grammar).has_word("e"))
        self.assertTrue(Early_algo(grammar).has_word(''))

    def test_4(self):
        grammar = self.get_data(4)
        self.assertTrue(Early_algo(grammar).has_word("adc"))
        self.assertTrue(Early_algo(grammar).has_word("adc"))
        self.assertTrue(Early_algo(grammar).has_word("abadadc"))
        self.assertTrue(Early_algo(grammar).has_word("dddddabadadc"))
        self.assertFalse(Early_algo(grammar).has_word("cdddddabadac"))
        self.assertFalse(Early_algo(grammar).has_word(""))

    def test_5(self):
        grammar = self.get_data(5)
        self.assertTrue(Early_algo(grammar).has_word("ab"))
        self.assertTrue(Early_algo(grammar).has_word("abaabb"))
        self.assertTrue(Early_algo(grammar).has_word(""))
        self.assertFalse(Early_algo(grammar).has_word("a"))

    def test_6(self):
        grammar = self.get_data(6)
        self.assertTrue(Early_algo(grammar).has_word('()()()()()()'))
        self.assertTrue(Early_algo(grammar).has_word('()((())())()'))
        self.assertFalse(Early_algo(grammar).has_word('())'))
        self.assertTrue(Early_algo(grammar).has_word('(((((())))))'))
        self.assertFalse(Early_algo(grammar).has_word('(((()'))
        self.assertTrue(Early_algo(grammar).has_word(''))

    def test_7(self):
        grammar = self.get_data(7)
        self.assertTrue(Early_algo(grammar).has_word('12+15=27'))
        self.assertTrue(Early_algo(grammar).has_word('15+12=27'))
        self.assertFalse(Early_algo(grammar).has_word('1215=27'))
        self.assertFalse(Early_algo(grammar).has_word('1+215='))
        self.assertTrue(Early_algo(grammar).has_word(''))

    def test_8(self):
        grammar = self.get_data(8)
        self.assertTrue(Early_algo(grammar).has_word('ayan_went_to_moscow_yesterday'))
        self.assertFalse(Early_algo(grammar).has_word('ayan_to_moscow_went'))
        self.assertTrue(Early_algo(grammar).has_word('yesterday_ayan_went_to_moscow'))
        self.assertFalse(Early_algo(grammar).has_word('yesterday_ayan_went_moscow'))
        self.assertTrue(Early_algo(grammar).has_word('yesterday_ayan_went_to_moscow.'))
        self.assertTrue(Early_algo(grammar).has_word('ayan_went_to_moscow.'))

    def test_from_lecture(self):
        grammar = self.get_data(9)
        self.assertFalse(Early_algo(grammar).has_word('abb'))
        self.assertTrue(Early_algo(grammar).has_word('aaabbbaaaabbbbaaaaabbbbbaabb'))
        self.assertFalse(Early_algo(grammar).has_word('baaabbbaaaabbbbaaaaabbbbbaabb'))
