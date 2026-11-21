# r8 (Jordi 21 nov): "middenlinks van de witte pixel moet een andere kleur zijn dan linksboven en linksonder, kijk naar hoe de originele swablu dat doet"
# Echte Swablu (anim_front): glans (31,34); middenlinks (30,34) = donkere lijntint (56,104,128), linksboven/-onder (30,33)/(30,35) = middenblauw.
# Hier: vanaf r7A; middenlinks (27,28) -> selout 12 (46,60,78), linksboven/-onder (27,27)/(27,29) blijven 7 (vogel donker).
from PIL import Image
im=Image.open('sprite_r7/swablu_r7A.png').copy()
im.putpixel((27,28),12)
im.save('sprite_r8/swablu_r8.png',transparency=0)
a=Image.open('sprite_r8/swablu_r8.png').convert('RGBA');bg=Image.new('RGBA',(64,64),'white');bg.alpha_composite(a);bg.resize((512,512),Image.NEAREST).save('sprite_r8/swablu_r8_8x.png')
w=Image.new('RGB',(560,260),'white')
w.paste(Image.open('sprite_r8/swablu_r8.png').convert('RGB').crop((22,22,35,35)).resize((260,260),Image.NEAREST),(0,0))
w.paste(Image.open('../../../../graphics/pokemon/swablu/anim_front.png').convert('RGB').crop((25,28,38,41)).resize((260,260),Image.NEAREST),(290,0))
w.save('sprite_r8/oog_vs_swablu.png')
