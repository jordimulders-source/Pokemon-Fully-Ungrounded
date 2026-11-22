import sys,numpy as np; from PIL import Image
im=Image.open(sys.argv[1]); s=int(sys.argv[3]) if len(sys.argv)>3 else 8
o=Image.open(sys.argv[1]); o.save('/tmp/_t.png',transparency=0)
rgba=Image.open('/tmp/_t.png').convert('RGBA'); bgc=Image.new('RGBA',rgba.size,(200,220,200,255)); bgc.alpha_composite(rgba)
bgc.resize((64*s,64*s),Image.NEAREST).save(sys.argv[2])
