# Alpaca ronde 17, variant_kop: D2 grotere kop. Basis: ../ (ronde 17).
# Geen herschaling: de kop wordt groter door 2 rijen en 2 kolommen letterlijk te verdubbelen op plekken zonder
# kenmerk, zodat oog, oren, vlechtjes, snuit, neus en mond pixel voor pixel gelijk blijven.
#  - kolom x21 (voorhoofd/wang tussen snuit en oog), rijen <=22: snuit 1 px langer naar links
#  - kolom x29 (achterhoofd achter het oog), rijen <=21: achterhoofd + nabij oor 1 px naar rechts
#  - rij y11 (voorhoofd tussen oorbasis en oog) en rij y19 (bovenlip, onder de neus): kop 2 rijen hoger
# Onderrand van de kop (y22) en de hals blijven staan; de kop groeit naar boven, links en rechts.
# Frame 2 = dezelfde regel als ronde 15-17 (kop y<=22 1 rij lager, hals blijft).
import numpy as np
from fu import *
old,pal=load('alpaca/ronde17'); a=old.copy()
OUT={1,6,10}
f1=old[:64].copy(); H=22
head=f1[:H+1].copy()
# kolom x21 verdubbelen (rijen 0..22): alles links van x21 schuift 1 naar links
h=head.copy(); h[:, :21]=head[:, 1:22]; head=h
# kolom x29 verdubbelen (rijen 0..21): alles rechts van x29 schuift 1 naar rechts
h=head.copy(); h[:H, 30:]=head[:H, 29:-1]; head=h
# rijen 11 en 19 verdubbelen; onderste rij blijft op y22
rows=list(range(0,12))+[11]+list(range(12,20))+[19]+list(range(20,H+1))
stack=head[rows]; assert not stack[:2].any()
newhead=stack[2:]
n1=f1.copy(); n1[:H+1]=newhead
n2=n1.copy(); n2[1:H+2]=n1[0:H+1]; n2[0]=0
a[:64]=n1; a[64:]=n2
zones=[(0,0,0,63,22),(1,0,0,63,23)]
r,outside=report(old,a,zones,OUT); print('\n'.join(r)); assert outside==0
save(a,pal,'alpaca/ronde17','alpaca/ronde17/variant_kop')
