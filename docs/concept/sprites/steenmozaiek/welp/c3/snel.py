# Snel vel: gegeven pngs naast elkaar op 1x, 3x en 6x (wit).
import sys
from PIL import Image
fs=sys.argv[2:]; uit=sys.argv[1]
def wit(f):
    im=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im); return bg.convert('RGB')
W=len(fs)*(64*6+10); o=Image.new('RGB',(W,64*6+64*3+64+30),'white')
for i,f in enumerate(fs):
    m=wit(f).crop((0,0,64,64)) if wit(f).size==(64,64) else wit(f).resize((64,64))
    x=i*(64*6+10); o.paste(m.resize((384,384),Image.NEAREST),(x,0)); o.paste(m.resize((192,192),Image.NEAREST),(x,394)); o.paste(m,(x+200,394))
o.save(uit)
