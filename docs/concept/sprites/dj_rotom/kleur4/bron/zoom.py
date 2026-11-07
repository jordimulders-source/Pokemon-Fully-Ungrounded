"""Bliksem-uitsnede: 16x, 2x en 1x op licht en donker (scratch)."""
import sys
from PIL import Image
im=Image.open('../dj_rotom.png').convert('RGBA').crop((14,4,36,32))
w=Image.new('RGB',(22*16+120,28*16),(255,255,255))
for i,bgc in enumerate([(236,236,228,255),(40,44,56,255)]):
    bg=Image.new('RGBA',im.size,bgc); bg.alpha_composite(im)
    if i==0: w.paste(bg.resize((352,448),Image.NEAREST).convert('RGB'),(0,0))
    w.paste(bg.resize((44,56),Image.NEAREST).convert('RGB'),(360,i*130)); w.paste(bg.convert('RGB'),(410,i*130))
w.save(sys.argv[1])
