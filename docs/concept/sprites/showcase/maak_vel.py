from PIL import Image, ImageDraw, ImageFont
import sys, os
OUT=os.path.abspath(sys.argv[1]); R0=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../.."))+"/"
os.chdir(R0+"docs/concept/sprites")
S=3; C=6
items=[
("alpaca/ronde17/variant_kop/anim_front.png",'"Palpaca"',"fight"),
("lama/fase2/af/lama.png","Lama","fight"),
("lama/fase3/af/lama3.png",'"Cholucha"',"fight"),
("olinguito_v2/af/olinguito.png",'"Bandolingo"',"dark"),
("coathief/af/coathief.png",'"Coathief"',"dark"),
("wasbeer/af/wasbeer.png","Wasbeer","dark"),
("nachtaap/ronde12/variant_spiraal/anim_front.png","Nachtaap","psychic"),
("nachtaap_evo/af/nachtaap_evo.png","Nachtaap fase 2","psychic"),
("nachtaap_fase3/af/nachtaap_fase3.png","Muriqui","psychic"),
("cuyby/ronde4/anim_front.png",'"Cuyby"',"normal"),
("cuyby_evo/ronde6/anim_front.png",'"Cuychu"',"normal"),
("hatun_runa/af/hatun_runa.png",'"Kiskiddo"',"normal/flying"),
("awki/af/awki.png","Awki","fire/flying"),
("koningstiran/af/sapa_inca.png","Sapa Inca","fire/psychic"),
("viscacha/af/viscacha.png",'"Zapacha"',"electric"),
("kolibrie_pre/af/kolibrie_pre.png",'"Hummlet"',"flying"),
("kolibrie/af/kolibrie.png","Kolibrie","ghost/flying"),
("picapau/af/picapau.png",'"Picapau"',"electric/flying"),
("picapau_evo/af/picapau_evo.png",'"Picaraio"',"electric/flying"),
("poedellarve/af/poedellarve.png",'"Pupoodle"',"bug/normal"),
("poedelmot/af/poedelmot.png","Poedelmot","bug/fairy"),
("potoo/af/potoo.png",'"Bootoo"',"ghost/normal"),
("silicobra_uyuni/af/silicobra_uyuni.png",'"Silicobra" (regional)',"ground/electric"),
("salticonda/af/salticonda.png",'"Salticonda"',"ground/electric"),
("dj_rotom/af/dj_rotom.png",'"DJ Rotom"',"electric/steel"),
("hitmontop_evo/af/hitmongroove.png",'"Hitmongroove"',"fight/ground"),
]
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR=F.replace("-Bold","")
ft=ImageFont.truetype(F,36); fn=ImageFont.truetype(F,19); fy=ImageFont.truetype(FR,16)
def icon(t):
    i=Image.open(R0+f"graphics/types/{t}.png"); a=i.convert("RGBA")
    if i.mode=="P":
        px=i.load(); ap=a.load()
        for y in range(i.height):
            for x in range(i.width):
                if px[x,y]==0: ap[x,y]=(0,0,0,0)
    return a.resize((a.width*3,a.height*3),Image.NEAREST)
cw=64*S+28; ch=64*S+92; top=95; pad=28
W=pad*2+C*cw; R=(len(items)+C-1)//C; H=top+R*ch+pad+24
img=Image.new("RGB",(W,H),(246,242,233)); d=ImageDraw.Draw(img)
d.text((pad,28),"Pokémon Fully Ungrounded — nieuwe Pokémon (frontsprites af)",font=ft,fill=(50,40,35))
for k,(p,n,t) in enumerate(items):
    s=Image.open(p).crop((0,0,64,64))
    if s.mode=="P":
        a=s.convert("RGBA"); px=s.load(); ap=a.load()
        for y in range(64):
            for x in range(64):
                if px[x,y]==0: ap[x,y]=(0,0,0,0)
    else: a=s.convert("RGBA")
    a=a.resize((64*S,64*S),Image.NEAREST)
    x=pad+(k%C)*cw; y=top+(k//C)*ch
    d.rounded_rectangle((x+4,y,x+cw-4,y+ch-12),14,fill=(255,253,248),outline=(220,212,198),width=2)
    img.paste(a,(x+14,y+6),a)
    f=fn if d.textlength(n,font=fn)<=cw-24 else ImageFont.truetype(F,16)
    tw=d.textlength(n,font=f); d.text((x+(cw-tw)/2,y+64*S+10),n,font=f,fill=(40,35,30))
    ty=y+64*S+34
    if t=="?":
        tw=d.textlength("type open",font=fy); d.text((x+(cw-tw)/2,ty+12),"type open",font=fy,fill=(120,110,100))
    else:
        ic=[icon(z) for z in t.split("/")]; tot=sum(i.width for i in ic)+6*(len(ic)-1); ix=x+(cw-tot)//2
        for i in ic: img.paste(i,(ix,ty),i); ix+=i.width+6
d.text((pad,H-34),"Namen tussen aanhalingstekens zijn rond; de rest is een beschrijving. Starterfasen 1–2 tonen het type van de lijn.",font=fy,fill=(140,130,120))
img.save(OUT)
