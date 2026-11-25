# lichaamskleur brons/zilver/goud: rug, flank, buik, tekening
from PIL import Image, ImageDraw, ImageFont
R = {"dikdik: brons":["#6E3E1E","#A8682F","#D99A5C","#F4DDBE","#3A2214"],
     "impala: zilver":["#4A5260","#8C98A8","#C8D2DE","#F4F7FA","#262A33"],
     "kudu: goud":["#7A5414","#BE8C22","#E8BE48","#FBF0C8","#4A3008"]}
kol = ["rug donker","rug","flank","buik","tekening"]
f = ImageFont.load_default(size=16)
im = Image.new("RGB",(180+5*90, 40+3*90),"#FFFFFF"); d = ImageDraw.Draw(im)
for i,k in enumerate(kol): d.text((180+i*90,12),k,fill="#000",font=f)
for r,(n,c) in enumerate(R.items()):
    y=40+r*90; d.text((10,y+28),n,fill="#000",font=f)
    for i,h in enumerate(c): d.rectangle([180+i*90,y,180+i*90+80,y+70],fill=h,outline="#000")
im.save("docs/concept/sprites/impala_lijn/lichaamskleur.png")
