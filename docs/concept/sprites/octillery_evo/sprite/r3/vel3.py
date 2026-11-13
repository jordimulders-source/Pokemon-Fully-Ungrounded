# vel3.py: r3-vel met r3-palet (zelfde opbouw als ../vel.py)
import sys,os; D=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,D); sys.path.insert(0,D+'/..')
import pal
sys.argv=['vel.py',D]; os.chdir(D+'/..')
exec(open(D+'/../vel.py').read())
