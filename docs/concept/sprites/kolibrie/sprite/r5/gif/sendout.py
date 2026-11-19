# Soulibri komt uit de Poké Ball (tegenstanderskant), nagebouwd uit de code:
# - bal (graphics/balls/poke.png) opent op de plek van de Pokémon (benadering: 10 frames bal, dan open);
# - Pokémon groeit uit de bal: sAffineAnim_Battler_Emerge (src/data.c): schaal 0x28/256, +0x12/256 per frame, 12 frames;
#   tijdens het groeien wit getint dat wegvloeit (benadering van de balflits);
# - daarna kreet + frontanimatie tegelijk: ANIM_FRAMES (frame 2 één keer lang: 0×1, 1×30, 0×1) + ANIM_V_SLIDE
#   (src/pokemon_animation.c: y2 = -Sin((t*384/40)%256, 6), t = 0..40).
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
bal=Image.open('../../../../../../graphics/balls/poke.png').convert('RGBA')
bal=[bal.crop((0,i*16,16,i*16+16)) for i in range(3)]
for b in bal:
    px=b.load(); k=b.getpixel((0,0))
    for y in range(16):
        for x in range(16):
            if px[x,y][:3]==k[:3]: px[x,y]=(0,0,0,0)
BG=(248,248,240); Z=4; S=112
def canvas(): return Image.new('RGBA',(S,S),BG+(255,))
def out(c): return c.convert('RGB').resize((S*Z,S*Z),Image.NEAREST)
def mon(c,im,dy=0,s=1.0,wit=0.0):
    if wit>0:
        w=Image.new('RGBA',im.size,(255,255,255,255)); w.putalpha(im.getchannel('A'))
        im=Image.blend(im,w,wit)
    if s<1:
        n=max(1,round(64*s)); im=im.resize((n,n),Image.NEAREST)
        c.alpha_composite(im,((S-n)//2,(S-n)//2+dy))
    else: c.alpha_composite(im,((S-64)//2,(S-64)//2+dy))
frames=[];dur=[]
def add(c,ms): frames.append(out(c)); dur.append(ms)
# 1. bal zweeft en opent
for i in range(6):
    c=canvas(); c.alpha_composite(bal[0],(S//2-8,S//2-8+(2 if i%2 else 0))); add(c,50)
c=canvas(); c.alpha_composite(bal[1] if len(bal)>1 else bal[0],(S//2-8,S//2-8)); add(c,80)
# 2. groeien (60 fps, 12 frames; in de gif per 2)
for t in range(0,13,2):
    s=min(1,(0x28+0x12*t)/256); c=canvas(); mon(c,F[0],s=s,wit=1-t/12); add(c,33)
# 3. kreet + animatie
seq=[0]*1+[1]*30+[0]*1
for t in range(0,44,2):
    f=seq[t] if t<len(seq) else 0
    dy=-int(math.sin(2*math.pi*((t*384//40)%256)/256)*6) if t<=40 else 0
    c=canvas(); mon(c,F[f],dy=dy); add(c,33)
c=canvas(); mon(c,F[0]); add(c,1500)
frames[0].save('gif/soulibri_uit_de_bal.gif',save_all=True,append_images=frames[1:],duration=dur,loop=0)
print(len(frames))
