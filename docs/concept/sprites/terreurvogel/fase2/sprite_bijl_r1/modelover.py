# model op spriteschaal: geeft (img, functie) voor overlay; spritepx = OX + (natief - X0)*S, natief = (modelpx - 9.25)/10.24
import numpy as np; from PIL import Image
import lib
def model_op(schaal):
    m=Image.open('../gemini/r1_eenvoud.png').convert('RGB')
    f=lib.S/10.24*schaal                       # schermpx per modelpx
    # modelpx -> sprite x: lib.OX + ((mx-9.25)/10.24 - lib.X0)*lib.S
    ox=(lib.OX+((0-9.25)/10.24-lib.X0)*lib.S)*schaal; oy=(lib.OY+((0-9.25)/10.24-lib.Y0)*lib.S)*schaal
    z=m.resize((round(1024*f),round(1024*f)),Image.LANCZOS)
    can=Image.new('RGB',(64*schaal,64*schaal),(255,255,255)); can.paste(z,(round(ox),round(oy)))
    return can
