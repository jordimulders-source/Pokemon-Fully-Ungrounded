"""Onderdelenkaart van B1 (lama-fase-3-methode): elk materiaal een vlakke eigen kleur, zelfde camera als B1.
Draaien: python3.11 labels.py  -> B1/labels.png (512 px)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import picapau, bpy
L = dict(geel=(1, 1, 0), vleugel=(0.4, 0.2, 0), staart=(1, 0.4, 0), wang=(1, 0, 0), kuiftop=(0, 0, 0),
         snavel=(0, 1, 1), oog=(0, 0, 1), glans=(1, 1, 1), poot=(0.5, 0.5, 0.5), schub=(1, 0.8, 0.8))
for k, v in L.items(): picapau.KLEUR[k] = v
wortel = picapau.bouw_picapau(); wortel.rotation_euler = (0, 0, picapau.math.radians(30))
picapau.camera_licht(512, 8)
sh = bpy.context.scene.display.shading
sh.light = 'FLAT'; sh.show_object_outline = False; sh.show_cavity = False
bpy.context.scene.render.filepath = os.path.abspath('B1/labels.png')
bpy.ops.render.render(write_still=True)
