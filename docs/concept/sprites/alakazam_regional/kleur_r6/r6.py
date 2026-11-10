# ronde 6: onderarmen grijs (links x12-20 y34-39, rechts x40-48 y32-37), tapse vingerlijnen, kleine reparaties
W={}
def p(y,x0,s): W.setdefault(y,[]).append((x0,s))
# 1. linkeronderarm grijs (licht linksboven), omlijning blijft
p(34,12,"aabbc"); p(35,12,"abbbcc"); p(36,13,"bbcccccc"); p(37,14,"ccccccc"); p(38,16,"ccccc"); p(39,17,"dddd")
# 1. rechteronderarm grijs (lange horizontale arm), elleboog = lijn x39/40
p(32,47,"b"); p(33,44,"aaab"); p(34,41,"bbbbbbb"); p(35,40,"cccccccc"); p(36,40,"cccccccc"); p(36,48,"d"); p(37,41,"dddddddd")
# 2. vingerlijnen taps
p(39,12,"c"); p(39,14,"c"); p(40,14,"c"); p(32,52,"cc"); p(34,52,"c")
# 3. streep rechteronderarm
for y in (31,32,33,34): p(y,49,"b")
# 4. schoppen links los van de rand
p(39,9,"w")
# 5. glans linkerknie 2x2
p(48,19,"m"); p(47,20,"n")
