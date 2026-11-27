# Bevroren-checks ek1 t.o.v. r3 (en r1/r2-silhouet)
import numpy as np; from PIL import Image
R3=Image.open('../sprite_r3/kuiken_r3_M_i_a.png'); E=Image.open('kuiken_ek1.png')
B=np.array(R3); S=np.array(E)
pB=[tuple(R3.getpalette()[i*3:i*3+3]) for i in range(16)]; pS=[tuple(E.getpalette()[i*3:i*3+3]) for i in range(16)]
rgbB=np.array(pB)[B]; rgbS=np.array(pS)[S]
print('alpha-diff t.o.v. r3:',int(((B>0)!=(S>0)).sum()))
R1=np.array(Image.open('../sprite_r1/kuiken_r1.png')); print('alpha-diff t.o.v. r1:',int(((R1>0)!=(S>0)).sum()))
OOGPX=[(13,23),(14,23),(15,23),(12,24),(13,24),(14,24),(15,24),(11,25),(12,25),(13,25),(14,25),(15,25),(11,26),(12,26),(13,26),(14,26),(15,26),(11,27),(12,27),(13,27)]
OOG=[(y+2,x+17) for (x,y) in OOGPX]+[(28,29)]
print('oog D: indexdiff',sum(B[p]!=S[p] for p in OOG),' RGB-diff',sum(tuple(rgbB[p])!=tuple(rgbS[p]) for p in OOG),'(%d px)'%len(OOG))
ring=[(y,x) for y in range(24,31) for x in range(27,34)]
print('oogvak 7x7 (incl. ring eromheen) RGB-diff',sum(tuple(rgbB[p])!=tuple(rgbS[p]) for p in ring))
print('kleuren incl. transparant:',len(set(S.ravel())|{0}),' palet uniek:',len(set(pS)))
ch=(B!=S); print('gewijzigde pixels:',int(ch.sum()))
# vlakvorm: een pixel mag alleen binnen zijn eigen 'lijn/vlak'-klasse schuiven: lijn (1,5,2,4 donkerst) <-> lijn, vlak <-> vlak
LIJN={1,2,5}; 
vl=[(y,x,int(B[y,x]),int(S[y,x])) for y,x in zip(*np.where(ch)) if (B[y,x] in LIJN)!=(S[y,x] in LIJN|{4})]
print('lijn<->vlak wissels:',vl)
# zwart-ratio
pal=pS; L=[sum(c)/3 for c in pal]; al=S>0
zw=sum(1 for y in range(64) for x in range(64) if al[y,x] and L[S[y,x]]<30)
binnen=sum(1 for y in range(1,63) for x in range(1,63) if al[y,x] and L[S[y,x]]<30 and all(al[y+dy,x+dx] for dy,dx in((0,1),(1,0),(0,-1),(-1,0))))
zwB=sum(1 for y in range(64) for x in range(64) if B[y,x]==1)
print('zwart %d -> %d (aandeel %.3f), binnen-zwart %d'%(zwB,zw,zw/al.sum(),binnen))
# tintvlakjes <3 px (4-buren), per index, behalve zwart/oog
def label(M):
    lab=np.zeros(M.shape,int); n=0
    for y,x in zip(*np.where(M)):
        if lab[y,x]: continue
        n+=1; st=[(y,x)]; lab[y,x]=n
        while st:
            cy,cx=st.pop()
            for dy,dx in ((0,1),(1,0),(0,-1),(-1,0)):
                q=(cy+dy,cx+dx)
                if 0<=q[0]<64 and 0<=q[1]<64 and M[q] and not lab[q]: lab[q]=n; st.append(q)
    return lab,n
def klein(A):
    out=[]
    for t in set(A.ravel())-{0,1,15}:
        lab,n=label(A==t)
        for k in range(1,n+1):
            c=np.argwhere(lab==k)
            if len(c)<3: out.append((t,[tuple(map(int,p)) for p in c]))
    return out
kb=klein(B); ks=klein(S)
print('vlakjes<3 r3: %d  ek1: %d'%(len(kb),len(ks)))
nieuw=[k for k in ks if k not in kb]; print('nieuwe vlakjes in ek1:',nieuw)
# helderheidsstappen per kleurgroep
Lm=lambda c:round(0.299*c[0]+0.587*c[1]+0.114*c[2])
for n,ix in [('lijf',[5,6,7]),('gezicht',[4,8,14]),('creme',[8,9,10]),('snavel',[2,3,9]),('poten',[11,12,13])]:
    print(n,[pS[i] for i in ix],[Lm(pS[i]) for i in ix])
