"""Handbewerking van dj_rotom.txt: python3 zet.py y x tekens [y x tekens ...]"""
import sys
L=open('dj_rotom.txt').read().split('\n')
a=sys.argv[1:]
for i in range(0,len(a),3):
    y,x,s=int(a[i]),int(a[i+1]),a[i+2]; r=list(L[1+y])
    for k,c in enumerate(s):
        if c!='_': r[x+k]=c
    L[1+y]=''.join(r)
open('dj_rotom.txt','w').write('\n'.join(L))
