# toon.py IN UIT : sprite 8x naast natief model op dezelfde schaal
import sys; from PIL import Image
im=Image.open(sys.argv[1]).convert('RGBA'); b=Image.new('RGBA',(64,64),(200,230,200,255)); b.alpha_composite(im)
n=Image.open('../natief.png').convert('RGB')
sh=Image.new('RGB',(1040,512),'white'); sh.paste(b.convert('RGB').resize((512,512),Image.NEAREST),(0,0))
# natief bbox 10..188 x 19..180 -> sprite: w=60 at x0=2, bottom row 62
nn=n.crop((3,-9,195,183)).resize((512,512),Image.NEAREST); sh.paste(nn,(528,0)); sh.save(sys.argv[2])
