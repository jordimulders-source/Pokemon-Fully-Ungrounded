# r9: MOETEN 1-3 uit sprite_r8/EINDKEURING.md (10 px), verder diff 0 met r8.
from PIL import Image
im=Image.open('sprite_r8/swablu_r8.png').copy()
zet={(28,37):7,(29,37):7,(28,38):12,(29,38):12,            # 1 V-inkeping onderrand vogel
     (14,38):12,(13,39):12,(13,42):12,(14,43):12,          # 2 linkerbuitenrand onderwolk
     (40,40):3,(43,40):3}                                  # 3 korrel naad rechtsonder
for p,i in zet.items(): im.putpixel(p,i)
im.save('sprite_r9/swablu_r9.png',transparency=0)
a=Image.open('sprite_r9/swablu_r9.png').convert('RGBA');bg=Image.new('RGBA',(64,64),'white');bg.alpha_composite(a);bg.resize((512,512),Image.NEAREST).save('sprite_r9/swablu_r9_8x.png')
