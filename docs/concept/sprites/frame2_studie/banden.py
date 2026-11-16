# Per horizontale band (kop / midden / voeten) de beste verschuiving van frame 2 t.o.v. frame 1.
import glob,os,sys,numpy as np,collections
from PIL import Image
suf=sys.argv[1]
def best(a,b,mask):
    bs=None
    for dy in range(-4,5):
        for dx in range(-4,5):
            s=np.roll(np.roll(a,dy,0),dx,1)
            sc=((s==b)&mask&(b!=0)).sum()
            if bs is None or sc>bs[0] or (sc==bs[0] and abs(dx)+abs(dy)<abs(bs[1])+abs(bs[2])): bs=(sc,dx,dy)
    return bs
C=collections.Counter();rows=[]
for p in sorted(glob.glob(f'graphics/pokemon/*/anim_front{suf}.png')):
    if '/' in os.path.relpath(p,'graphics/pokemon').split('/anim')[0]: continue
    a=np.array(Image.open(p).convert('P'))
    if a.shape!=(128,64): continue
    f1,f2=a[:64],a[64:]
    if not (f2!=0).any(): continue
    ys=np.where((f1!=0).any(1))[0];t,bt=ys.min(),ys.max();h=bt-t+1
    Y=np.arange(64)[:,None]*np.ones((1,64),bool)
    top=(Y<t+h*0.35);bot=(Y>bt-h*0.15)
    st=best(f1,f2,top);sb=best(f1,f2,bot)
    kind=('voeten vast' if (sb[1],sb[2])==(0,0) else 'voeten mee')+', bovenkant '+('stil' if (st[1],st[2])==(0,0) else 'beweegt')
    C[kind]+=1; rows.append((os.path.basename(os.path.dirname(p)),st[1:],sb[1:]))
n=len(rows);print(suf or 'ds',n)
for k,v in C.most_common(): print(f'  {k}: {v} ({v*100//n}%)')
mag=collections.Counter(max(abs(r[1][0]),abs(r[1][1])) for r in rows if r[2]==(0,0))
print('  grootte beweging bovenkant bij vaste voeten:',sorted(mag.items()))
dyc=collections.Counter(np.sign(r[1][1]) for r in rows if r[2]==(0,0) and r[1]!=(0,0));print('  richting dy (-1=omhoog):',dict(dyc))
