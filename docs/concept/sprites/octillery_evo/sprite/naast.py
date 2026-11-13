# naast.py raster out [z]: model BOX-verkleind (64x64) | sprite, op z (standaard 5) + 1x
import cfg,sys
from PIL import Image
a=cfg.read(sys.argv[1]); z=int(sys.argv[3]) if len(sys.argv)>3 else 5
mo=cfg.model64(); sp=cfg.rgba(a,(255,255,255,255))
o=Image.new('RGB',(64*z*2+20+150,64*z),'white')
o.paste(mo.resize((64*z,64*z),Image.NEAREST),(0,0)); o.paste(sp.resize((64*z,64*z),Image.NEAREST),(64*z+10,0))
o.paste(mo,(2*64*z+30,10)); o.paste(sp,(2*64*z+30,90))
o.save(sys.argv[2])
