import sys,var,zoom
from PIL import Image
S='/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/3bd5ae97-6ac2-52a5-8d79-9a6104e8993f/scratchpad/s/'
b=list(map(int,sys.argv[2].split(',')))
ims=[zoom.zoom(var.build(k.split('+')),*b,z=20,model=False) for k in sys.argv[3:]]
O=Image.new('RGB',(sum(i.width for i in ims),ims[0].height),'white'); x=0
for i in ims: O.paste(i,(x,0)); x+=i.width
O.save(S+sys.argv[1])
