from PIL import Image,ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
D=R+'docs/concept/sprites/silicobra_uyuni/ronde6/'
def load(path,pal=None):
    im=Image.open(path).crop((0,0,64,64))
    if pal:
        L=open(pal).read().split('\n')[3:19]; p=[tuple(map(int,l.split())) for l in L if l.strip()]
        im.putpalette(list(sum(p,()))+[0]*(768-48))
    m=Image.new('L',(64,64)); m.putdata([0 if v==0 else 255 for v in im.get_flattened_data()])
    r=im.convert('RGBA'); r.putalpha(m); return r
P=R+'graphics/pokemon/'
mine=load(D+'silicobra_uyuni.png'); r1=load(R+'docs/concept/sprites/silicobra_uyuni/ronde5/silicobra_uyuni.png')
base=load(P+'silicobra/anim_front.png')
sk=Image.open(R+'docs/concept/sprites/silicobra_uyuni/schetsen_ronde2.png').convert('RGB').crop((320,30,640,350)).resize((64,64),Image.NEAREST).convert('RGBA')
refs=[(n,load(P+n+'/anim_front.png',P+n+'/normal.pal')) for n in ['sandshrew/alola','lanturn','torkoal','shuckle','sandaconda']]
items=[('origineel',base),('5A',r1),('ronde 6',mine)]
Z=4; W=64*Z
sh=Image.new('RGB',(W*3+20, 30+W*2+20+64*2+40+W+30),(250,250,250)); d=ImageDraw.Draw(sh)
d.text((6,6),'Silicobra (Uyuni) ronde 6 - 4x op licht en donker, daaronder 1x, onderaan referenties 4x/1x',fill=(0,0,0))
for k,(n,im) in enumerate(items):
    for j,bg in enumerate([(236,232,222),(56,58,68)]):
        t=Image.new('RGB',(64,64),bg); t.paste(im,(0,0),im); sh.paste(t.resize((W,W),Image.NEAREST),(k*(W+10),30+j*W))
    d.text((k*(W+10)+6,34),n,fill=(0,0,0))
y=30+2*W+10
for k,(n,im) in enumerate(items):
    for j,bg in enumerate([(236,232,222),(56,58,68)]):
        t=Image.new('RGB',(64,64),bg); t.paste(im,(0,0),im); sh.paste(t,(k*(W+10)+j*70,y))
y+=80
for k,(n,im) in enumerate(refs):
    t=Image.new('RGB',(64,64),(236,232,222)); t.paste(im,(0,0),im)
    sh.paste(t,(k*150,y)); sh.paste(t.resize((128,128),Image.NEAREST),(k*150,y+68)) if False else None
    d.text((k*150,y+66),n.split('/')[0]+('-A' if 'alola' in n else ''),fill=(0,0,0))
y+=84
row=Image.new('RGB',(W*3+20,W//2+10),(250,250,250))
for k,(n,im) in enumerate(refs[:3]+[('5A',r1),('ronde 6',mine)]):
    t=Image.new('RGB',(64,64),(236,232,222)); t.paste(im,(0,0),im); sh.paste(t.resize((128,128),Image.NEAREST),(k*160,y))
sh=sh.crop((0,0,W*3+20,y+140))
cr=(10,14,44,34); Z8=8
y0=sh.size[1]+10
big=Image.new('RGB',(sh.size[0],y0+(cr[3]-cr[1])*Z8+30),(250,250,250)); big.paste(sh,(0,0)); dd=ImageDraw.Draw(big)
for k,(n,im) in enumerate([('origineel 8x',base),('ronde 6 8x',mine)]):
    t=Image.new('RGB',(64,64),(236,232,222)); t.paste(im,(0,0),im); c=t.crop(cr)
    big.paste(c.resize(((cr[2]-cr[0])*Z8,(cr[3]-cr[1])*Z8),Image.NEAREST),(k*((cr[2]-cr[0])*Z8+12),y0+20)); dd.text((k*((cr[2]-cr[0])*Z8+12),y0+4),n,fill=(0,0,0))
big.save(D+'vel.png')
