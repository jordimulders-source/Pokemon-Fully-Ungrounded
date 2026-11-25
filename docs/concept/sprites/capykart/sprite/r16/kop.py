# Kop-lijnen naar Gen 3 (gemeten: viscacha/capybarrel/raticate: lichtkant = donkerste eigen tint, schaduwkant = 1 px schaduwtint + zwart,
# geen dubbele donkerste tint naast zwart; binnenlijn alleen waar vorm over vorm valt, in eigen tint, taps). Tinten van r15b (3 -> D).
KOPLOG=[]
def zet(x,y,n,waarom):
    if G[y,x]!=n: KOPLOG.append(f'({x},{y}) {G[y,x]}->{n} {waarom}'); G[y,x]=n
# a) rechterrand kop/oor: "4 4 1" -> "D 4 1" (één donkere tint vóór de zwarte lijn, zoals viscacha '41' / capybarrel '51')
for y in range(10,30):
    for x in range(33,42):
        if kop[y,x] and G[y,x]==4 and G[y,x+1]==4 and G[y,x+2]==1 and (x,y) not in FACE: zet(x,y,13,'dubbel 4 voor zwart')
# b) kaaklijn r29-30 x30-40: model is daar D (lum 104-117), geen lijn; kop en nek scheiden door de schaduwsikkel zoals in het model
for y in (29,30):
    for x in range(30,41):
        if kop[y,x] and G[y,x]==4 and LUM4[y,x]>=98: zet(x,y,13,f'kaaklijn volgt model (lum {LUM4[y,x]:.0f})')
# c) snuitlijn x18: taps aan de bovenkant (r24 -> D)
if G[24,18]==4: zet(18,24,13,'snuitlijn taps')
