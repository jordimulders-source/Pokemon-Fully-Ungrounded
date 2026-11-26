# Poten-studie: onderste deel van Gen 3-viervoeters met korte/dunne poten op 6x (alleen _gba-sprites)
from PIL import Image, ImageDraw, ImageFont
N = ["ponyta","rapidash","girafarig","stantler","mareep","eevee","vulpix","poochyena","mightyena","electrike","manectric","skitty","houndour","absol","smeargle","zigzagoon"]
S = 6; f = ImageFont.load_default(size=14); cols = 4
cel = (64*S, 30*S+20)
vel = Image.new("RGB", (cols*(cel[0]+8), ((len(N)+cols-1)//cols)*(cel[1]+8)), "white"); d = ImageDraw.Draw(vel)
for i,n in enumerate(N):
    try: im = Image.open(f"graphics/pokemon/{n}/anim_front_gba.png").convert("RGBA").crop((0,0,64,64))
    except FileNotFoundError: continue
    bg = im.getpixel((0,0)); px = im.load()
    for y in range(64):
        for x in range(64):
            if px[x,y] == bg: px[x,y] = (255,255,255,255)
    x0 = (i%cols)*(cel[0]+8); y0 = (i//cols)*(cel[1]+8)
    vel.paste(im.convert("RGB").crop((0,34,64,64)).resize((64*S,30*S), Image.NEAREST), (x0, y0+20))
    d.text((x0+4, y0+2), n, fill="black", font=f)
vel.save("docs/concept/sprites/impala_lijn/impala/poten_studie/poten_gen3.png")
