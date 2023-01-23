class RegexEngine:
    def isMatch(self, test: str, pattern: str) -> bool:
        self.test = test
        self.pattern = pattern
        self.regex = self.makeRegex()
        return self.match(len(self.regex)-1, len(self.test)-1, -1) and self.match()

    def makeRegex(self):
        regex = []
        for ch in self.pattern:
            if ch == "*":
                regex[-1].star = True
            else:
                regex.append(Rex(ch))
        return regex

    def endOfRegex(self, ir, x):
        if x > 0:
            return all(map(lambda y: y.star, self.regex[ir:]))
        else:
            return all(map(lambda y: y.star, self.regex[:ir+1]))

    def match(self, ir = 0, it = 0, x=1):
        if not 0 <= it < len(self.test) and (not 0 <= ir < len(self.regex) or self.endOfRegex(ir, x)):
            return True
        if not 0 <= it < len(self.test) or not 0 <= ir < len(self.regex):
            return False

        if self.regex[ir].star:
            if self.match(ir+x, it, x):
                return True
            if self.matchChar(ir, it):
                if self.match(ir, it+x, x):
                    return True
                if self.match(ir+x, it+x, x):
                    return True
        elif self.matchChar(ir, it):
            if self.match(ir+x, it+x, x):
                return True
        return False

    def matchChar(self, ir, it):
        return self.regex[ir].char == "." or self.regex[ir].char == self.test[it]

class Rex:
    def __init__(self, character):
        self.char = character
        self.star = False


rengine = RegexEngine()
assert False == rengine.isMatch("aa", "a")
assert True == rengine.isMatch("a", "ab*")
assert True == rengine.isMatch("bbbba", ".*a*a")
assert False == rengine.isMatch("mississippi", "mis*is*p*.")
assert True == rengine.isMatch("aaa", "ab*a*c*a")
assert True == rengine.isMatch("aab", "c*a*b")
assert False == rengine.isMatch("aaaaaaaaaaaaab", "a*a*a*a*a*a*a*a*a*a*c")
assert True == rengine.isMatch("abcaaaaaaabaabcabac", ".*ab.a.*a*a*.*b*b*")
assert True == rengine.isMatch("cbbbaccbcacbcca", "b*.*b*a*.a*b*.a*")
assert True == rengine.isMatch("bcbabcaacacbcabac", "a*c*a*b*.*aa*c*a*a*")
