# r2/vel2.py : zelfde vel als ../vel.py (zelfde opbouw als r1/vel.png), met het r2-palet uit bouw2.py.  Vanuit sprite2/: python3 r2/vel2.py
import sys,runpy; sys.path.insert(0,'r2'); sys.path.insert(0,'.')
import bouw2
sys.argv=['vel.py','r2']; runpy.run_path('vel.py',run_name='__main__')
