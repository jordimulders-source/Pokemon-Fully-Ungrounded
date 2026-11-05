from PIL import Image, ImageDraw, ImageFont
import sys, os
OUT=os.path.abspath(sys.argv[1])
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
S=4; C=5
items=[
("alpaca/ronde17/variant_kop/anim_front.png","Alpaca","Fighting"),
("lama/fase2/af/lama.png","Lama","Fighting"),
("lama/fase3/af/lama3.png","Cholita-lama","Fighting"),
("olinguito_v2/af/olinguito.png","Olinguito","Dark"),
("coathief/af/coathief.png","Coathief","Dark"),
("wasbeer/af/wasbeer.png","Wasbeer","Dark"),
("nachtaap/ronde12/variant_spiraal/anim_front.png","Nachtaap","Psychic"),
("nachtaap_evo/af/nachtaap_evo.png","Nachtaap fase 2","Psychic"),
("cuyby/ronde4/anim_front.png","Cuyby","Normal"),
("cuyby_evo/ronde6/anim_front.png","Cuychu","Normal"),
("kolibrie_pre/af/kolibrie_pre.png","Kolibrie fase 1","Ghost/Flying"),
("kolibrie/af/kolibrie.png","Kolibrie","Ghost/Flying"),
("silicobra_uyuni/af/silicobra_uyuni.png","Silicobra (Uyuni)","Ground/Electric"),
("salticonda/af/salticonda.png","Salticonda","Ground/Electric"),
("dj_rotom/af/dj_rotom.png","DJ Rotom",""),
]
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR=F.replace("-Bold","")
ft=ImageFont.truetype(F,40); fn=ImageFont.truetype(F,22); fy=ImageFont.truetype(FR,17)
cw=64*S+40; ch=64*S+80; top=110; pad=30
W=pad*2+C*cw; R=(len(items)+C-1)//C; H=top+R*ch+pad+30
img=Image.new("RGB",(W,H),(246,242,233)); d=ImageDraw.Draw(img)
d.text((pad,30),"Pokémon Fully Ungrounded — nieuwe frontsprites",font=ft,fill=(50,40,35))
for k,(p,n,t) in enumerate(items):
    s=Image.open(p)
    s=s.crop((0,0,64,64))
    if s.mode=="P":
        a=s.convert("RGBA"); px=s.load(); ap=a.load()
        for y in range(64):
            for x in range(64):
                if px[x,y]==0: ap[x,y]=(0,0,0,0)
    else: a=s.convert("RGBA")
    a=a.resize((64*S,64*S),Image.NEAREST)
    x=pad+(k%C)*cw; y=top+(k//C)*ch
    d.rounded_rectangle((x+6,y,x+cw-6,y+64*S+20),14,fill=(255,253,248),outline=(220,212,198),width=2)
    img.paste(a,(x+20,y+10),a)
    tw=d.textlength(n,font=fn); d.text((x+(cw-tw)/2,y+64*S+26),n,font=fn,fill=(40,35,30))
    if t: tw=d.textlength(t,font=fy); d.text((x+(cw-tw)/2,y+64*S+52),t,font=fy,fill=(120,110,100))
d.text((pad,H-34),"Werknamen; namen, types en details kunnen nog veranderen.",font=fy,fill=(140,130,120))
img.save(OUT)
