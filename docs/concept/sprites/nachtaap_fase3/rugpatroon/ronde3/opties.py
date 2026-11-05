# Rugpatroon ronde 3: banden met de hand als spans per rij (rij: (x_van, x_tot) inclusief).
# Kleur: onderliggende vacht 5/4 -> 13 (band licht), 3 -> 14 (band schaduw); omlijning 1/2 blijft.
from PIL import Image
BASE='../../kleur/ronde7c/nachtaap_fase3.png'
# Optie A: 3 banden in de taal van fase 2: breed (4) aan de rugkant, ')' -boog, taps tot een punt bij de buik.
A = {
 1: {30:(26,28),31:(25,29),32:(26,29),33:(26,29),34:(27,30),35:(27,30),36:(28,30),37:(28,30),38:(28,30),39:(28,30),40:(29,30),41:(29,30),42:(28,29),43:(28,29),44:(28,28)},
 2: {33:(32,32),34:(32,34),35:(32,35),36:(33,36),37:(33,36),38:(34,36),39:(34,36),40:(35,36),41:(35,36),42:(34,35),43:(34,35),44:(34,34),45:(34,34)},
 3: {35:(38,39),36:(38,40),37:(38,41),38:(39,42),39:(39,42),40:(40,42),41:(40,42),42:(40,41),43:(40,41),44:(39,40),45:(39,39)},
}
# Optie B: 3 volle ringen zoals Furret: gelijke breedte 3, ')' -boog, tot de buikomtrek.
B = {
 1: {31:(26,28),32:(26,28),33:(27,29),34:(27,29),35:(27,29),36:(28,30),37:(28,30),38:(28,30),39:(28,30),40:(28,30),41:(28,30),42:(27,29),43:(27,29),44:(27,29),45:(26,28)},
 2: {33:(32,32),34:(32,33),35:(32,34),36:(33,35),37:(33,35),38:(33,35),39:(34,36),40:(34,36),41:(34,36),42:(33,35),43:(33,35),44:(33,35),45:(32,34),46:(32,34)},
 3: {35:(38,38),36:(38,39),37:(38,40),38:(39,41),39:(39,41),40:(40,42),41:(40,42),42:(39,41),43:(39,41),44:(38,40),45:(38,40),46:(37,39)},
}

# Optie C (weggegooid: leest op 1x als wit verband/vest): 2 brede ringen (5 px) zoals de brede banden van Dusclops/Typhlosion: ')' -boog, tot de buikomtrek.
C = {
 1: {30:(26,28),31:(25,29),32:(26,30),33:(26,30),34:(27,31),35:(27,31),36:(28,32),37:(28,32),38:(28,32),39:(28,32),40:(28,32),41:(28,32),42:(27,31),43:(27,31),44:(27,31),45:(26,30)},
 2: {33:(33,33),34:(33,34),35:(33,36),36:(34,37),37:(34,38),38:(35,39),39:(35,39),40:(35,39),41:(35,39),42:(35,39),43:(34,38),44:(34,38),45:(34,38),46:(33,37)},
}
# Onderbeen (dijwortel) begint onder deze lijn: ringen lopen daar onder het been door, niet erop.
def LEG(x,y): return (x>=32 and y>=45) or (x>=37 and y>=44)
MAP={5:13,4:13,3:14}
def maak(spec,out):
    im=Image.open(BASE); a=im.load(); n=0
    for band in spec.values():
        for y,(x0,x1) in band.items():
            for x in range(x0,x1+1):
                if LEG(x,y): continue
                v=a[x,y]
                if v in MAP: a[x,y]=MAP[v]; n+=1
    im.save(out); return n
if __name__=='__main__':
    print('A',maak(A,'optie_A.png')); print('B',maak(B,'optie_B.png'))
