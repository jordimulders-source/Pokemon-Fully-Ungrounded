# r2_maan: varianten A/B vanaf r2, alleen in de maan (x4-22, y35-43). Bewijs: pixeldiff 0 erbuiten, alpha-diff 0.
import sys; sys.path.insert(0,'r1'); from pal import *
H=dict(zip('.123456789ABCDEF',range(16)))
r2=np.load('r2/r2.npy')
# rijen vanaf x=7 (links daarvan niets veranderd); '?' = laten staan
# A: bovenkant 1 px ingekort (rij kopvacht 5 onder de buitenlijn), rechterrand als boog: laatste wit x15,16,17,17,18,18,19,19 (y36-43)
A={35:'????55555555',            # x7..: x11-18 -> 5 (was 8888 7 555)
   36:'??55'+'88888'+'75555',    # x9-10 5, x11-15 wit, rand x16, x17-20 5
   37:'55'+'88888888'+'7555',    # x7-8 5, wit x9-16, rand x17, x18-20 5
   38:'8'*11+'7555',             # wit x7-17, rand x18, x19-21 5
   39:'?'+'8'*10+'7554',         # wit x8-17 (x6-7 al wit), rand x18, x19-20 5, x21 4
   42:'????????????87'+'4'}      # x19 wit, rand x20, x21 4
# B: bovenkant 2 px ingekort, zelfde boog vanaf y37
B=dict(A); B.update({36:'??'+'5'*12,             # x9-20 -> 5
   37:'5555'+'888888'+'7555',                    # x7-10 5, wit x11-16, rand x17
   38:'55'+'8'*9+'7555'})                        # x7-8 5, wit x9-17, rand x18
def maak(rows):
    g=r2.copy()
    for y,s in rows.items():
        for i,c in enumerate(s):
            if c!='?': g[y,7+i]=H[c]
    return g
def zone(x,y): return 4<=x<=22 and 35<=y<=43
for naam,rows in (('A',A),('B',B)):
    g=maak(rows); d=np.argwhere(g!=r2)
    buiten=sum(1 for y,x in d if not zone(x,y)); alpha=int(((g>0)!=(r2>0)).sum())
    ogen=int((g[44:50]!=r2[44:50]).sum())
    print(naam,'gewijzigd',len(d),'| buiten maanzone',buiten,'| alpha-diff',alpha,'| ogen y44-49',ogen,
          '| wit->paars',int(((r2==8)&(g!=8)).sum()),'| 7 verplaatst',int(((r2==7)!=(g==7)).sum()))
    assert buiten==0 and alpha==0 and ogen==0
    np.save('r2_maan/%s.npy'%naam,g)
    full=np.zeros((128,64),'uint8'); full[:64]=g; full[64:]=g
    im=Image.fromarray(full,'P'); flat=[]
    for c in PAL: flat+=list(c)
    im.putpalette(flat); im.save('r2_maan/%s.png'%naam,transparency=0)
    for y in range(34,45): print('%2d '%y+''.join(S[v] for v in g[y,0:26]))
