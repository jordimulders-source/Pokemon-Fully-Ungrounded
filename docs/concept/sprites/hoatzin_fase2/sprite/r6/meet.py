# zwart/donker binnen de figuur: aandeel index 1 en 2 (hele figuur en binnen = niet aan transparant grenzend)
import sys, numpy as np; from PIL import Image
for f in sys.argv[1:]:
    a=np.array(Image.open(f)); fg=a!=0; p=np.pad(fg,1); inn=fg&p[:-2,1:-1]&p[2:,1:-1]&p[1:-1,:-2]&p[1:-1,2:]
    print(f, 'figuur',fg.sum(), 'idx1 %.1f%% (binnen %.1f%%)'%(100*(a==1).sum()/fg.sum(),100*((a==1)&inn).sum()/inn.sum()),
          'idx2 %.1f%% (binnen %.1f%%)'%(100*(a==2).sum()/fg.sum(),100*((a==2)&inn).sum()/inn.sum()),
          'aantallen',{i:int((a==i).sum()) for i in range(1,16)})
