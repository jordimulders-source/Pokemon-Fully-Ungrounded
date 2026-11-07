"""Kleine wijzigingen op het opgeslagen model (muriqui.blend), zonder herbouw (Jordi 5 nov: "waarom maak je niet
telkens kleine wijzigingen?"). Opent de .blend, past kleuren/objecten aan, maakt een snelle render en slaat op.
Gebruik: python3 pas_aan.py [--fur #hex] [--oog #hex] [--pupil schaal] [--uit naam] [--groot] [--niet-opslaan]"""
import argparse, os, sys, time
import bpy

HIER = os.path.dirname(os.path.abspath(__file__))
a = argparse.ArgumentParser()
a.add_argument('--fur'); a.add_argument('--oog'); a.add_argument('--pupil', type=float)
a.add_argument('--uit', default='snel'); a.add_argument('--groot', action='store_true'); a.add_argument('--niet-opslaan', action='store_true')
args = a.parse_args(sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv[1:])
t0 = time.time()
bpy.ops.wm.open_mainfile(filepath=os.path.join(HIER, 'muriqui.blend'))

def kleur(naam, hexkleur):
    m = bpy.data.materials[naam]; b = m.node_tree.nodes['Principled BSDF']
    h = hexkleur.lstrip('#'); rgb = [(int(h[i:i + 2], 16) / 255) ** 2.2 for i in (0, 2, 4)] + [1]
    b.inputs['Base Color'].default_value = rgb
    if b.inputs['Emission Strength'].default_value > 0: b.inputs['Emission Color'].default_value = rgb

if args.fur: kleur('fur', args.fur)
if args.oog: kleur('eye', args.oog)
if args.pupil:
    for o in bpy.data.objects:
        if o.name.startswith('pupil'): o.scale = [s * args.pupil for s in o.scale]
sc = bpy.context.scene
sc.render.resolution_x = sc.render.resolution_y = 1440 if args.groot else 560
sc.cycles.samples = 12 if args.groot else 6
sc.render.filepath = os.path.join(HIER, f'render_{args.uit}.png')
bpy.ops.render.render(write_still=True)
if not args.niet_opslaan:
    bpy.ops.wm.save_mainfile(compress=True)
print(f'KLAAR in {time.time() - t0:.0f} s')
