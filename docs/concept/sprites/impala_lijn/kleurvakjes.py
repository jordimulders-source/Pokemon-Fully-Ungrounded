from PIL import Image, ImageDraw, ImageFont
P = {
 "A  lavendel/lila + creme": ["#8E7BB5","#B9A8DA","#F2EAD8","#5B4A82"],
 "B  teal/zeegroen + wit":   ["#2E8C86","#5FC2B5","#F4F7F2","#1E5C5A"],
 "C  creme/wit + rood":      ["#E6D3A8","#F6EEDA","#FFFFFF","#C8323A"],
 "D  zwart + goud":          ["#2A2630","#4A4452","#E8C25A","#B08A2E"],
 "E  oranje-koraal + creme": ["#E0683E","#F2A070","#F8EBD6","#8C3A22"],
}
STAAL = ["#5A6470","#9AA6B2","#E6EEF4"]
HOUT  = ["#7A5230","#B08050"]
kol = ["rug","flank","buik","tekening"]
f = ImageFont.load_default(size=18); fs = ImageFont.load_default(size=14)
W,H = 120*7+300, 90*len(P)+110
im = Image.new("RGB",(W,H),"#FFFFFF"); d = ImageDraw.Draw(im)
for i,k in enumerate(kol+["staal (impala/kudu)","","","hout (dikdik)"]):
    if k: d.text((300+i*90 if i<4 else 300+i*90, 20), k, fill="#000", font=fs)
for r,(naam,c) in enumerate(P.items()):
    y = 60+r*90
    d.text((10,y+28), naam, fill="#000", font=f)
    for i,h in enumerate(c+STAAL+HOUT[:1]+HOUT[1:]):
        x = 300+i*90
        d.rectangle([x,y,x+80,y+70], fill=h, outline="#000")
im.save("docs/concept/sprites/impala_lijn/kleurvakjes.png")
