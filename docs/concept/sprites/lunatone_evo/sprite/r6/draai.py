# r6: driekwart-varianten van r5 (kleur A). Niets getekend: oog en neus zijn bestaande pixels die
# verschoven worden; perspectief door kolommen te schrappen; vrijgekomen lijf = dichtstbijzijnde lijfpixel.
import numpy as np; from PIL import Image; from scipy import ndimage
im=Image.open('../r5/sprite.png'); pal=im.getpalette(); R5=np.array(im)
J,I=np.mgrid[0:64,0:64]
EC=(28.0,35.5)
oogm=(((I-EC[1])**2+(J-EC[0])**2)<=7.6**2)&np.isin(R5,[1,8,9,10])
lab,n=ndimage.label(oogm,structure=np.ones((3,3))); oogm=lab==np.argmax(np.bincount(lab.ravel())[1:])+1
ys,xs=np.where(oogm); print('oog bbox x',xs.min(),xs.max(),'y',ys.min(),ys.max())
STEEN=[3,4,5,7]
def variant(dx,dy,oogschrap,neusk,neus_c0=8):
    o=R5.copy()
    # 1. oog eruit; gat vullen met dichtstbijzijnde lijfpixel (steentint) buiten het oog
    # oogkas (oog + donkere kasschaduw binnen r 9,6) vullen met de dichtstbijzijnde lijfpixel buiten de kas
    kas=(((I-EC[1])**2+(J-EC[0])**2)<=9.6**2)&(R5>0)&~np.isin(R5,[2])
    bron=np.isin(R5,STEEN)&~kas
    _,(iy,ix)=ndimage.distance_transform_edt(~bron,return_indices=True)
    o[kas]=R5[iy[kas],ix[kas]]
    # spaken van de vulling gladstrijken: meest voorkomende steentint in een 5x5-buurt (alleen in de kas)
    for _ in range(2):
        p=o.copy()
        for j,i in zip(*np.where(kas)):
            w=[v for v in p[max(0,j-2):j+3,max(0,i-2):i+3].ravel() if v in STEEN]
            if w: o[j,i]=max(set(w),key=w.count)
    # 2. oog smaller: kolommen uit het midden schrappen (niet door de pupil)
    x0,x1=xs.min(),xs.max(); y0,y1=ys.min(),ys.max()
    E=np.where(oogm,R5,0)[y0:y1+1,x0:x1+1]
    for c in oogschrap: E=np.delete(E,c-x0-(0),axis=1)  # c = oorspronkelijke kolom (aflopend opgeven)
    # 3. oog plakken, verschoven
    ty,tx=np.nonzero(E); o[ty+y0+dy,tx+x0+dx]=E[ty,tx]
    # 4. neus korter: kolommen neus_c0..+k schrappen in rij 24-33, alles links ervan k naar rechts
    if neusk:
        for j in range(24,34):
            row=R5[j].copy(); left=row[:neus_c0].copy()
            new=row.copy(); new[:neus_c0+neusk]=0
            new[neusk:neus_c0+neusk]=left
            o[j,:neus_c0+neusk]=new[:neus_c0+neusk]
    return o
V={'A_licht':dict(dx=-2,dy=0,oogschrap=[38],neusk=2),
   'B_middel':dict(dx=-4,dy=1,oogschrap=[38],neusk=3),
   'C_sterk':dict(dx=-6,dy=1,oogschrap=[39,37],neusk=4)}
out={}
with open('wijzigingen.txt','w') as f:
  f.write('r6: driekwart-varianten van r5 (kleur A). Oog en neus = bestaande pixels, alleen verschoven/kolommen geschrapt.\n')
  for nm,p in V.items():
    o=variant(**p); out[nm]=o
    im2=Image.fromarray(o.astype('uint8'),'P'); im2.putpalette(pal); im2.save(nm+'.png',transparency=0)
    # pixels buiten oog en neus aangepast
    ys2,xs2=np.where(oogm)
    oogzone=np.zeros((64,64),bool); oogzone[min(ys2):max(ys2)+2+p['dy'],min(xs2)+p['dx']:max(xs2)+1]=True
    neuszone=(J>=24)&(J<=33)&(I<8+p['neusk'])
    d=(o!=R5); buiten=d&~oogzone&~neuszone
    f.write(f"{nm}: oog {-p['dx']} px naar links, {p['dy']} px omlaag, kolom(men) {p['oogschrap']} geschrapt (oog {len(p['oogschrap'])} px smaller); "
            f"neus {p['neusk']} px korter (kolommen 8..{7+p['neusk']} geschrapt, punt schuift naar rechts, basis vast); "
            f"oude oogkas (r 9,6, incl. donkere kasschaduw) gevuld met de dichtstbijzijnde lijfpixel erbuiten, daarna meest voorkomende buurtint (5x5) tegen spaken. Gewijzigd totaal {int(d.sum())} px, buiten oog-/neusvak {int(buiten.sum())}; silhouet-diff {int(((o>0)!=(R5>0)).sum())} (alleen de neuspunt).\n")
print(open('wijzigingen.txt').read())
# vel
def on(a,sc):
    i=Image.fromarray(a.astype('uint8'),'P'); i.putpalette(pal); i.info['transparency']=0
    r=i.convert('RGBA'); b=Image.new('RGBA',r.size,(222,222,222,255)); b.alpha_composite(r)
    return b.convert('RGB').resize((64*sc,64*sc),Image.NEAREST)
L=[R5]+[out[k] for k in V]
v=Image.new('RGB',(4*520,512+90),(255,255,255))
for k,a in enumerate(L): v.paste(on(a,8),(k*520,0)); v.paste(on(a,1),(k*520,522)); v.paste(on(a,2),(k*520+80,522-0))
lun=Image.open('../../../../../../graphics/pokemon/lunatone/anim_front.png').convert('RGB').crop((0,0,64,64))
v.paste(lun,(4*520-70,522))
v.save('vel.png')
