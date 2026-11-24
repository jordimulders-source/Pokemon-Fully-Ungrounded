# Bouwt een ronde: kale reductie -> oog -> antennes/gewrichten -> png. Gebruik: python3 bouw.py rN
# Voorbereiding (eenmalig): natief.py (meting raster), klassen.py -> klassen2.py (zones.png staat vast). Daarna per ronde dit script.
import subprocess, sys, numpy as np
R=sys.argv[1]
run=lambda *a: subprocess.run(['python3',*a],check=True)
import os
if os.environ.get('SAT_MODEL'):   # r5: ander model -> zones en klassen eerst opnieuw (klassen zonder zone -> zones -> klassen met zone)
    subprocess.run(['python3','klassen.py'],check=True,env={**os.environ,'SAT_NOZONE':'1'})
    run('zones.py'); run('klassen.py'); run('klassen2.py')
run('kaal.py','0.5','0.34',R+'/k')
run('oog.py',R+'/k.npy',R+'/e.npy')
run('beschermd.py',R+'/e.npy',R+'/a.npy')
run('schoon.py',R+'/a.npy',R+'/k.npy',R+'/s.npy',R+'/k_F.npy')
run('paneelrand.py',R+'/s.npy',R+'/k_F.npy',R+'/p.npy')
run('licht.py',R+'/p.npy',R+'/l.npy')
run('lijftint.py',R+'/l.npy',R+'/p.npy',R+'/t0.npy')
run('randlo.py',R+'/t0.npy',R+'/k_F.npy',R+'/t.npy')
run('toon.py',R+'/t.npy',R+'/sprite.png')
run('vel.py',R+'/sprite.png',R+'/vel.png',*sys.argv[2:3])
run('check.py',R+'/sprite.png')
run('compact.py',R+'/sprite.png',R+'/sprite.png')
