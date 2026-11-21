import sys
exec(open('bouw.py').read())
im=Image.fromarray(o.astype('uint8'),'P'); im.putpalette(PAL+[0]*(768-48)); im.save(sys.argv[1],transparency=0)
