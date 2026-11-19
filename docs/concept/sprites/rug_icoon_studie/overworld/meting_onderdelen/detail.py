import sys
from PIL import Image
from rooster_ow import detail
sp=sys.argv[2]; B=[detail(sp,k) for k in (0,2,4)]
img=Image.new('RGB',(sum(b.width for b in B)+40,max(b.height for b in B)),(255,255,255)); x=0
for b in B: img.paste(b,(x,0)); x+=b.width+20
img.save(sys.argv[1])
