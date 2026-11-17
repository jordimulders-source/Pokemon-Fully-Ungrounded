# Per spritepixel: zwartfractie (lum<55), achtergrondfractie (bijna wit, niet het vruchtvlees), en de dichtstbijzijnde paletkleur
# van het gemiddelde van de niet-zwarte, niet-achtergrond modelpixels. Gebruik: python3 kaart.py MODEL X0 Y0 X1 Y1
import sys,numpy as np; from PIL import Image; from box import win
P=Image.open('../sprite_r2/pitahaya3_r2.png').getpalette(); P=np.array(P[:48]).reshape(16,3).astype(float)
ch='.#drpPgGhHwWoyYs'
M=np.asarray(Image.open(sys.argv[1]).convert('RGB')).astype(float); x0,y0,x1,y1=map(int,sys.argv[2:6])
rows={'kleur':[],'zwart':[],'bg':[]}
for Y in range(y0,y1):
    a=b=c=''
    for X in range(x0,x1):
        w=win(M,X,Y); l=w@[.299,.587,.114]; sat=w.max(1)-w.min(1)
        zw=l<55; bg=(l>235)&(sat<20); n=len(w)
        rest=w[~zw&~bg]
        if len(rest)==0: k=1 if zw.mean()>.3 else 0
        else: k=1+int(((P[1:]-rest.mean(0))**2).sum(1).argmin())
        if bg.mean()>.5: k=0
        a+=ch[k]; b+=str(min(9,int(zw.mean()*10))); c+=str(min(9,int(bg.mean()*10)))
    rows['kleur'].append(a); rows['zwart'].append(b); rows['bg'].append(c)
print('    '+''.join(str(x%10) for x in range(x0,x1))+'   zwart/10'+' '*(x1-x0-8)+'   achtergrond/10')
for i,Y in enumerate(range(y0,y1)): print('%2d  %s   %s   %s'%(Y,rows['kleur'][i],rows['zwart'][i],rows['bg'][i]))
