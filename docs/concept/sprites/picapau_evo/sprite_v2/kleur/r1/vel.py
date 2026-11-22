# vel.png: kleur r1 | r4 | model (8x); onder: 1x/2x op licht en donker, en 1x naast Pidgeot en Swellow
import numpy as np; from PIL import Image, ImageDraw
R='/home/user/Pokemon-Fully-Ungrounded/'
def rgba(f):
    im=Image.open(f); im.save('_tmp/tmp.png',transparency=0); return Image.open('_tmp/tmp.png').convert('RGBA')
cur=rgba('picaraio.png'); prev=rgba('../../r4/picaraio.png')
mi0=Image.open('../../../gemini/r9_prompt_v6.png').convert('RGB'); S=15.36
mi=Image.new('RGB',(1024,1060),(255,255,255)); mi.paste(mi0,(0,11))
m=mi.crop((int(20.48),1,int(20.48+64*S),int(1+64*S))).resize((64,64),Image.BOX).convert('RGBA')
def on(im,bg,s):
    b=Image.new('RGBA',im.size,bg); b.alpha_composite(im); return b.convert('RGB').resize((im.width*s,im.height*s),0)
V=Image.new('RGB',(3*522+10,20+512+30+140),(200,200,200)); d=ImageDraw.Draw(V)
for i,(im,t) in enumerate([(cur,'kleur r1'),(prev,'r4'),(m,'model r9 verkleind')]):
    V.paste(on(im,(255,255,255,255),8),(10+i*522,20)); d.text((10+i*522,4),t,fill=(0,0,0))
y0=560; x=10
for bg in ((248,248,248,255),(40,40,48,255)):
    V.paste(on(cur,bg,1),(x,y0)); V.paste(on(cur,bg,2),(x+70,y0)); x+=210
refs=[Image.open(R+'graphics/pokemon/%s/anim_front.png'%n).convert('RGBA').crop((0,0,64,64)) for n in ('pidgeot','swellow')]
for bg in ((248,248,248,255),(152,208,160,255)):
    for im in [cur]+refs: V.paste(on(im,bg,1),(x,y0)); x+=68
    x+=12
d.text((430,y0-14),'1x naast Pidgeot en Swellow',fill=(0,0,0))
V.save('vel.png'); print(V.size)
