import sys; from PIL import Image
im=Image.open(sys.argv[1]); s=int(sys.argv[3]) if len(sys.argv)>3 else 8
im.save('/tmp/_z.png',transparency=0) if False else None
r=im.convert('RGBA'); bgc=Image.new('RGBA',r.size,(255,255,255,255)); bgc.alpha_composite(r)
bgc.convert('RGB').resize((im.width*s,im.height*s),Image.NEAREST).save(sys.argv[2])
