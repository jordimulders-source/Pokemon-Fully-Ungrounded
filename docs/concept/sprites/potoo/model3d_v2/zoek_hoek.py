"""Rendert de kop op een raster van kijkhoeken (yaw, pitch) voor een gegeven kop_op; gebruik met score.py."""
import os, sys, math
sys.argv = [sys.argv[0]] + sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else sys.argv
import potoo3d as M
import bpy
uit = sys.argv[1]; os.makedirs(uit, exist_ok=True)
P = M.params('A')
for kv in os.environ.get('PARAM', '').split(','):
    if kv: k_, v_ = kv.split('='); P[k_] = float(v_)
po = M.Potoo(P); M.bouw_mesh(po); cam = M.camera()
cam.data.ortho_scale = 46
for yaw in [int(v) for v in os.environ.get('YAWS', '-52,-62,-72').split(',')]:
    for pitch in [int(v) for v in os.environ.get('PITCHES', '-4,-12,-20').split(',')]:
        M.kijk(cam, yaw, pitch, doel=(2, 0, -2))
        bpy.context.scene.render.filepath = os.path.join(uit, f'k{int(P["kop_op"])}_y{-yaw}_p{-pitch}.png')
        bpy.ops.render.render(write_still=True)
