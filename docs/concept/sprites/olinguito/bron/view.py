import sys
sys.path.insert(0,'/home/user/projectgrounded/tools/concept/sprites')
import spritelib as L
from PIL import Image
a,pal=L.load_png(sys.argv[1]); z=int(sys.argv[3]) if len(sys.argv)>3 else 6
fr=[a[:64],a[64:128]]
W=Image.new('RGBA',(64*z*2+8+140,64*z),(255,255,255,255))
for i,f in enumerate(fr):
    bg=L.checker_bg(64*z,64*z,4*z); bg.alpha_composite(L.scaled(L.rgb_img(f,pal),z)); W.paste(bg,(i*(64*z+8),0))
for i,f in enumerate(fr):
    bg=L.checker_bg(64,64,4); bg.alpha_composite(L.rgb_img(f,pal)); W.paste(bg,(2*(64*z+8)+4,i*70))
W.save(sys.argv[2])
