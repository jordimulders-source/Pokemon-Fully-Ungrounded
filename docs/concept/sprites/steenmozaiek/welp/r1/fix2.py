# Ronde 1, handwerk stap 3: voorhoofdkrul (groter, extra graveerlijn), rechteroor, oude ver-oogpixels weg,
# borst-facet, schouderspiraal als echte spiraal, selout aan de lichtkant.
from edit import *
# oude ver-oog-resten weg
put(30,13,"5"); put(31,13,"5")
# voorhoofd: groter gegraveerd krul-motief (dubbele band met graveerlijn, krult links naar binnen)
put(24,19,"888887"); put(24,25,"7")
put(25,16,"887"); put(25,19,"22222"); put(25,24,"76")
put(26,15,"8277776"); put(26,22,"63")
put(27,15,"727"); put(27,18,"3")
put(28,15,"666"); put(28,18,"3")
# rechteroor: grotere donkere binnenkant
put(24,28,"33"); put(25,28,"22"); put(26,28,"22"); put(27,28,"33")
# borst: lichte facet links van de schouderspiraal (model)
for y,s in [(42,"3345"),(43,"3445"),(44,"3455"),(45,"2345"),(46,"2345"),(47,"3345"),(48,"3343")]:
    put(y,21,s)
save()
