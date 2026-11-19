# Ronde 6: handgezette tonen binnen het bruine lijf (rij: 'x0-x1:index').
# Indexen: 5 schaduw/sikkel, 6 midden, 7 licht, E hooglicht (nieuw). Alleen lijf-binnenpixels mogen veranderen;
# het script weigert elke wijziging daarbuiten (randpixels van het lijf, kop, poten, staart, lijnen).
import os
D=os.path.dirname(os.path.abspath(__file__))
R5=[l.rstrip('\n') for l in open(os.path.join(D,'..','r5','r5.txt'))]
R=[list(r) for r in R5]
def T(x,y): return not(0<=x<64 and 0<=y<64) or R5[y][x]=='0'
mag={(x,y) for y in range(64) for x in range(64) if R5[y][x] in '567' and not any(T(x+dx,y+dy) for dx,dy in [(0,-1),(-1,0),(1,0),(0,1)])}
H={
31:'37-41:7',
32:'35-45:7 46-47:6',
33:'29:7 32-42:7 43-44:E 45-46:7 47-48:6',
34:'28:6 29-37:7 38:6 39-41:7 42-44:E 45-47:7 48:6 49:5',
35:'28:6 29:7 30-32:E 33-36:7 37-39:6 40-41:7 42-45:E 46-47:7 48-49:5',
36:'28:6 29:7 30-33:E 34-35:7 36-40:6 41-42:7 43-44:E 45-46:7 47-48:5',
37:'28:6 29:7 30-32:E 33-34:7 35:7 36:5 37-39:6 40-41:7 42-43:E 44:7 45:6 46-47:5',
38:'28:6 29-31:E 32-33:7 34:6 35-36:5 37-39:6 40:7 41-42:E 43-44:7 45:6 46-47:5',
39:'27:6 28:7 29-30:E 31-33:7 34:6 35:6 36-37:5 38-39:6 40-41:7 42:E 43:7 44-45:6 46-48:5',
40:'27:6 28-32:7 33-35:6 36:5 37:6 38-39:6 40-42:7 43-45:6 46-48:5',
41:'26:5 27:6 28-31:7 32-35:6 36-37:5 38-39:6 40-41:7 42-45:6 46-48:5',
42:'26-27:5 28:6 29-30:7 31-35:6 36-38:5 39:6 40:7 41-45:6 46-48:5',
43:'25-27:5 28:6 29-30:7 31-35:6 36-38:5 39-45:6 46-48:5',
44:'24-27:5 28-29:6 30:7 31-34:6 35-38:5 39-45:6 46-48:5',
45:'22-26:5 27-33:6 34-38:5 39-44:6 45-48:5',
46:'21-25:5 26-32:6 33-39:5 40-43:6 44-48:5',
47:'22-24:5 25-31:6 32-39:5 40-42:6 43-48:5',
48:'23-25:5 26-31:6 32-36:5 40-43:6 44-47:5',
49:'23-24:5 25-30:6 31-34:5 41-46:5',
50:'24:5 25-30:6 31-34:5 42-45:5',
51:'24:5 25-30:6 31-34:5',
52:'25:5 28-30:6 31-34:5',
53:'30-31:6 32-33:5',
}
for y,s in H.items():
  for tok in s.split():
    rng,c=tok.split(':'); a,b=(rng.split('-')+[rng])[:2]
    for x in range(int(a),int(b)+1):
      assert (x,y) in mag, ('bevroren pixel',x,y)
      R[y][x]=c
open(os.path.join(D,'r6.txt'),'w').write('\n'.join(''.join(r) for r in R)+'\n')
diff=[(x,y) for y in range(64) for x in range(64) if R[y][x]!=R5[y][x] and (x,y) not in mag]
print('wijzigingen buiten het lijf:',len(diff))
