# Vel ronde 1: per variant model-uitsnede (bewerkt model verkleind naar 384) | sprite 6x | sprite 1x; onderaan alles op 1x.
import sys
from PIL import Image, ImageDraw
R=sys.argv[1] if len(sys.argv)>1 else 'r1'
K=['kaal','A','B','C','groot_kaal','groot_A']
T={'kaal':'kale reductie r3b','A':'A: manen r3b +70,+30','B':'B: manen r3b 1,3x lang, +40','C':'C: lokken r3c +90,+20','groot_kaal':'groot: 8 hoornrijen weg','groot_A':'groot + A'}
S=384; V=Image.new('RGB',(S*2+64+40,len(K)*(S+20)+120),(255,255,255)); d=ImageDraw.Draw(V)
for i,k in enumerate(K):
    y=i*(S+20)+16; mk=k.replace('groot_','')
    m=Image.open(f'{R}/model_{mk}.png').convert('RGB').resize((S,S),Image.LANCZOS); V.paste(m,(0,y))
    sp=Image.open(f'{R}/kudu_{R}_{k}.png'); sp.save('/tmp/_t.png',transparency=0)
    s=Image.open('/tmp/_t.png').convert('RGBA')
    V.paste(s.resize((S,S),Image.NEAREST),(S+10,y),s.resize((S,S),Image.NEAREST)); V.paste(s,(2*S+20,y+10),s)
    d.text((4,y-14),T[k],fill=(0,0,0))
y=len(K)*(S+20)+30
for i,k in enumerate(K):
    s=Image.open('/tmp/_t.png') if False else Image.open(f'{R}/kudu_{R}_{k}.png').convert('RGBA'); V.paste(s,(10+i*74,y),s)
V.save(f'{R}/vel.png'); print(V.size)
