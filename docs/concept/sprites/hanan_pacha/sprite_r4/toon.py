import numpy as np, sys; from PIL import Image
sys.path.insert(0,'../sprite_r3'); 
PAL=[(240,240,236),(26,16,20),(124,76,18),(196,148,53),(229,184,79),(246,214,124),(206,188,180),(244,240,234),(128,28,42),(166,48,63),(208,99,104),(186,82,38),(222,118,50),(50,41,52),(204,192,148),(92,80,96)]
def rgb(o): return Image.fromarray(np.array(PAL,'uint8')[o])
def zoom(o,box,s): return rgb(o).crop(box).resize(((box[2]-box[0])*s,(box[3]-box[1])*s),Image.NEAREST)
