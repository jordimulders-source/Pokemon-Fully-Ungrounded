# wijzig_extra.py (door wijzig.py ingelezen): opschoning en selout
zet(26,21,'c','gezicht: los crème-puntje (1 px) in de wangschaduw, model dC/Cc -> crème-schaduw')
zet(55,44,'Y','staartvlam: lichtgeel vlamhart viel in de crèmeklasse, model = vlamkern')
# gekleurde selout aan de lichtkant (linksboven) van de bruine benen/hoeven: een tint donkerder dan het vlak eronder
for (x,y) in [(14,43),(15,43),(12,44),(11,45),(10,47),(17,56),(16,57),(15,58)]:
    zet(x,y,'h','selout lichtkant been/hoef (vlak eronder lichtbruin)')
for (x,y) in [(19,43),(20,44),(21,44),(22,44),(23,45),(24,45),(10,48),(10,49),(11,50)]:
    zet(x,y,'H','selout lichtkant been (vlak eronder middenbruin)')
# kleine hoornhaak links van het gezicht: de zwart/donkergrijs-regel maakte hem zwart; model = bruine hoorn met zwarte lijn
zet(16,18,'h','hoornhaak: model hH/hH')
zet(16,20,'h','hoornhaak: model hh/hh (was donkergrijs)')
zet(17,20,'H','hoornhaak: model H#/hd')
zet(17,21,'h','hoornhaak naar de kop: model #g/dh')
zet(18,21,'h','hoornhaak naar de kop: model hh/h#')
