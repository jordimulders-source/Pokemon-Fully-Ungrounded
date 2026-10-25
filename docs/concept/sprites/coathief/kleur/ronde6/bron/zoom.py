"""Hulpweergave: sprite op 8x op licht en donker + 1x (alleen om zelf te kijken)."""
import os, sys
from PIL import Image
H=os.path.dirname(os.path.abspath(__file__))
im=Image.open(os.path.join(H,'../coathief.png')).convert('RGBA')
S=8
W=Image.new('RGBA',(64*S*2+40+140,64*S),(236,236,230,255))
d=Image.new('RGBA',(64*S,64*S),(40,40,60,255))
big=im.resize((64*S,64*S),Image.NEAREST)
W.alpha_composite(big,(0,0)); d.alpha_composite(big); W.paste(d,(64*S+20,0))
W.alpha_composite(im,(64*S*2+40,20)); 
d2=Image.new('RGBA',(64,64),(40,40,60,255)); d2.alpha_composite(im); W.paste(d2,(64*S*2+40,100))
W.alpha_composite(im.resize((128,128),Image.NEAREST),(64*S*2+40,180))
W.save(sys.argv[1] if len(sys.argv)>1 else '/tmp/zoom.png')
