# Eindkeuring 2 (eindkeuring2/RAPPORT.md) reparaties 1-6 op eind_r1/potoo.png, met controle op de oude waarde.
import numpy as np; from PIL import Image
im=Image.open('../eind_r1/potoo.png'); a=np.array(im); pal=im.getpalette()
R=[(37,3,2,1),(42,9,4,1),(22,40,1,2),(22,38,2,8),(22,39,2,4),(44,33,5,6),(44,34,5,6),(44,35,5,6),(43,46,6,5),(43,47,6,5),
   (24,40,8,7),(25,40,8,7),(27,40,8,7),(24,41,4,6),(25,41,4,6),(34,21,2,4)]
b=a.copy(); fout=[]
for x,y,old,new in R:
    if a[y,x]!=old: fout.append((x,y,int(a[y,x]),old)); continue
    b[y,x]=new
print('gewijzigd',int((b!=a).sum()),'afwijkend:',fout)
o=Image.fromarray(b,'P'); o.putpalette(pal); o.save('potoo.png',transparency=0)
z=8; sh=Image.new('RGB',(2*64*z+10,64*z+80),(255,255,255))
for i,arr in enumerate((a,b)):
    t=Image.fromarray(arr,'P'); t.putpalette(pal); m=Image.fromarray(((arr!=0)*255).astype('uint8'))
    bg=Image.new('RGB',(64,64),(255,255,255)); bg.paste(t.convert('RGB'),(0,0),m)
    sh.paste(bg.resize((64*z,64*z),Image.NEAREST),(i*(64*z+10),0)); sh.paste(bg,(i*(64*z+10)+5,64*z+8))
    dk=Image.new('RGB',(64,64),(40,40,48)); dk.paste(t.convert('RGB'),(0,0),m); sh.paste(dk,(i*(64*z+10)+80,64*z+8))
sh.save('voor_na.png')
