"""Headless mGBA-hulp. Nodig: pip install mgba (libmgba staat al op het systeem).
Bewegen: press(richting, hold=12..16); een korte tik draait de speler alleen om."""
import mgba.core, mgba.image, mgba.log, sys
mgba.log.silence()
from PIL import Image
KEYS={'A':0,'B':1,'SELECT':2,'START':3,'RIGHT':4,'LEFT':5,'UP':6,'DOWN':7,'R':8,'L':9}
class Emu:
    def __init__(self, rom):
        self.core=mgba.core.load_path(rom)
        self.img=mgba.image.Image(240,160); self.core.set_video_buffer(self.img)
        self.core.reset()
    def run(self,n):
        for _ in range(n): self.core.run_frame()
    def press(self,key,hold=4,after=20):
        self.core.set_keys(*[KEYS[k] for k in key.split('+')])
        self.run(hold); self.core.set_keys(); self.run(after)
    def shot(self,path):
        self.img.to_pil().convert('RGB').resize((480,320),Image.NEAREST).save(path)

def load(e,path):
    e.core.load_raw_state(open(path,'rb').read())

def debug_script(e, k, settle=300):
    """Start debug-script k (1-8) via START -> DEBUG -> Scripts."""
    e.press('START', after=30); e.press('A', after=30)
    for _ in range(5): e.press('DOWN', after=6)
    e.press('A', after=30)
    for _ in range(k - 1): e.press('DOWN', after=6)
    e.press('A', after=30); e.run(settle)
