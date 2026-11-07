# Eindkeuring (eindkeuring/RAPPORT.md) reparaties 1-7 op kandidaat/potoo.png; elke pixel met controle op de oude waarde.
import numpy as np; from PIL import Image
im=Image.open('../kandidaat/potoo.png'); a=np.array(im); pal=im.getpalette()
R=[(1,[(29,40),(30,40),(31,40),(32,40)],8,7),(1,[(29,41),(31,41),(32,41)],8,6),(1,[(34,28),(34,29),(34,30),(34,31),(34,32)],8,7),
   (2,[(25,29),(24,30),(31,33),(32,33),(31,38),(25,39)],2,4),(2,[(33,40),(30,41)],2,3),
   (3,[(35,28),(35,29),(37,28)],2,3),
   (4,[(44,31),(44,32)],5,6),(4,[(42,36),(42,37),(43,38),(43,39)],7,6),
   (5,[(38,4),(38,5),(39,6)],8,7),(6,[(25,23)],3,5),(7,[(39,56),(39,58)],3,5)]
b=a.copy(); n=0; fout=[]
for k,ps,old,new in R:
    for x,y in ps:
        if a[y,x]!=old: fout.append((k,x,y,int(a[y,x]),old)); continue
        b[y,x]=new; n+=1
print('gewijzigd',n,'afwijkend (niet gewijzigd):',fout)
o=Image.fromarray(b,'P'); o.putpalette(pal); o.save('potoo.png',transparency=0)
z=8; sh=Image.new('RGB',(2*64*z+10,64*z+80),(255,255,255))
for i,arr in enumerate((a,b)):
    t=Image.fromarray(arr,'P'); t.putpalette(pal); m=Image.fromarray(((arr!=0)*255).astype('uint8'))
    bg=Image.new('RGB',(64,64),(255,255,255)); bg.paste(t.convert('RGB'),(0,0),m)
    sh.paste(bg.resize((64*z,64*z),Image.NEAREST),(i*(64*z+10),0)); sh.paste(bg,(i*(64*z+10)+5,64*z+8))
    dk=Image.new('RGB',(64,64),(40,40,48)); dk.paste(t.convert('RGB'),(0,0),m); sh.paste(dk,(i*(64*z+10)+80,64*z+8))
sh.save('voor_na.png')
