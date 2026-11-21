# dekking r2 tegen het modelsilhouet (r1 = reductie van het model): '-' model wel / r2 niet, '+' r2 wel / model niet, letters = veer
import sys, numpy as np
r1=np.load('r1_kls.npy'); o=np.load(sys.argv[1]); own=np.load('own.npy')
ch='abcdefghijklmnopq'; m=p=0
for y in range(8,48):
  s=''
  for x in range(62):
    if r1[y,x] and not o[y,x]: s+='-'; m+=1
    elif o[y,x] and not r1[y,x]: s+='+'; p+=1
    elif own[y,x]>=0: s+=ch[own[y,x]]
    elif o[y,x]: s+='#'
    else: s+=' '
  if len(sys.argv)>2: print('%2d '%y+s)
print('model wel/r2 niet',m,' r2 wel/model niet',p)
