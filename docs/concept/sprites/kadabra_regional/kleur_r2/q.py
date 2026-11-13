# q.py sx0 sy0 sx1 sy1: modelcellen (letters van grid10 + r=rood, w=wit binnen de figuur, '.'=achtergrond) voor een sprite-uitsnede.
# Kop: per celkolom de spritekolom (tientallen/eenheden); links per celrij de spriterij. Een spritepixel is 1,516 cel.
import sys,numpy as np
sys.path.insert(0,'../model'); from grid10 import cls
from meet import C,L,fig,CX0,CY0,SX0,SY0,SUB,BLK
x0,y0,x1,y1=map(int,sys.argv[1:5])
sx=lambda c:int((c+.5-CX0)*SUB/BLK+SX0); sy=lambda r:int((r+.5-CY0)*SUB/BLK+SY0)
cols=[c for c in range(100) if x0<=sx(c)<x1]; rws=[r for r in range(100) if y0<=sy(r)<y1]
def ch(r,c):
    if not fig[r,c]: return ' '
    if C[r,c,0]>C[r,c,2]+25: return 'r'
    if L[r,c]>222: return 'w'
    if L[r,c]<20: return '#'
    if L[r,c]<50 : return 'K'   # zwart materiaal basis
    k=cls(C[r,c]); return 'k' if k in 'ok' else k
print('     '+''.join(str(sx(c)//10) for c in cols)); print('     '+''.join(str(sx(c)%10) for c in cols))
for r in rws: print('%2d %2d'%(sy(r),r)+''.join(ch(r,c) for c in cols)+'|')
