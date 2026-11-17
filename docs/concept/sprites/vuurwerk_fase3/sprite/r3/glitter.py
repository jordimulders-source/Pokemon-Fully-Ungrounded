# Zoekt de glinstersterren/-spikkels in het lijf van het model: bijna-witte pixels (min-kanaal >= 225) in het origineel,
# binnen het roze/rode lijf van de sprite (niet aan de rand), geclusterd; geeft spritecoordinaten + grootte.
import numpy as np, json; from PIL import Image
a=np.asarray(Image.open('../../referenties/model_v14.png').convert('RGB')).astype(int)
sp=np.asarray(Image.open('stap_gezicht.png'))
W=a.min(2)>=225
H,Wd=W.shape; seen=np.zeros_like(W); out=[]
for y0 in range(120,120+768):
    for x0 in range(106,106+768):
        if not W[y0,x0] or seen[y0,x0]: continue
        st=[(y0,x0)]; seen[y0,x0]=1; c=[]
        while st:
            y,x=st.pop(); c.append((y,x))
            for dy in (-1,0,1):
                for dx in (-1,0,1):
                    q=(y+dy,x+dx)
                    if 0<=q[0]<H and 0<=q[1]<Wd and W[q] and not seen[q]: seen[q]=1; st.append(q)
        if len(c)>2000: continue  # achtergrond
        cy,cx=np.mean(c,0); i,j=int((cx-106)//12),int((cy-120)//12)
        if not(1<=i<63 and 1<=j<63): continue
        if sp[j,i] not in (6,7,8,9,10,11,12): continue
        if (sp[j-1:j+2,i-1:i+2]==0).any(): continue
        if len(c)>=12: out.append((i,j,len(c)))
out.sort(key=lambda t:-t[2]); print(out); json.dump(out,open('glitter_plekken.json','w'))
