# px.py ronde x,y x,y ... : model per spritepixel (gem RGB, helderheid gem/p15/max) naast de spritewaarde. ronde = map, bv kleur_r1
import sys,json,numpy as np; from PIL import Image
P='/home/user/Pokemon-Fully-Ungrounded/docs/concept/sprites/potoo/'
k=json.load(open(P+'gereedschap/kader.json')); X0,Y0,s=k['x0'],k['y0'],k['s']
c=np.asarray(Image.open(P+'model/model_lijf_30.png')).astype(float)
sp=np.asarray(Image.open(P+sys.argv[1]+'/potoo.png').convert('RGBA'))
for a in sys.argv[2:]:
    x,y=map(int,a.split(','))
    b=c[int(Y0+y*s):int(Y0+(y+1)*s),int(X0+x*s):int(X0+(x+1)*s)]; f=b[...,3]>0
    if not f.any(): print(f'({x},{y}) model leeg, sprite {tuple(sp[y,x])}'); continue
    rgb=b[...,:3][f]; L=rgb.mean(1)
    print(f'({x},{y}) sprite {tuple(sp[y,x,:3])} a{sp[y,x,3]} | model dekking {f.mean():.2f} gem {tuple(rgb.mean(0).astype(int))} L gem {L.mean():.0f} p15 {np.percentile(L,15):.0f} max {L.max():.0f}')
