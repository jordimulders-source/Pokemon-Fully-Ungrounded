# bouw.py: lijf = r10 (52-schaal, alle goedgekeurde lijfwijzigingen) met rijen geschrapt (romp/broek/benen korter),
# kop = kop_ruw.npy (natieve schaal) erop, chin op de nek.
import numpy as np, sys
CUT=[22,25,31,33,37,42,43]
HDX,HDY=int(sys.argv[1]) if len(sys.argv)>1 else 0, int(sys.argv[2]) if len(sys.argv)>2 else 0
r10=np.load('../sprite_r10/bokser.npy').copy()
r10[0:12,10:]=0; r10[12:16,18:28]=0
keep=[y for y in range(52) if y not in CUT]
body=r10[keep]                       # 46 rijen; r10-rij 15 (kin) -> index 15
H=np.zeros((64,64),int)
bh=body.shape[0]; by=62-bh+1; bx=8
H[by:by+bh,bx:bx+35]=body
kop=np.load('kop_ruw.npy')
dx=int(round(bx+21.5-49))+HDX; dy=by+15-30+HDY
for y,x in zip(*np.where(kop)):
    if 0<=y+dy<64 and 0<=x+dx<64: H[y+dy,x+dx]=kop[y,x]
np.save('ruw.npy',H)
ys,xs=np.where(H); print('maat',xs.max()-xs.min()+1,'x',ys.max()-ys.min()+1,'top',ys.min())
# --- technische reparaties na het samenvoegen (eindcoördinaten)
FIX={(40,28):0,(41,28):0,          # 2-px uitsteeksel aan de kaakhoek (haarrand model) weg
     (48,16):0,(49,16):0,          # losse haarsliert onder de kuifpunt weg: schone punt
     (50,16):0,
     (31,12):1,(46,12):1,(32,13):1,(41,16):1,(41,18):1,   # losse donkergrijze pixels in de kuiven -> lijn
     (39,23):7,(39,24):7,(36,21):7,(38,26):7,              # losse tintjes aan de haar-/wangrand gelijk aan de buren
     (23,25):8,                    # los lichtgrijs vlekje links onder het linkeroog
     (33,33):6,(34,33):6,(35,33):1}# nek: gat tussen kin en nabije schouder dicht
for (x,y),v in FIX.items(): H[y,x]=v
np.save('ruw.npy',H)
