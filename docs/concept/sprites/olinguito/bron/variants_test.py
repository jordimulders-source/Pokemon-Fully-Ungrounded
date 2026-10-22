import sys
sys.path.insert(0,'/home/user/projectgrounded/tools/concept/sprites')
import spritelib as L
from PIL import Image
a,pal=L.load_png(sys.argv[1]); z=4
alb=list(pal); alb[1:5]=[(255,255,255),(230,222,222),(180,172,180),(123,115,131)]
blk=list(pal); blk[1:5]=[(115,106,123),(74,68,82),(49,45,57),(33,30,41)]; blk[5:8]=[(213,205,189),(180,164,148),(131,115,106)]
W=Image.new('RGBA',(3*64*z*2+40,64*z),(255,255,255,255))
i=0
for p in (pal,alb,blk):
    for f in (a[:64],a[64:128]):
        bg=L.checker_bg(64*z,64*z,4*z); bg.alpha_composite(L.scaled(L.rgb_img(f,p),z)); W.paste(bg,(i*(64*z+6),0)); i+=1
W.save(sys.argv[2])
