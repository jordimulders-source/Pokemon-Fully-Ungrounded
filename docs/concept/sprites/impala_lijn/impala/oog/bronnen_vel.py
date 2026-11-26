# Gen 3-viervoeters naast elkaar (frame 1, 4x) als bron voor het impala-oog
from PIL import Image, ImageDraw, ImageFont
N = ["stantler","rapidash","girafarig","absol","suicune","raikou","entei"]
S = 4; f = ImageFont.load_default(size=18)
out = Image.new("RGB", (len(N)*64*S, 64*S+30), "#FFFFFF"); d = ImageDraw.Draw(out)
for i, n in enumerate(N):
    im = Image.open(f"graphics/pokemon/{n}/anim_front_gba.png").convert("RGBA").crop((0,0,64,64))
    bg = im.getpixel((0,0))
    im = Image.eval(im, lambda v: v)  # kopie
    px = im.load()
    for y in range(64):
        for x in range(64):
            if px[x,y] == bg: px[x,y] = (255,255,255,255)
    out.paste(im.resize((64*S,64*S), Image.NEAREST), (i*64*S, 30))
    d.text((i*64*S+8, 5), n, fill="#000", font=f)
out.save("docs/concept/sprites/impala_lijn/impala/oog/bronnen.png")
