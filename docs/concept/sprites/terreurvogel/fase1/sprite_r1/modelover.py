# Model op het 64-raster (spritecoordinaten) geschaald, voor vergelijken: modelbeeld(k) -> RGBA 64k x 64k
import numpy as np; from PIL import Image
from lib import S,OX,OY,X0,Y0
P=10.24; B0=9.77-10.24
M=Image.open('../gemini/model_kandidaat.png').convert('RGB')
def modelbeeld(k):
    # sprite X -> modelpx = B0 + P*(X0 + (X-OX)/S)
    sc=P/S                        # modelpx per spritepx
    x0=B0+P*(X0-OX/S); y0=B0+P*(Y0-OY/S)
    box=(x0,y0,x0+64*sc,y0+64*sc)
    return M.transform((64*k,64*k),Image.EXTENT,box,Image.BILINEAR,fillcolor=(255,255,255))
def model1x():
    # model op 1x: per spritepixel meest voorkomende kleur (box)
    sc=P/S; x0=B0+P*(X0-OX/S); y0=B0+P*(Y0-OY/S)
    big=M.transform((64*8,64*8),Image.EXTENT,(x0,y0,x0+64*sc,y0+64*sc),Image.BILINEAR,fillcolor=(255,255,255))
    return big.resize((64,64),Image.BOX)
