from PIL import Image, ImageDraw, ImageFont
import sys, os
OUT=os.path.abspath(sys.argv[1]); R0=os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)),"../../../.."))+"/"
os.chdir(R0+"docs/concept/sprites")
S=3; C=6
SECTIES=[
("New",[
("alpaca/af/palpaca.png",'"Palpaca"',"fight"),
("lama/fase2/af/lama.png",'"Llamauler"',"fight"),
("lama/fase3/af/lama3.png",'"Cholucha"',"fight"),
("olinguito_v2/af/olinguito.png",'"Bandolingo"',"dark"),
("coathief/af/coathief.png",'"Coathief"',"dark"),
("wasbeer/af/wasbeer.png",'"Vigiloot"',"dark"),
("nachtaap/af/nachtaap.png",'"Nocticue"',"psychic"),
("nachtaap_evo/af/nachtaap_evo.png",'"Moonkey"',"psychic"),
("nachtaap_fase3/af/nachtaap_fase3.png",'"Curiqui"',"psychic/cosmic"),
("cuyby/ronde4/anim_front.png",'"Cuyby"',"normal"),
("cuyby_evo/ronde6/anim_front.png",'"Cuychu"',"normal"),
("hatun_runa/af/hatun_runa.png",'"Kiskiddo"',"normal/flying"),
("awki/af/awki.png",'"Princadee"',"fire/flying"),
("koningstiran/af/sapa_inca.png",'"Sunperor"',"fire/psychic"),
("viscacha/af/viscacha.png",'"Zapacha"',"electric"),
("kolibrie_pre/af/kolibrie_pre.png",'"Hummlet"',"flying"),
("kolibrie/af/kolibrie.png",'"Soulibri"',"ghost/flying"),
("picapau/af/picapau.png",'"Picapau"',"electric/flying"),
("picapau_evo/af/picapau_evo.png",'"Picaraio"',"electric/flying"),
("poedellarve/af/poedellarve.png",'"Pupoodle"',"bug/normal"),
("poesrups/af/poesrups.png",'"Purrpillar"',"bug/fairy"),
("poedelmot/af/poedelmot.png",'"Lanymph"',"bug/fairy"),
("potoo/af/potoo.png",'"Bootoo"',"ghost/normal"),
("sneeuwbolslak/af/sneeuwbolslak.png",'"Globsnail"',"ice"),
("sneeuwbolslak_fase2/af/sneeuwbolslak_fase2.png",'"Clionice"',"ice"),
("ijskomeet/af/ijskomeet.png",'"Cryomet"',"ice/cosmic"),
("steenmozaiek/af/welp.png",'Steenjaguar-welp',"rock"),
("steenmozaiek/af/steenjaguar.png",'"Mosaguar"',"rock"),
("blobfish/af/blobfish.png",'"Gumfish"',"water"),
("blobfish_fase2/af/blobfish_fase2.png",'Blobfish (pudding)',"water"),
("spooktrein_fase1/af/spooktrein_fase1.png",'"Scrapstack"',"steel"),
("spooktrein_fase2/af/spooktrein_fase2.png",'"Wagogogon"',"steel/ghost"),
("spooktrein_fase3/af/spooktrein.png",'"Hexpress"',"steel/ghost"),
("pitahaya_draak/af/pitahaya_draak.png",'"Pitaling"',"grass/dragon"),
("pitahaya_draak_fase2/af/pitahaya_draak_fase2.png",'"Tejuice"',"grass/dragon"),
("pitahaya_draak_fase3/af/pitahaya_draak_fase3.png",'Pitahaya-draak fase 3',"grass/dragon"),
("vuurwerk_fase1/af/vuurwerk_fase1.png",'"Axolaunch"',"fire/fairy"),
("vuurwerk_fase3/af/vuurwerkslang.png",'"Pyrowyrm"',"fire/fairy"),
("mate/af/mate.png",'Mate-kalebas',"grass/water"),
("mate_fase2/af/mate2.png",'"Rowmate"',"grass/water"),
("vlieglijn_fase1/af/vlieg.png",'"Flytron"',"bug/electric"),
("vlieglijn_fase2/af/mug.png",'"Buzzquito"',"poison/electric"),
("vuurduivel_fase1/af/vuurduivel.png",'"Impyre"',"fire/dark"),
("vuurduivel_fase2/af/vuurduivel2.png",'Vuurduivel fase 2',"fire/dark"),
("gnomini/af/gnomini.png",'"Gnomini"',"fairy"),
("gnomad/af/gnomad.png",'"Gnomad"',"fairy"),
("gnometrotter_rock/af/gnometrotter_rock.png",'"Gnometrotter" (Rock)',"fairy/rock"),
("gnometrotter_ice/af/gnometrotter_ice.png",'"Gnometrotter" (Ice)',"fairy/ice"),
("gnometrotter_grass/af/gnometrotter_grass.png",'"Gnometrotter" (Grass)',"fairy/grass"),
("satelliet_lijn/fase1/af/satelliet_fase1.png",'Satelliet fase 1 (Spoetnik)',"steel/cosmic"),
("satelliet_fase2/af/satelliet.png",'Satelliet fase 2',"steel/cosmic"),
("satelliet_fase3/af/ruimtestation.png",'Ruimtestation (satelliet fase 3)',"steel/cosmic"),
("capybarrel/af/capybarrel.png",'"Capybarrel"',"normal"),
("capykart/af/capykart.png",'"Capykart"',"normal"),
("tempel/af/tempel.png",'Levende tempel',"ghost/rock"),
("impala_lijn/dikdik/af/dikdik.png",'Dikdik (impala-lijn fase 1)',"normal"),
("impala_lijn/impala/af/impala.png",'"Impalar"',"normal/steel"),
("impala_lijn/kudu/af/kudu.png",'Kudu (impala-lijn fase 3)',"normal/steel"),
("glitch_lijn/fase1_glitch/af/glitch_fase1.png",'"Missingraph."',"electric"),
("glitch_lijn/fase2_bug/af/glitch_fase2.png",'Bug (glitch-lijn fase 2)',"electric/bug"),
("glitch_lijn/fase3_virus/af/glitch_fase3.png",'Virus (glitch-lijn fase 3)',"electric/bug"),
("guarana/af/guarana.png",'Guaraná fase 1',"grass/ghost"),
("guarana_fase2/af/guarana_fase2.png",'Guaraná fase 2',"grass/ghost"),
("sneeuwmonster/af/sneeuwmonster.png",'Sneeuwmonster (fase 1)',"ice"),
("sneeuwmonster_fase2/af/sneeuwmonster2.png",'Sneeuwmonster (fase 2)',"ice/fire"),
("sneeuwmonster_fase3/af/sauna_yeti.png",'Sauna-yeti (fase 3)',"ice/fire"),
("hoatzin/af/hoatzin_fase1.png",'Hoatzin fase 1 (kuiken)',"poison/dark"),
("hoatzin/af/hoatzin_fase2.png",'Hoatzin fase 2 (pestmasker)',"poison/dark"),
("zandloper/fase1/af/zandloper_fase1.png",'Zandloper (zandloper-lijn fase 1)',"ground/psychic"),
("zandloper/fase3/af/zandloper_fase3.png",'Zand-djinn (zandloper-lijn fase 3)',"ground/psychic"),
]),
("Evolutions of existing Pokémon",[
('hitmontop_evo/af/hitmongroove.png', '"Hitmongroove" (Hitmontop)', 'fight/ground'),
('octillery_evo/af/krassault.png', '"Krassault" (Octillery)', 'water/steel'),
('banette_evo/af/shuppetto.png', '"Shuppetto" (Banette)', 'ghost/dark'),
('skinguin/af/skinguin.png', '"Skinguin" (Delibird)', 'ice/water'),
('dundragoon/af/dundragoon.png', '"Dundragoon" (Dunsparce)', 'dragon/normal'),
('mightyena_evo/af/alphyena.png', '"Alphyena" (Mightyena)', 'dark/fight'),
('bibarel_evo/af/bibarel_evo.png', '"Bibuilder" (Bibarel)', 'water/fight'),
('sunflora_evo/af/sunflora_evo.png', 'Sunflora-evolutie (Sunflora)', 'grass/cosmic'),
('kricketune_evo/af/krickestro.png', '"Krickestro" (Kricketune)', 'bug/fairy'),
('solrock_evo/af/solrock_evo.png', 'Solrock-evolutie (Solrock)', 'rock/cosmic'),
('lunatone_evo/af/bloedmaan.png', 'Bloedmaan (Lunatone)', 'rock/cosmic'),
('emolga_evo/af/model.png', 'Wingsuit-colugo (Emolga)', 'electric/flying'),
('emolga_evo_fase3/af/fruitvampier.png', 'Fruitvampier (Emolga)', 'electric/flying'),
('ledian_evo/af/ledian_evo.png', 'Ledian-evolutie (Ledian)', 'bug/cosmic'),
]),
("Regional forms / convergent Pokémon",[
("silicobra_uyuni/af/silicobra_uyuni.png",'"Silicobra" (regional)',"ground/electric"),
("salticonda/af/salticonda.png",'"Salticonda"',"ground/electric"),
("abra_regional/af/abra_regional.png",'Abra (regional)',"dark"),
("kadabra_regional/af/kadabra_charlatan.png",'Kadabra (regional)',"dark/psychic"),
("alakazam_regional/af/alakazam_charlatan.png",'Alakazam (regional)',"dark/psychic"),
("dustly/af/dustly.png",'"Dustly"',"cosmic/poison"),
("hauntflare/af/hauntflare.png",'"Hauntflare"',"cosmic/poison"),
("gengas/af/gengas.png",'"Gengas"',"cosmic/poison"),
("rufflet_regional/af/rufflet.png",'Rufflet (regional)',"flying"),
("harpij_braviary/af/harpij.png",'"Harpiary"',"steel/flying"),
("oddish_regional/af/oddish_regional.png",'Oddish (regional)',"water/grass"),
("oddish_regional/gloom_sprite/af/gloom.png",'Gloom (regional)',"water/fire"),
("oddish_regional/vileplume_sprite/af/vileplume_regional.png",'Vileplume (regional)',"water/fire"),
("baltoy_regional/af/baltoy_regional.png",'Baltoy (regional)',"rock/psychic"),
("baltoy_regional/claydol_af/claydol_regional.png",'Claydol (regional)',"rock/psychic"),
("swablu_regional/af/swablu.png",'Swablu (regional)',"electric/flying"),
("swablu_regional/altaria/af/altaria.png",'Altaria (regional)',"electric/dragon"),
("oricorio_dansen/cumbia/af/cumbia.png",'Oricorio (cumbia)',"water/flying"),
("oricorio_dansen/tango/af/tango.png",'Oricorio (tango)',"dark/flying"),
("oricorio_dansen/samba/af/samba.png",'Oricorio (samba)',"grass/flying"),
("pincurchin_regional/af/pincurchin_regional.png",'Pincurchin (regional)',"poison/rock"),
("lotad_regional/af/lotad_gaucho.png",'Lotad (gaucho)',"ground"),
("lotad_regional/lombre/af/lombre_gaucho.png",'Lombre (gaucho)',"ground/fight"),
("lotad_regional/ludicolo/af/ludicolo_gaucho.png",'Ludicolo (gaucho)',"ground/fight"),
("mrmime_regional/bokser/af/bokser.png",'Mr. Mime (regional)',"fight/psychic"),
("mr_prime/af/mr_prime.png",'"Mr. Prime"',"fight/psychic"),
("jynx_regional/af/jynx_regional.png",'Jynx (regional)',"fairy/dark"),
("poliwag_regional/af/poliwag_regional.png",'Poliwag (regional)',"ice/poison"),
("poliwhirl_regional/af/poliwhirl_regional.png",'Poliwhirl (regional)',"ice/poison"),
("poliwrath_regional/af/poliwrath_regional.png",'Poliwrath (regional)',"ice/poison"),
("grimer_hoenn/af/grimer_hoenn.png",'Grimer (regional)',"poison/ground"),
("muk_hoenn/af/muk_hoenn.png",'Muk (regional)',"poison/ground"),
("dj_rotom/af/dj_rotom.png",'"DJ Rotom"',"electric/steel"),
]),
]
F="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"; FR=F.replace("-Bold","")
ft=ImageFont.truetype(F,36); fn=ImageFont.truetype(F,19); fy=ImageFont.truetype(FR,16)
def icon(t):
    eigen=R0+f"docs/concept/sprites/showcase/types/{t}.png"  # nieuwe types (Cosmic) die nog niet in graphics/types staan
    i=Image.open(eigen if os.path.exists(eigen) else R0+f"graphics/types/{t}.png"); a=i.convert("RGBA")
    if i.mode=="P":
        px=i.load(); ap=a.load()
        for y in range(i.height):
            for x in range(i.width):
                if px[x,y]==0: ap[x,y]=(0,0,0,0)
    return a.resize((a.width*3,a.height*3),Image.NEAREST)
