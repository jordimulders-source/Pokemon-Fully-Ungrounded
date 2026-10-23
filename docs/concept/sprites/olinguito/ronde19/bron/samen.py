"""Zet kop19.txt op het lijf van ronde 18 (oude kop weg) -> samen_f1.txt (werkbestand om daarna met de hand te zuiveren)."""
import sys
OX,OY=int(sys.argv[1]),int(sys.argv[2])
b=[list(l.rstrip('\n')) for l in open('r18_f1.txt')]
for y in range(64):
    for x in range(64):
        if x<=39 and y<=38: b[y][x]='.'
k=[l.rstrip('\n') for l in open('kop19.txt') if l.strip()]
for y,l in enumerate(k):
    for x,c in enumerate(l):
        if c!='.': b[OY+y][OX+x]=c
open('samen_f1.txt','w').write('\n'.join(''.join(r) for r in b)+'\n')
