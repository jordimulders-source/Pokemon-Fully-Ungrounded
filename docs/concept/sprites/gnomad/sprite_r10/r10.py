# Gnomad r10: hele sprite volgens Dragonfly Cave (outline base per kleurvlak, zwart alleen als outline shadow,
# outline highlights aan de binnenkant van de lijn op de meest belichte randen). Bron: ../sprite_r9/gnomad.png.
from analyse import *   # im, a, res (buitenlijnpixels: groep, normaal), T, BASE
SH={'M':{3,2},'H':{7,6},'S':{0xc,0xe},'B':{9}}
out=im.copy(); o=out.load()
def frozen(x,y):  # riem + gesp + hun zwarte lijnen (Machoke-voorbeeld): bevroren
    return 13<=x<=41 and 41<=y<=51 and a[x,y] in (1,0xc,0xd,0xe,0xf)
why={}
# 1. buitenlijn: lichtkant = outline base van het eigen vlak, schaduwkant (onder/rechts) = zwart
for (x,y),(g,nx,ny,d) in res.items():
    if g not in BASE or frozen(x,y): continue
    if d>0.3 or ny>0.6: c=1
    elif d<-0.15: c=BASE[g]
    else:
        ins=[a[x+dx,y+dy] for dx in(-1,0,1) for dy in(-1,0,1) if (dx or dy) and not T(x+dx,y+dy) and (dx*nx+dy*ny)<0 and a[x+dx,y+dy]!=1]
        sh=sum(1 for c_ in ins if c_ in SH[g]); c=1 if ins and sh*2>=len(ins) else BASE[g]
    if c!=a[x,y]: o[x,y]=c; why[(x,y)]='buitenlijn '+g
# 2. handcorrecties
FIX={
 # neus: linker/linksonder lijn op de lichtkant in de eigen donkerroze; onderkant (17..22,33) blijft zwart
 (14,28):6,(14,29):6,(14,30):6,(15,31):6,(16,32):6,
 # losse zwarte pixel rechts van de neus (las als oog, Jordi r1) -> plooi in donkerroze
 (24,31):6,
 # losse zwarte pixels binnen de snor (strengscheiding in licht vlak) -> snor-selout
 (12,34):0xe,(15,37):0xe,
 # linkerhand linksonder: was donkerroze in r9, blijft zo (geen extra zwart op de lichtkant)
 (4,45):6,
 # rechterhand: (44,39) en (42,45) houden hun donkerroze uit r9 (anders zwart/roze om en om op de handrand)
 (44,39):6,(42,45):6,
}
for p,c in FIX.items():
    if o[p]!=c: o[p]=c; why[p]='hand'
    if o[p]==a[p] and p in why: del why[p]
# 3. muts rechterflank: geen afwisseling zwart/donkerlila op één rand -> vanaf x>=47 alles zwart
for (x,y),(g,nx,ny,d) in res.items():
    if g=='M' and x>=47 and y<=33 and o[x,y]==2 and nx>0:
        o[x,y]=1; why[(x,y)]='mutsflank'
        if a[x,y]==1: del why[(x,y)]
# 4. outline highlights (schaduwtint ín de lijn) op de meest belichte randen
OH=[((23,12),3),((24,11),3),((25,11),3),   # muts: top van de bolling linksboven
    ((5,40),7),((4,41),7),                    # linkerhand linksboven
    ((15,54),0xa),((16,54),0xa)]              # linkerschoen bovenkant
import sys
for p,c in OH:
    o[p]=c; why[p]='outline highlight'
out.save('gnomad.png')
if __name__=='__main__':
    for p in sorted(why,key=lambda t:(t[1],t[0])): print(p,'%x->%x'%(a[p],o[p]),why[p])
    op=[(x,y) for y in range(64) for x in range(64) if a[x,y]]
    assert all((a[x,y]==0)==(o[x,y]==0) for y in range(64) for x in range(64))
    b0=sum(a[p]==1 for p in op); b1=sum(o[p]==1 for p in op)
    print(len(why),'gewijzigd; zwart %d->%d (%.1f%% -> %.1f%%)'%(b0,b1,100*b0/len(op),100*b1/len(op)))
