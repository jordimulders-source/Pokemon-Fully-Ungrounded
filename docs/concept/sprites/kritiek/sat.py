import sys, colorsys, numpy as np
sys.path.insert(0, '/home/user/projectgrounded/tools/concept/sprites')
import spritelib as L
D='/home/user/projectgrounded/docs/concept/sprites/'
sps = sys.argv[1:]
res=[]
for sp in sps:
    if sp in ('alpaca','olinguito','nachtaap'):
        a,pal=L.load_png(D+sp+'/anim_front.png'); a=a[:64]
    else:
        try: fr,pal=L.load_front(sp,'gba')
        except Exception: fr,pal=L.load_front(sp,'new')
        a=fr[0]
    px=a[a>0]; n=len(px)
    cnt=np.bincount(px,minlength=16)
    sats=[];hues=[]
    tot=0;ss=0;high=0
    for k in range(1,16):
        if cnt[k]==0: continue
        r,g,b=[c/255 for c in pal[k][:3]]
        h,l,s=colorsys.rgb_to_hls(r,g,b); hsv_s=colorsys.rgb_to_hsv(r,g,b)[1]; v=max(r,g,b)
        if v<0.15: continue  # omlijning
        tot+=cnt[k]; ss+=cnt[k]*hsv_s
        if hsv_s>0.5 and v>0.5: high+=cnt[k]
    top=[ '#%02x%02x%02x'%tuple(pal[k][:3]) for k in np.argsort(-cnt)[:3] if k]
    res.append((sp, ss/tot, high/tot, ' '.join(top)))
for r in res: print('%-12s gem.verzadiging %.2f  felle px %.0f%%  top %s'%(r[0],r[1],100*r[2],r[3]))
