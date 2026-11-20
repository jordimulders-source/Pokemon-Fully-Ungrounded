# r6: doorlopend Sigilyph-zigzagpatroon over kraag, romp, bovenarmen en bovenbenen (Jordi: "een zigzagpatroon he").
# Witte zigzaglijnen (1 px) tussen gekleurde banden (afwisselend kleur A en B). Driehoeksgolf met periode 6 kolommen,
# toppen op de dijmiddens (kol 13 en 19) en het spleetmidden (kol 16): op elke dij een chevron van 2 rijen.
# Silhouet, kop, onderarmen en onderbenen = r4. Materialen: a A c = band A licht/midden/schaduw, n N m = band B,
# W wit, k lijn.
import sys, numpy as np
P=int(sys.argv[1]) if len(sys.argv)>1 else 5      # rijen per herhaling (1 wit + P-1 kleur)
OFF=int(sys.argv[2]) if len(sys.argv)>2 else 0   # fase van de banden
r4=np.array([list(l.rstrip('\n')[3:]) for l in open('../sprite_r4/rollen_hand.txt') if l.strip()]); H,W=r4.shape
o=r4.copy()
def bg(j,i): return not(0<=j<H and 0<=i<W) or r4[j,i]=='.'
def rand(j,i): return any(bg(j+a,i+b) for a,b in ((1,0),(-1,0),(0,1),(0,-1)))
zone=np.zeros((H,W),bool); deel=np.full((H,W),'',dtype='<U2')
def zet_zone(rows,cols,naam):
    for j in rows:
        for i in cols:
            if r4[j,i]!='.' and not zone[j,i]: zone[j,i]=True; deel[j,i]=naam
zet_zone(range(20,23),range(14,22),'R')     # kraag/nek
zet_zone(range(23,28),range(12,22),'R')     # romp
zet_zone(range(20,25),range(0,13),'LA')     # linker bovenarm (elleboog rij 20)
zet_zone(range(25,31),range(20,W),'RA')     # rechter bovenarm (elleboog rij 30)
zet_zone(range(28,42),range(10,17),'LD')    # linker dij (knie rij 41)
zet_zone(range(28,42),range(17,23),'RD')    # rechter dij
lijn=np.zeros((H,W),bool)
for j in range(H):
    for i in range(W):
        if zone[j,i] and (r4[j,i] in 'KS' or (r4[j,i] in 'bBrR' and rand(j,i))): lijn[j,i]=True; o[j,i]='k'
vul=zone&~lijn
# schaduw: 0 licht, 1 midden, 2 schaduw; één doorlopende lichte kant links/boven
sch=np.ones((H,W),int)
for j in range(H):
    for i in range(W):
        if not vul[j,i]: continue
        d=deel[j,i]
        if d=='LA':
            col=[y for y in range(H) if vul[y,i] and deel[y,i]=='LA']
            sch[j,i]=0 if j==min(col) else (2 if (j==max(col) and len(col)>=3) else 1)
        else:
            row=[x for x in range(W) if vul[j,x] and deel[j,x]==d]
            sch[j,i]=0 if i==min(row) else (2 if (i==max(row) and len(row)>=3) else 1)
z=lambda i: abs(((i-13)%6)-3)      # 3 op kol 13/19, 0 op kol 16
for j in range(H):
    for i in range(W):
        if not vul[j,i]: continue
        t=j+z(i)+OFF
        if deel[j,i]=='LA':   # langs de arm: kolom + 1 voor de onderste pixel -> witte lijn dwars over de arm, chevronstap
            t=i+(0 if sch[j,i]==0 else 1)+OFF
        if deel[j,i]=='RA':   # langs de arm: rij + 1 voor de rechter pixel
            t=j+(0 if sch[j,i]==0 else 1)+OFF
        if t%P==0: o[j,i]='W'
        else: o[j,i]=('aAc' if (t//P)%2==0 else 'nNm')[sch[j,i]]
np.save('mat.npy',o)
if __name__=='__main__':
    for j in range(18,44): print('%2d '%j+''.join(o[j]))
