# hulpje: nieuw | r17 | model op spriteschaal, uitsnede op schaal s (argv: uit x0 y0 x1 y1 s)
import sys; sys.argv_k=sys.argv[:]; sys.argv=['bouw']
exec(open('eindkeuring_dc/bouw.py').read().replace("if __name__=='__main__'","if False"))
a=sys.argv_k; out=a[1]; x0,y0,x1,y1,s=map(int,a[2:7])
r17=Image.open(SRC).convert('RGB'); mo=Image.fromarray(mos.astype('uint8'))
ims=[rgb(n),r17,mo]
W=(x1-x0)*s; H=(y1-y0)*s
vel=Image.new('RGB',(3*W+40,H),(255,255,255))
for i,im in enumerate(ims): vel.paste(im.crop((x0,y0,x1,y1)).resize((W,H),Image.NEAREST),(i*(W+20),0))
vel.save(out)
