# Hulpje: handmatige pixelbewerkingen op het tekstraster. Gebruik: from edit import *; ...; save()
g=[list(l.rstrip('\n')) for l in open('welp_r2.txt')]
def put(y,x,s):
    for i,c in enumerate(s):
        if c!=' ': g[y][x+i]=c
def save(): open('welp_r2.txt','w').write('\n'.join(''.join(r) for r in g)+'\n')
