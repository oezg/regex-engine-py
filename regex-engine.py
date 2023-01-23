class RegexEngine:
    def isMatch(self, test: str, pattern: str) -> bool:
        self.test = test
        self.pattern = pattern
        self.regex = self.makeRegex()
        return self.match(len(self.regex)-1, len(self.test)-1, True) and self.match()

    def makeRegex(self) -> list["Rex"]:
        regex: list["Rex"] = []
        for ch in self.pattern:
            if ch == "*":
                regex[-1].star = True
            else:
                regex.append(Rex(ch))
        return regex

    def endOfRegex(self, irx: int, back: bool) -> bool:
        if back:
            return all(map(lambda rex: rex.star, self.regex[:irx+1]))
        return all(map(lambda rex: rex.star, self.regex[irx:]))

    def match(self, irx: int = 0, itx: int = 0, back: bool = False) -> bool:
        if not (0 <= itx < len(self.test) or 0 <= irx < len(self.regex)): 
            return True
        if not 0 <= itx < len(self.test) and self.endOfRegex(irx, back):
            return True
        if not (0 <= itx < len(self.test) and 0 <= irx < len(self.regex)):
            return False

        change = -1 if back else 1

        if self.regex[irx].star:
            if self.match(irx + change, itx, back):
                return True
            if self.matchChar(irx, itx):
                if self.match(irx, itx + change, back):
                    return True
                if self.match(irx + change, itx + change, back):
                    return True
        elif self.matchChar(irx, itx):
            if self.match(irx + change, itx + change, back):
                return True
        return False

    def matchChar(self, irx: int, itx: int) -> bool:
        return self.regex[irx].char == "." or self.regex[irx].char == self.test[itx]

class Rex:
    def __init__(self, character: str) -> None:
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
