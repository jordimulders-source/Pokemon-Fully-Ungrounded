# pxraster.py x0 y0 x1 y1 : per spritepixel: spritecode | model gem-helderheid | model rgb (afgerond /10)
import sys,numpy as np; sys.path.insert(0,'sprite/r1'); import meet
S=np.load('sprite/r1/A.npy'); ch='.#gGh5YyLdtsCPWQ'
x0,y0,x1,y1=map(int,sys.argv[1:5])
for y in range(y0,y1):
    row=[]
    for x in range(x0,x1):
        g,p,m,c=meet.px(x,y); row.append(f"{ch[S[y,x]]}{int(g):3d}({int(c[0]):3d},{int(c[1]):3d},{int(c[2]):3d})")
    print(y,' '.join(row))
