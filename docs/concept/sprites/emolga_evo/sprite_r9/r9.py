import sys; sys.path.insert(0,'/tmp/claude-0/-home-user-Pokemon-Fully-Ungrounded/df5125ac-9381-5d71-af17-ce82baab011f/scratchpad')
from ronde import run
R=[]
# (2) oor: punt licht (4), onderdeel basis (3), schaduw rechts (2); x6 = gekleurde selout
R+= [('oor',43,7,'44'),('oor',44,7,'442'),('oor',45,7,'432'),('oor',46,7,'332'),('oor',47,7,'3332'),('oor',48,7,'3322')]
# (1) lijf onderkant: basis 3 linksboven, schaduw 2 rechtsonder, diagonale grens
R+= [('lijf',44,25,'33322'),('lijf',45,22,'3333332'),('lijf',46,22,'333332'),('lijf',47,22,'3332222'),('lijf',48,21,'2332222'),('lijf',49,21,'232222')]
# (4) band: boven 3 (licht), lager links 3 rechts 2, onderaan bij het lijf 2
R+= [('band',38,36,'332'),('band',39,35,'332'),('band',40,34,'332'),('band',41,33,'322'),('band',42,32,'322'),('band',43,31,'322'),('band',44,30,'222'),('band',45,29,'222')]
# (3) geel nabije vleugel: 5 waar hij onder het lijf/band verdwijnt
R+= [('geel',41,32,'5'),('geel',42,30,'55'),('geel',43,30,'5')]
run('sprite_r8/A0.png','sprite_r9',R)
