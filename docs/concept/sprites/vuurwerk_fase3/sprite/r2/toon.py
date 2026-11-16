import sys; from PIL import Image
for f in sys.argv[1:]:
    im=Image.open(f); im.save('/tmp/_t.png',transparency=0) if False else None
    im=im.convert('RGBA'); bg=Image.new('RGBA',im.size,(255,255,255,255)); bg.alpha_composite(im)
    s=8 if im.size[0]<=64 else 4
    bg.resize((im.size[0]*s,im.size[1]*s),Image.NEAREST).save(f.replace('.png','_8x.png'))
