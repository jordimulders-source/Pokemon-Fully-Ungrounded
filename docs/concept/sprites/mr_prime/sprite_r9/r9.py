# r9 (op de r8-uitvoer; vel9.py draait r7.py, r8.py, dan dit): snor terug naar r7, jas links een bolling,
# rechterarm zonder rijbanden, losse 3 aan het einde van de hoedrand. Alleen tinten/pixels van de sprite zelf.
R8=C.copy(); LOG.clear()
import math
def rand0(y,x): return any(C[y+dy,x+dx]==0 for dy,dx in ((1,0),(-1,0),(0,1),(0,-1)))

# ---- 1. SNOR: vorm en tinten van r7 terug (krullen met lichte gaten, twee lobben), r8-snorzone ongedaan
Z='1 snor terug naar r7'
for y in range(20,26):
    for x in range(24,44):
        if (y,x) in ((21,32),(21,33),(21,34)): continue   # r8 punt 4: gezichtswit boven de snor blijft
        zet(Z,y,x,R7[y,x])
# alleen de losse lichte pixels midden in het zwart weg (krulgaten (26,22) en (41-42,21) blijven: die maken de krullen)
Z='1 snor: losse lichte pixels in het zwart'
zet(Z,23,42,1); zet(Z,24,33,1)

# ---- 2. JAS LINKS: een bolling, licht linksboven, sikkel aan de schaduwkant (rechts naar de V, onder)
Z='2 jas links'
M=np.zeros(C.shape,bool)
for y in range(30,45):
    for x in range(24,32):
        if y<31 and x<28: continue                      # mouw
        if C[y,x] in (2,3,4,5) and not rand0(y,x): M[y,x]=True
cx,cy,rx,ry=28.5,37.0,6.5,9.5
Lv=np.array([-0.75,-0.5,0.5]); Lv/=np.linalg.norm(Lv)
I=np.full(C.shape,-9.)
for y,x in zip(*np.where(M)):
    nx=(x+.5-cx)/rx; ny=(y+.5-cy)/ry; r2=min(nx*nx+ny*ny,0.98)
    I[y,x]=nx*Lv[0]+ny*Lv[1]+math.sqrt(1-r2)*Lv[2]
v=np.sort(I[M]); n=len(v); gr=[]; acc=0
for f in (0.22,0.36,0.30):
    acc+=f; gr.append(v[min(n-1,int(acc*n))])
for y,x in zip(*np.where(M)): zet(Z,y,x,(2,3,4,5)[sum(I[y,x]>=g for g in gr)])

# ---- 3. RECHTERARM (x45-53, y29-35): licht boven, schaduw onder; tintgrens = verhouding afstand tot de bovenrand
# (achtergrond) en tot de onderlijn (zwarte binnenlijn arm/jas), dus langs de arm i.p.v. per rij
Z='3 rechterarm'
ARM={29:46,30:47,31:47,32:48,33:47,34:49,35:50}
A=[(y,x) for y,x0 in ARM.items() for x in range(x0,57) if C[y,x] in (2,3,4,5) and not rand0(y,x)]
TOP=[(y,x) for y in range(26,40) for x in range(40,60) if C[y,x]==0 and x>=44]
BOT=[(y,x) for y in range(31,38) for x in range(44,56) if C[y,x]==1 and not rand0(y,x)]
def dmin(p,S): return min(math.hypot(p[0]-a,p[1]-b) for a,b in S)
for y,x in A:
    dt,db=dmin((y,x),TOP),dmin((y,x),BOT); t=dt/(dt+db)
    zet(Z,y,x,5 if (t<0.30 and x<=49) else 4 if t<0.45 else 3 if t<0.72 else 2)

# ---- 4. (50,11) losse 3 aan het einde van de hoedrand -> randtint
Z='4 hoedrand'
zet(Z,11,50,C[11,48])
