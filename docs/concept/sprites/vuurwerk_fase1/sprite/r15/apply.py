import numpy as np; from PIL import Image
S=Image.open('../r14/sprite.png'); a=np.array(S); b=a.copy()
for l in open('patches_r15.txt'):
    l=l.split('#')[0].strip()
    for t in l.split():
        rc,v=t.split('='); r,c=map(int,rc.split(',')); b[r,c]=int(v)
im=Image.fromarray(b,'P'); im.putpalette(S.getpalette()); im.save('sprite.png',transparency=0)
print('gewijzigd',int((a!=b).sum()),'silhouet-diff',int(((a==0)!=(b==0)).sum()))
v=Image.open('/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/86835790-8242-560c-8a0b-487fe7ec68a2/scratchpad/eind_r14/voorstel.png')
print('voorstel',v.mode,v.size)
vr=np.array(v.convert('RGBA')); sr=np.array(Image.open('sprite.png').convert('RGBA'))
if vr.shape==sr.shape:
    m=(vr!=sr).any(2)&~((vr[...,3]==0)&(sr[...,3]==0)); print('verschil met voorstel:',list(zip(*np.nonzero(m))))
def on(fn,bgc,z):
    x=Image.open(fn).convert('RGBA'); g=Image.new('RGBA',x.size,bgc+(255,)); g.alpha_composite(x); return g.resize((x.width*z,x.height*z),Image.NEAREST).convert('RGB')
on('sprite.png',(255,255,255),8).save('sprite_8x.png')
F3='../../../vuurwerk_fase3/af/vuurwerkslang.png'
V=Image.new('RGB',(2*522+10,512+20+128+20),'white')
for k,f in enumerate(['sprite.png',F3]):
    x=10+k*522; V.paste(on(f,(255,255,255),8),(x,10)); y=512+20
    V.paste(on(f,(248,248,240),1),(x,y)); V.paste(on(f,(40,40,48),1),(x+70,y))
    V.paste(on(f,(248,248,240),2),(x+140,y)); V.paste(on(f,(40,40,48),2),(x+274,y))
V.save('vergelijk.png')
