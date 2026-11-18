"""Zoek soorten met een vergelijkbare front-pose (silhouet-IoU op 32x32 na bbox-normalisatie).
python3 pose_buren.py front.png [n]"""
import os,sys,numpy as np
from PIL import Image
def norm(p):
    a=np.array(Image.open(p))[:64]>0
    if not a.any(): return None
    ys,xs=np.nonzero(a); c=a[ys.min():ys.max()+1,xs.min():xs.max()+1]
    return np.array(Image.fromarray(c.astype(np.uint8)*255).resize((32,32),Image.BOX))>100, c.shape[1]/c.shape[0]
q,qa=norm(sys.argv[1]); n=int(sys.argv[2]) if len(sys.argv)>2 else 20; G='graphics/pokemon'; R=[]
for sp in os.listdir(G):
    d=f'{G}/{sp}'
    fp=d+'/anim_front.png' if os.path.exists(d+'/anim_front.png') else d+'/front.png'
    if not (os.path.exists(fp) and os.path.exists(d+'/icon.png')): continue
    try: m,a=norm(fp)
    except Exception: continue
    iou=(m&q).sum()/(m|q).sum(); R.append((iou*(1-min(.5,abs(a-qa)/qa)),sp))
for s,sp in sorted(R,reverse=True)[:n]: print(f'{s:.2f} {sp}')
