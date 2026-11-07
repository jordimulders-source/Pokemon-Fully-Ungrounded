import sys
from PIL import Image
out=sys.argv[1]; fs=sys.argv[2:]
c=Image.new('RGB',(len(fs)*(32*9+8),48*9),(255,255,255))
for i,f in enumerate(fs):
    im=Image.open(f).convert('RGBA'); bg=Image.new('RGBA',(64,64),(235,235,225,255)); bg.alpha_composite(im)
    c.paste(bg.crop((18,4,50,52)).resize((32*9,48*9),Image.NEAREST),(i*(32*9+8),0))
c.save(out)
