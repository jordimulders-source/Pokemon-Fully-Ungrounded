# p4: keuring p3 MOET 1-2 (7 px) + MAG heup schaduwkant, toegepast door Claude
from PIL import Image
im=Image.open('p3/welp_p3.png'); px=im.load()
E={(29,43):3,(30,43):3,(31,43):8,            # spiraalhart: groef naar midden
   (25,39):3,(25,45):3,(36,39):3,(36,45):3,  # ring ronder
   (47,50):7,(47,51):7,(47,52):7}            # MAG: heup schaduwkant
for k,v in E.items(): print(k,px[k],'->',v); px[k]=v
im.save('p4/welp_p4.png',transparency=0)
a=Image.open('p4/welp_p4.png').convert('RGBA'); a.resize((512,512),Image.NEAREST).save('p4/welp_p4_8x.png')
bg=Image.new('RGBA',a.size,(236,234,224,255)); bg.alpha_composite(a)
o=Image.new('RGBA',(512+20+128,512),(255,255,255,255)); o.paste(bg.resize((512,512),Image.NEAREST),(0,0)); o.paste(bg.resize((128,128),Image.NEAREST),(532,0)); o.paste(bg,(532,150))
o.save('p4/vel.png')
