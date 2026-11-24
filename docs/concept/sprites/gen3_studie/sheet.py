import json,sys
from PIL import Image,ImageDraw,ImageFont
R="/home/user/Pokemon-Fully-Ungrounded/"
D=json.load(open("scored.json"))
F=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",13)
def tile(p,S):
    im=Image.open(p); a=im.convert("RGBA").crop((0,0,64,64))
    if im.mode=="P":
        px=im.load(); ap=a.load()
        for y in range(64):
            for x in range(64):
                if px[x,y]==0: ap[x,y]=(0,0,0,0)
    return a.resize((64*S,64*S),Image.NEAREST)
def sheet(lst,out,S=3,C=8):
    cw=64*S+10; ch=64*S+22; rows=(len(lst)+C-1)//C
    img=Image.new("RGB",(C*cw,rows*ch),(250,248,240)); d=ImageDraw.Draw(img)
    for k,(p,lab) in enumerate(lst):
        x=(k%C)*cw; y=(k//C)*ch; t=tile(p,S); img.paste(t,(x+5,y),t); d.text((x+5,y+64*S+3),lab[:28],font=F,fill=(0,0,0))
    img.save(out)
ours=[(R+"docs/concept/sprites/"+d["path"],f'{d["score"]:.1f} {d["name"]}') for d in D["ours"]]
sheet(ours,"alle_op_score.png",S=2,C=10)
g3=["taillow","mightyena","linoone","breloom","vileplume","gengar","altaria","swablu","banette","delibird","claydol","sunflora","octillery","dunsparce","hitmontop","alakazam"]
sheet([(R+f"graphics/pokemon/{n}/anim_front_gba.png",n) for n in g3],"gen3_ref.png",S=2,C=8)
