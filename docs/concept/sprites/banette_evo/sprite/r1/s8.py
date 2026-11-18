import sys,numpy as np; from view import rgba; from PIL import Image
g=np.load(sys.argv[1]); z=int(sys.argv[3]) if len(sys.argv)>3 else 8
im=rgba(g); bg=Image.new('RGBA',im.size,(255,255,255,255)); im=Image.alpha_composite(bg,im).convert('RGB').resize((64*z,64*z),Image.NEAREST)
im.save(sys.argv[2])
