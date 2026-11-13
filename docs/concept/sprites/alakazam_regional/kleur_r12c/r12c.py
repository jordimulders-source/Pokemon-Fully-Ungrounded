# r12c (Claude): rechterbovenarm helemaal grijs van schouder tot elleboog (Jordi: "de rechterbovenarm is nog niet helemaal grijs")
W={}
def p(y,x0,s): W.setdefault(y,[]).append((x0,s))
p(29,35,"aaab"); p(30,35,"abbbc"); p(31,35,"bbbcc"); p(32,35,"bbccc")
p(33,36,"ccccc"); p(34,37,"dd"); p(35,38,"o")
