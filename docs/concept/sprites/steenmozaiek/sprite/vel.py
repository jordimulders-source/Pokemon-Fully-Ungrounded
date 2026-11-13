# vel: sprite 8x | model verkleind op zelfde hoogte | sprite 1x
import sys; from PIL import Image
s=Image.open(sys.argv[1]).convert('RGBA'); m=Image.open('../referenties/model_gekozen.png').convert('RGBA')
S=8; big=s.resize((64*S,64*S),Image.NEAREST)
mm=m.resize((512,512),Image.LANCZOS)
V=Image.new('RGBA',(512*2+90,512),(255,255,255,255)); V.paste(big,(0,0),big); V.paste(mm,(512,0))
V.paste(s,(1030,10),s); V.paste(s.resize((128,128),Image.NEAREST),(965,300),s.resize((128,128),Image.NEAREST))
V.convert('RGB').save(sys.argv[2])
