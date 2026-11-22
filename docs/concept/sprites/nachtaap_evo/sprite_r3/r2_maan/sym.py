# A_sym / B_sym vanaf r2: maan (wit 8 + lila rand 7) spiegelsymmetrisch rond de oogas.
import sys; sys.path.insert(0,'r1'); from pal import *
H=dict(zip('.123456789ABCDEF',range(16)))
r2=np.load('r2/r2.npy')
# as: oogcentra = midden van de rode oogvlakken (A/B/9) per oog, y44-49
ys,xs=np.where(np.isin(r2[44:50,3:22],(9,10,11))); xs=xs+3
L=xs[xs<12]; R=xs[xs>12]; cl=(L.min()+L.max())/2; cr=(R.min()+R.max())/2; AS=(cl+cr)/2
print('oogcentra',cl,cr,'as x =',AS)
assert AS==12.0
rij={35:'?????'+'??'+'5'*8+'????',
     37:'???'+'5'+'7'+'8'*7+'7'+'5555'+'??',
     38:'???'+'7'+'8'*9+'7'+'5555'+'?',
     39:'??'+'7'+'8'*11+'7'+'55'+'4'+'?',
     40:'?'+'7'+'8'*13+'7'+'44'+'?',
     41:'5'+'7'+'8'*13+'7'+'44'+'?',
     42:'7'+'8'*6+'777'+'8'*6+'7'+'4'+'?',
     43:'7'+'8'*5+'?????'+'8'*5+'7'+'??'}
A=dict(rij); A[36]='?????'+'7'+'8'*5+'7'+'5'*5+'??'
B=dict(rij); B[36]='?????'+'5'*12+'??'
def zone(x,y): return 4<=x<=22 and 35<=y<=43 or (x==4 and y in (48,49))
for naam,rows in (('A_sym',A),('B_sym',B)):
    g=r2.copy()
    for y,s in rows.items():
        assert len(s)==19,(y,len(s))
        for i,c in enumerate(s):
            if c!='?': g[y,4+i]=H[c]
    g[48,4]=7; g[49,4]=7          # linkerpunt eindigt als de rechter (7 op y48-49)
    d=np.argwhere(g!=r2); buiten=sum(1 for y,x in d if not zone(x,y))
    alpha=int(((g>0)!=(r2>0)).sum()); ogen=int(sum(1 for y in range(44,50) for x in range(5,20) if g[y,x]!=r2[y,x]))
    # symmetriebewijs: maan = pixels 7/8 in de kop (x<=21, y35-49); spiegel x -> 24-x
    m=np.zeros_like(g); m[35:50,0:22]=np.isin(g[35:50,0:22],(7,8))*g[35:50,0:22]
    m[45:50,6:19]=0               # oogglans (wit in de ogen) hoort niet bij de maan
    asym=sum(1 for y in range(35,50) for x in range(0,25) if m[y,x]!=(m[y,24-x] if 0<=24-x<64 else 0))
    print(naam,'gewijzigd t.o.v. r2',len(d),'| buiten maanzone',buiten,'| alpha-diff',alpha,'| ogen',ogen,'| asymmetrische maanpixels',asym)
    assert buiten==0 and alpha==0 and ogen==0
    np.save('r2_maan/%s.npy'%naam,g)
    full=np.zeros((128,64),'uint8'); full[:64]=g; full[64:]=g
    im=Image.fromarray(full,'P'); flat=[]
    for c in PAL: flat+=list(c)
    im.putpalette(flat); im.save('r2_maan/%s.png'%naam,transparency=0)
    for y in range(34,51): print('%2d '%y+''.join(S[v] for v in g[y,0:26]))
