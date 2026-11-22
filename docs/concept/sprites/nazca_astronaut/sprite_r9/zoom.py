import sys; from PIL import Image
im=Image.open(sys.argv[1]).convert('RGBA'); bg=Image.new('RGBA',(64,64),(232,236,228,255)); bg.alpha_composite(im)
bg.crop((14,22,46,50)).resize((32*16,28*16),Image.NEAREST).save(sys.argv[2])
