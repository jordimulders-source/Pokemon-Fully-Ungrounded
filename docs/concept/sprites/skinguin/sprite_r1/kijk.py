# naast elkaar: model (box-verkleind naar 61 px, op 8x) | sprite op 8x
import sys; from PIL import Image
m=Image.open('../model/model.png').convert('RGB').crop((12*10.24+9.25-10.24+1,16*10.24+9.25-10.24+1,87*10.24+9.25-10.24+1,91*10.24+9.25-10.24+1)) if False else Image.open('natief.png').convert('RGB').crop((12,16,87,91))
m=m.resize((61*8,61*8),Image.NEAREST)
s=Image.open(sys.argv[1]).convert('RGB').resize((512,512),Image.NEAREST)
v=Image.new('RGB',(61*8+512+16,512),(255,255,255)); v.paste(m,(0,24)); v.paste(s,(61*8+16,0)); v.save(sys.argv[2])
