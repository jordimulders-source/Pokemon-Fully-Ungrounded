"""Getrouwe Gen 3-tegenhanger van MissingNo: GEEN spritedata, maar trainerdata uit de ROM
(net als MissingNo in Gen 1) als 4bpp-sprite gelezen, met het ?-palet (index 0, zoals MissingNo
het palet van index 0 kreeg). Vorm uit een maat-/startfout zoals in Gen 1 (deel van de buffer
blijft leeg). Trainertabel in Ungrounded 1.0 testfix8: rond 0x650000-0x657000 (namen om de 0x30).
Gebruik: python3 gen3_trainerdata.py ROM UITMAP"""
import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0,os.path.dirname(__file__))
from gen3_missingno import pal_none
from gen3_afmeting import lees
rom=open(sys.argv[1],'rb').read(); uit=sys.argv[2]; os.makedirs(uit,exist_ok=True); pal=pal_none()
starts=[0x651600,0x651800,0x652000,0x653400,0x654800,0x655c00,0x656b00,0x656e00]
fouten=[(8,0,'goed'),(7,0,'7/rij'),(8,-600,'start -600'),(7,-900,'7/rij -900'),(9,-300,'9/rij -300')]
sh=Image.new('RGB',(len(fouten)*72+8,len(starts)*72+16),(255,255,255)); d=ImageDraw.Draw(sh)
for j,f in enumerate(fouten): d.text((8+j*72,2),f[2],fill=(0,0,0))
for i,s in enumerate(starts):
    data=rom[s:s+2048]
    for j,(pr,st,lab) in enumerate(fouten):
        im=lees(data,pal,pr,st); x,y=8+j*72,14+i*72; sh.paste(im,(x,y),im)
        im.save(f'{uit}/t{s:X}_{pr}_{st}.png')
sh.resize((sh.size[0]*2,sh.size[1]*2),Image.NEAREST).save(f'{uit}/vel.png')
