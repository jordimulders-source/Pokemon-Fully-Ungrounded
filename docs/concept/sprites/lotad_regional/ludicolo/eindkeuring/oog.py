# Rechteroog (rechts op de sprite) iets ovaler (Jordi: "het rechteroog heeft nog niet de perfecte vorm" ... "mag iets ovaler").
# Twee varianten op ludicolo_gaucho_e.png; pupil (28,25-26) en iris (27,26)/(29,26) blijven; verder niets aan het gezicht.
# A: ovaal 3 breed rond de pupil (x27-29): links een tweede irispixel, rechtsonder de hoek rond (model daar olijfmasker 116,100,65).
# B: ovaal naar rechts (x28-30), pupil links in het oog zoals in het model: rechts twee irispixels op rij 26-27, hoeken blijven masker.
import os, numpy as np; from PIL import Image, ImageDraw
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'ludicolo_gaucho_e.png')); e=np.array(im); pal=np.array(im.getpalette()[:48]).reshape(16,3)
VAR={'A':{(27,27):5,(29,28):10}, 'B':{(30,26):5,(30,27):6}}
def opslaan(s,pad):
    o=Image.fromarray(s.astype('uint8'),'P'); o.putpalette([int(v) for v in pal.ravel()]+[0]*(768-48)); o.save(pad,transparency=0)
def rgb(s,bg=(200,200,200)):
    a=pal[s].astype('uint8'); a[s==0]=bg; return Image.fromarray(a)
uit={'e (eindkeuring)':e}
for k,d in VAR.items():
    s=e.copy()
    for (x,y),v in d.items(): s[y,x]=v
    opslaan(s,os.path.join(H,'oog_%s.png'%k)); uit['oog_'+k]=s
    print('oog_%s: %d px gewijzigd'%(k,int((s!=e).sum())), {f'({x},{y})':f'{e[y,x]}->{v}' for (x,y),v in d.items()})
x0,y0,x1,y1=17,21,37,32; Z=20; w=(x1-x0)*Z; h=(y1-y0)*Z
mod=Image.open(os.path.join(H,'..','r6','gemini_r6.png')).convert('RGB').crop((300,330,560,470)).resize((int(260*h/140),h),Image.NEAREST)
W=Image.new('RGB',(3*(w+10)+mod.width,h+30+2*136+10),'white'); d=ImageDraw.Draw(W)
for i,(n,s) in enumerate(uit.items()):
    W.paste(rgb(s).crop((x0,y0,x1,y1)).resize((w,h),Image.NEAREST),(i*(w+10),24)); d.text((i*(w+10)+3,6),n,fill=(0,0,0))
    for bg_i,bg in enumerate([(248,248,248),(40,44,52)]): W.paste(rgb(s,bg).resize((128,128),Image.NEAREST),(i*(w+10)+bg_i*136,h+34))
W.paste(mod,(3*(w+10),24)); d.text((3*(w+10)+3,6),'model gemini_r6 (uitsnede)',fill=(0,0,0))
W.save(os.path.join(H,'oog_vel.png')); print(W.size)