cw=64*S+28; ch=64*S+92; top=95; pad=28; kop=58
W=pad*2+C*cw; H=top+sum(kop+((len(it)+C-1)//C)*ch for _,it in SECTIES)+pad+24
img=Image.new("RGB",(W,H),(246,242,233)); d=ImageDraw.Draw(img)
d.text((pad,28),"Pokémon Fully Ungrounded — nieuwe Pokémon (frontsprites af)",font=ft,fill=(50,40,35))
fs=ImageFont.truetype(F,28); y0=top
for titel,items in SECTIES:
    d.text((pad,y0+12),f"{titel} ({len(items)})",font=fs,fill=(90,60,40)); d.line((pad,y0+50,W-pad,y0+50),fill=(200,185,165),width=2)
    y0+=kop
    for k,(p,n,t) in enumerate(items):
        s=Image.open(p).crop((0,0,64,64))
        if s.mode=="P":
            a=s.convert("RGBA"); px=s.load(); ap=a.load()
            for yy in range(64):
                for xx in range(64):
                    if px[xx,yy]==0: ap[xx,yy]=(0,0,0,0)
        else: a=s.convert("RGBA")
        a=a.resize((64*S,64*S),Image.NEAREST)
        x=pad+(k%C)*cw; y=y0+(k//C)*ch
        d.rounded_rectangle((x+4,y,x+cw-4,y+ch-12),14,fill=(255,253,248),outline=(220,212,198),width=2)
        img.paste(a,(x+14,y+6),a)
        f=fn; z=19
        while d.textlength(n,font=f)>cw-20 and z>11: z-=1; f=ImageFont.truetype(F,z)
        tw=d.textlength(n,font=f); d.text((x+(cw-tw)/2,y+64*S+10),n,font=f,fill=(40,35,30))
        ty=y+64*S+34
        if t=="?":
            tw=d.textlength("type open",font=fy); d.text((x+(cw-tw)/2,ty+12),"type open",font=fy,fill=(120,110,100))
        else:
            ic=[icon(z) for z in t.split("/")]; tot=sum(i.width for i in ic)+6*(len(ic)-1); ix=x+(cw-tot)//2
            for i in ic: img.paste(i,(ix,ty),i); ix+=i.width+6
    y0+=((len(items)+C-1)//C)*ch
d.text((pad,H-34),"Werknamen; rond tot ze ooit worden aangepast. Starterfasen 1–2 tonen het type van de lijn.",font=fy,fill=(140,130,120))
img.save(OUT)
