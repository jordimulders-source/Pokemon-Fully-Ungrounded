# r3/zoom3.py x0 y0 x1 y1 uit.png [k] : model (met raster) | r3-sprite, met het r3-palet
import sys,runpy; sys.path.insert(0,'r3'); sys.path.insert(0,'.')
import bouw3
a=sys.argv[1:]; sys.argv=['zoom.py','r3/raster.txt']+a; runpy.run_path('zoom.py',run_name='__main__')
