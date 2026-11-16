# Laatste handmatige pixelcorrecties (x, y, kleur) na de controle op losse pixels/randen.
import sys
from gio import from_txt, to_txt, CH
G=from_txt(sys.argv[1])
P=[(32,15,'W'),(28,16,'W'),(30,16,'W'),
   (22,21,'w'),(22,22,'w'),            # lavendel spleet tussen kleine punt en massa
   (18,24,'S'),                        # bovenlijn kop dicht
   (25,32,'n'),(32,34,'j'),(22,38,'n'),(29,39,'K'),
   (19,38,'W'),(20,38,'W'),
   (29,45,'W'),(24,45,'D'),
   (15,55,'W'),(23,55,'W'),(30,55,'W'),(11,55,'M'),(12,56,'M'),
   # lichtvlakken van de onderste punten (G, H) doorgetrokken in de donkere massa, zoals in het model
   (39,40,'j'),(40,40,'j'),(37,41,'j'),(38,41,'j'),(35,42,'j'),(36,42,'j'),(34,43,'j'),
   (37,45,'j'),(38,45,'j'),(35,46,'j'),(36,46,'j'),(34,47,'j'),
]
for x,y,c in P: G[y,x]=CH.index(c)
to_txt(G,sys.argv[2])
