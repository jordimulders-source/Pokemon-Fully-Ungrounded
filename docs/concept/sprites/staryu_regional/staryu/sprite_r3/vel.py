# vel.py: r3 | r2 | model op schaal (8x) / 1x op wit en donker: r3, r2, model, Gen 3 Staryu, Taillow + maatstaf (skinguin, dundragoon, viscacha, awki)
import sys, numpy as np; from PIL import Image, ImageDraw
sys.path.insert(0,'gereedschap'); import gemeen as g
def sp(path,bg):
    im=Image.open(path); o=np.asarray(im)[:64,:64]; pal=np.array(im.getpalette()[:48]).reshape(-1,3)
    img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
def gba(n,bg):
    p=[int(t) for t in open('../../../../../graphics/pokemon/%s/normal_gba.pal'%n).read().split()[3:]]
    im=Image.open('../../../../../graphics/pokemon/%s/anim_front_gba.png'%n).crop((0,0,64,64)); im.putpalette(p+[0]*(768-len(p)))
    o=np.asarray(im); pal=np.array(p[:48]).reshape(-1,3); img=np.zeros((64,64,3),'uint8'); img[:]=bg
    for k in range(1,16): img[o==k]=pal[k]
    return Image.fromarray(img)
W=(255,255,255); D=(40,44,52)
box=(8,8,56,58); z=8
p8=[sp('sprite_r3/staryu_r3.png',W).crop(box), sp('sprite_r2/staryu_r2.png',W).crop(box), g.model_op_schaal().crop(box)]
pw=(box[2]-box[0])*z; ph=(box[3]-box[1])*z
v=Image.new('RGB',(max(3*pw+40,9*200),ph+60+2*150),'white'); dr=ImageDraw.Draw(v)
for i,(p,t) in enumerate(zip(p8,['r3','r2','model op schaal'])):
    v.paste(p.resize((pw,ph),Image.NEAREST),(i*(pw+20),20)); dr.text((i*(pw+20),4),t,fill=(0,0,0))
y=ph+50
srcs=[('r3',lambda b:sp('sprite_r3/staryu_r3.png',b)),('r2',lambda b:sp('sprite_r2/staryu_r2.png',b)),('model',lambda b:g.model_op_schaal())]
srcs+=[(n,(lambda n: lambda b:gba(n,b))(n)) for n in ['staryu','taillow']]
srcs+=[(n,(lambda n: lambda b:sp('../../%s/af/%s.png'%(n,n),b))(n)) for n in ['skinguin','dundragoon','viscacha','awki']]
for j,bg in enumerate([W,D]):
    for i,(n,f) in enumerate(srcs):
        im=f(bg); v.paste(im,(i*200,y+j*150)); v.paste(im.resize((128,128),Image.NEAREST),(i*200+66,y+j*150))
        dr.text((i*200,y+j*150+66),n,fill=(0,0,0) if bg==W else (255,255,255))
v.save('sprite_r3/vel.png'); print(v.size)
