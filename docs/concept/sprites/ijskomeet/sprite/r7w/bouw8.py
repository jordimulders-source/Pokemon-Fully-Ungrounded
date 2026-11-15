# r8: vanaf r7; kopomtrek + kruinfacetten (model), tonen per pixel uit modelpercentielen, donkere naden voet/kop-onderrand
import sys; sys.path.insert(0,'r7w')
from zones import *
import p6
o=np.load('r7w/r7.npy').copy()
body=np.load('r7w/body2.npy'); outer=np.load('r7w/outer2.npy')
P50=np.load('r7w/P50.npy'); P80=np.load('r7w/P80.npy')
eye=isin(R,'erCg')
seam=np.load('r7w/seam_hand.npy').copy()
kop_onder=[(41,2),(42,3),(42,4),(43,5),(44,6),(45,7),(45,8),(44,9),(43,10),(42,11),(41,12),(40,13),(39,14),(38,15),(38,16),(37,17),(37,18),(37,19)]
kruin=[(28,16),(28,15),(28,14),(29,13),(29,12),(30,11),(30,10),(31,9)]  # modelfacet (27,17)->(31,9), los einde boven het linkeroog
for p in kop_onder+kruin: seam[p]=True
seam[(45,9)]=False
inter=body&~outer&~eye
seam&=inter
def toon(j,i):
    m,h=P50[j,i],P80[j,i]
    if m>=226 or (h>=238 and m>=215): return 'W'
    if m>=208: return 'L'
    if m>=178: return 'M'
    return 'D'
for j,i in zip(*np.where(inter)):
    o[j,i]=I['S'] if seam[j,i] else I[toon(j,i)]
for p in kop_onder: o[p]=I['K']
voet=np.zeros((64,64),bool); voet[53:,:]=True
o[seam&voet]=I['K']
np.save('r7w/seam8.npy',seam)
# losse pixels in de vulling naar de meerderheid van de 4-buren
for _ in range(2):
  n=o.copy()
  for j,i in zip(*np.where(inter&~seam)):
    n4=[o[j+dy,i+dx] for dy,dx in ((1,0),(-1,0),(0,1),(0,-1))]
    dg=[o[j+dy,i+dx] for dy,dx in ((1,1),(-1,-1),(1,-1),(-1,1))]
    f=[v for v in n4 if CH[v] in 'WLMD']
    if o[j,i] not in n4 and o[j,i] not in dg and f: n[j,i]=max(set(f),key=f.count)
  o=n
np.save('r7w/r8.npy',o); p6.to_txt(o,'r8.txt')
im=Image.fromarray((o+1).astype('uint8'),'P'); pal=[255,255,255]+[v for c in p6.PAL for v in c]
im.putpalette(pal+[0]*(768-len(pal))); im.save('r8.png',transparency=0)
r=Image.open('r8.png').convert('RGBA').resize((512,512),0); bg=Image.new('RGBA',r.size,(255,255,255,255)); bg.alpha_composite(r); bg.convert('RGB').save('r8_8x.png')
