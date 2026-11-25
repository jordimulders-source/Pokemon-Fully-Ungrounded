# brons/zilver/goud-ramps op elke vachtkleur, om te zien of zilver opvalt
from PIL import Image, ImageDraw, ImageFont
VACHT = {"A lila":"#8E7BB5","B teal":"#2E8C86","C creme":"#E6D3A8","D zwart":"#2A2630","E koraal":"#E0683E"}
MET = {"brons":["#5C3418","#9A5A2A","#D08A4A","#F2C08A"],
       "zilver":["#3C4450","#8A96A6","#D4DEE8","#FFFFFF"],
       "goud":["#6A4A10","#B8861E","#EBC24A","#FFF2A8"]}
f = ImageFont.load_default(size=16)
cw, ch = 300, 120
im = Image.new("RGB",(150+cw*3, 40+ch*len(VACHT)),"#FFFFFF"); d = ImageDraw.Draw(im)
for j,m in enumerate(MET): d.text((150+j*cw+10,12), m, fill="#000", font=f)
for i,(vn,vc) in enumerate(VACHT.items()):
    y = 40+i*ch
    d.text((10,y+50), vn, fill="#000", font=f)
    for j,(mn,ramp) in enumerate(MET.items()):
        x = 150+j*cw
        d.rectangle([x,y,x+cw-10,y+ch-10], fill=vc)
        # een gebogen 'hoorn' als strook van ramp-banden
        for k in range(len(ramp)):
            d.rectangle([x+40+k*8, y+20, x+40+k*8+7, y+90], fill=ramp[k])
        for k in range(len(ramp)):
            d.rectangle([x+120+k*30, y+30, x+120+k*30+28, y+80], fill=ramp[k], outline="#000")
im.save("docs/concept/sprites/impala_lijn/metaal_op_vacht.png")
