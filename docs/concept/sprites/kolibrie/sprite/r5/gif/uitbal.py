# Soulibri uit de Poké Ball (benadering): eerst groeien uit de bal (affine, ±16 frames, benadering),
# dan frontanimatie: ANIM_FRAMES-wissel + engine ANIM_V_SLIDE (nagerekend uit src/pokemon_animation.c:
# y2 = -Sin((t*384/40)%256, 6) voor t<=40; Sin = sinustabel*amp/256). 60 fps, gif in stappen van 2 frames.
import math
from PIL import Image
f1=Image.open('frame1.png'); f2=Image.open('frame2_a.png')
def rgba(im):
    a=im.convert('RGBA'); px=a.load(); ix=im.load()
    for y in range(64):
        for x in range(64):
            if ix[x,y]==0: px[x,y]=(0,0,0,0)
    return a
F=[rgba(f1),rgba(f2)]
def sin(i,amp): return int(math.sin(2*math.pi*(i%256)/256)*amp)
def vslide(t): return -sin(t*384//40,6) if t<=40 else 0
def ritme(cmds):
    seq=[]
    for img,d in cmds: seq+= [img]*d
    return seq
BEAUTIFLY=ritme([(0,2),(1,2)]*4+[(0,2)])          # Beautifly/Crobat-ritme
LANG=ritme([(0,1),(1,30),(0,1)])                   # frame 2 één keer lang in beeld
def render(naam,seq,engine,Z=4):
    imgs=[];dur=[]
    def frame(im,dy=0,s=1.0):
        c=Image.new('RGBA',(96,96),(255,255,255,255))
        if s<1:
            w=max(1,int(64*s)); im=im.resize((w,w),Image.NEAREST)
            c.alpha_composite(im,(16+(64-w)//2,16+(64-w)))
        else: c.alpha_composite(im,(16,16+dy))
        return c.convert('RGB').resize((96*Z,96*Z),Image.NEAREST)
    for t in range(0,16,2): imgs.append(frame(F[0],s=(t+2)/16)); dur.append(33)
    imgs.append(frame(F[0])); dur.append(300)
    T=max(len(seq),42)
    for t in range(0,T,2):
        f=seq[t] if t<len(seq) else 0
        imgs.append(frame(F[f],vslide(t) if engine else 0)); dur.append(33)
    imgs.append(frame(F[0])); dur.append(1200)
    imgs[0].save('gif/'+naam,save_all=True,append_images=imgs[1:],duration=dur,loop=0)
render('A_beautifly_ritme_vslide.gif',BEAUTIFLY,True)
render('B_frame2_lang_vslide.gif',LANG,True)
render('C_frame2_lang_zonder_engine.gif',LANG,False)
print('ok')
