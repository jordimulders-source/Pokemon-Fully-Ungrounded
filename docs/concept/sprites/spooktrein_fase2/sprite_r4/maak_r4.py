# r4 = r3 + groen spookwiel uit model r5 (wiel_r5.py, T=0.45); controle bevriezing; sprite.png/8x
import numpy as np, subprocess; from PIL import Image
subprocess.run(['python3','wiel_r5.py','0.45'],check=True,capture_output=True)
r3i=Image.open('../sprite_r3/sprite.png'); r3=np.asarray(r3i).astype(int); o=np.load('wiel_T0.45.npy')
d=o!=r3
wolk=np.isin(r3,[3,4,5]); wolk[:27]=False
print('gewijzigd',d.sum(),'| rij 0-26:',d[:27].sum(),'| buiten wolkzone:',(d&~wolk).sum())
print('per overgang:',{f'{a}->{b}':int(((r3==a)&(o==b)).sum()) for a in (3,4,5) for b in (3,4,5) if a!=b})
im=Image.fromarray(o.astype(np.uint8),'P'); im.putpalette(r3i.getpalette()); im.save('sprite.png',transparency=0)
im=Image.open('sprite.png').convert('RGBA'); bg=Image.new('RGBA',(64,64),'white')
Image.alpha_composite(bg,im).convert('RGB').resize((512,512),Image.NEAREST).save('sprite_8x.png')
im=Image.open('sprite.png'); print(im.mode,im.info.get('transparency'),'kleuren',len(im.getcolors()))
