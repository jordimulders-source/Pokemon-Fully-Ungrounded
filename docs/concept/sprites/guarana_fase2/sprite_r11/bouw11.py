# Guarana fase 2, r11 (start r10a; Jordi koos a). Alleen de plekken die Jordi omcirkelde (sprite_r10/jordi_omcirkeld.png):
# "dit zijn plekken waar ogen niet goed zitten of waar de vorm van het fruit niet klopt, waardoor die op afstand niet goed leest.
#  Ook rechtsbovenin de meest rechtse". Per plek: duidelijk oog (rond wit, pupil 2 px, rode schil) of duidelijk ronde vrucht.
# Pupil 2 px (2x1) in ogen van 2 rijen hoog, anders een zwart blok (Jordi eerder: 'Half dicht is prima, dan kan je makkelijker wegkomen met een kleiner pupil').
# Draaien vanuit guarana_fase2/: python3 sprite_r11/bouw11.py
import sys; sys.path.insert(0,'sprite_r9'); import numpy as np; from PIL import Image; from gemeen2 import *
K,L,S,M,H=1,2,3,4,5; l,sg,m,h=6,7,8,9; W=10
def rij(y,x0,s,d):
    for i,c in enumerate(s):
        if c!='_': d[(x0+i,y)]={'.':0,'K':K,'L':L,'S':S,'M':M,'H':H,'l':l,'s':sg,'m':m,'h':h,'W':W}[c]
P={}  # plek -> {(x,y):kleur}
# 1 middelste tros, half dicht oog boven (was L-W-K-W-L: pupil splitste het wit in twee stippen) -> lid, 4x2 wit, pupil linksonder, schil
d={}; rij(16,24,'LLLLLL',d); rij(17,24,'LWWWWL',d); rij(18,24,'LKKWWL',d); rij(19,25,'LLLL',d); P['1 middelste tros: half dicht oog boven']=d
# 2 middelste tros, gat (30,17) leek een oogwit naast (29,17) -> vrucht
P['2 middelste tros: gat rechts van dat oog']={(30,17):M}
# 3 middelste tros, oog M2 (pupil 1 px op de buitenrand, wit 3 px) -> 4x2 wit met pupil 2 px, schil rondom
d={}; rij(19,21,'LLLL',d); rij(20,20,'LWWWWL',d); rij(21,20,'LWKKWL',d); rij(22,21,'LLLL',d); P['3 middelste tros: oog M2']=d
# 4 linkertros, oog L1 (schuin wit, pupil op de buitenlijn) -> 4x2 wit, pupil 2 px, schil
d={}; rij(26,8,'LLLL',d); rij(27,8,'WWWWL',d); rij(28,8,'WKKWL',d); rij(29,9,'LLL',d); P['4 linkertros: oog L1']=d
# 5 linkertros, oog L5 (dun wit om een zwarte klont, raakte oog L4) -> schil boven, wit boven/rechts, pupil 2 px linksonder
d={}; rij(33,16,'LLL',d); rij(34,15,'LWWWW',d); rij(35,15,'LKKW',d); rij(36,15,'LLLK',d); P['5 linkertros: oog L5']=d
# 6 rechtertros boven, oog (pupil in de hoek rechtsboven zonder schil) -> oog tegen de bovenrand, wit 4 breed, pupil 2 px, schil
d={}; rij(21,47,'lll',d); rij(22,47,'LLLL',d); rij(23,45,'MLWWWWL',d); rij(24,45,'MLWKKWL',d); rij(25,47,'LLLL',d); rij(26,48,'LL',d)
P['6 rechtertros: oog boven']=d
# 7 rechtertros, meest rechtse oog R2 (los wit onder de pupil) -> 4x2 wit, pupil 2 px midden (zoals a), schil; (57,24) erbij als buitenlijn
d={}; rij(21,54,'m',d); rij(22,53,'LLLL',d); rij(23,52,'LWWWW',d); rij(24,52,'LWKKWK',d); rij(25,53,'LLLK',d); P['7 rechtertros: meest rechtse oog (R2)']=d
# 8 rechtertros, onderpunt (rafelig, liep in de stam over) -> ronde vrucht: licht linksboven, schaduw rechtsonder, eigen rand
d={}; rij(36,45,'LHHMML',d); rij(37,45,'LHMMSK',d); rij(38,46,'KMSSK',d); rij(39,47,'KKK',d); rij(40,48,'m',d); P['8 rechtertros: onderpunt']=d
if __name__=='__main__':
    o=np.array(Image.open('sprite_r10/guarana2_r10a.png')).astype(int); o0=o.copy()
    for n,d in P.items():
        ch=[(x,y,int(o0[y,x]),v) for (x,y),v in sorted(d.items()) if o0[y,x]!=v]
        for (x,y),v in d.items(): o[y,x]=v
        print(n,len(ch),'px')
    print('totaal anders dan r10a',int((o!=o0).sum()))
    opslaan(o,'sprite_r11/guarana2_r11.png')
    open('sprite_r11/normal.pal','w').write(open('sprite_r10/normal.pal').read())
