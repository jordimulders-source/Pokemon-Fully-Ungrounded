# 8x-weergave met coördinatenraster (elke 4 px) om de ogen in Gen 3-bronnen te vinden
import sys
from PIL import Image, ImageDraw, ImageFont
n = sys.argv[1]; x0,y0,x1,y1 = map(int, sys.argv[2:6]); S = 16
im = Image.open(f"graphics/pokemon/{n}/anim_front_gba.png").convert("RGB").crop((x0,y0,x1,y1))
big = im.resize(((x1-x0)*S,(y1-y0)*S), Image.NEAREST); d = ImageDraw.Draw(big); f = ImageFont.load_default(size=11)
for x in range(x0, x1):
    if x % 4 == 0: d.line([((x-x0)*S,0),((x-x0)*S,big.height)], fill=(255,0,0)); d.text(((x-x0)*S+2,2), str(x), fill=(255,0,0), font=f)
for y in range(y0, y1):
    if y % 4 == 0: d.line([(0,(y-y0)*S),(big.width,(y-y0)*S)], fill=(0,0,255)); d.text((2,(y-y0)*S+2), str(y), fill=(0,0,255), font=f)
big.save(f"/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/78dbbfb0-c63e-58cf-88e8-0c28e12348d5/scratchpad/oog_{n}.png")
