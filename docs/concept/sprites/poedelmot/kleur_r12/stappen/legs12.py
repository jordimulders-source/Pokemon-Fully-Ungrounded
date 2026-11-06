# r12: voorpoten A/B als mouwen onder de kraag, overlap A over B, schaduw onder/achter; middenstuk koel grijs met dunne segmentlijnen
F={}
def put(y,x0,s):
    for i,c in enumerate(s):
        if c!='=': F[(x0+i,y)]=c
# kraagrand + aanzet A/B
put(48,18,"AAAA7A33333")      # 18-22 kraag, 23 B-aanzet links, 24-28 B-bovenlijn
put(49,18,"33A7A")            # A-bovenlijn 18-19, kraagpunt 20-21, B-lijn 22
put(50,16,"AAAA3337")          # A binnen 16-19, aansluitlijn 20-22
put(51,16,"AAA773777AAAA73")  # A: 16-18 licht, 19-20 schaduw, 21 overlap, B 22-24 schaduw (achter A), 25-28 licht, 29-30?
put(52,16,"AA7773777AAA773")
put(53,17,"A7773777A77763")
put(54,18,"776377777663")
# middenstuk (x30-40)
put(48,31,"3373377333")
put(49,31,"8833733663")
put(50,30,"38883776663")
put(51,30,"38883666663")
put(52,30,"38883655563")
put(53,30,"388935")
put(54,30,"88999")
put(55,30,"89999")
put(56,32,"99")
W={}
for (x,y),c in F.items(): W.setdefault(y,[]).append((x,c))
# reparaties na controle
for (x,y),c in {(21,48):'7',(22,48):'7',(21,49):'7',(22,49):'7',(33,48):'A',(29,53):'7',(20,54):'7',(35,52):'5'}.items():
    W.setdefault(y,[]).append((x,c))
