# Sapa Inca – ronde 6b (reparatie op ronde 6)

Basis: `ronde6/sapa_inca.txt`; de reparatie staat onderaan in het blok "ronde 6b". Bestanden: `sapa_inca.png/.txt`, `bouw.py`, `controle6b.py` (diff + stafcontrole), `overlay.py` → `overlay.png` (rode lijnen op ronde 6 en 6b), `vel.py` → `vel.png` (lijf op 6× naast ronde 6), `kijk.py`, `uitlijning.npy` (uitlijning van ronde 6: 8,25 px per spritepixel, +11/+6).

Afkeuring van ronde 6: onder de vleugelpunt hing de staf als lange, dunne, losse sliert (rij 43–51). Jordi eerder: "dus minder lange sliert", "niet een verbinding maken naar iets wat niet bestaat".

## Wat er veranderde (alleen x12–26, rij 42–53)
- De vleugelpunt sluit op rij 46 af met een doorlopende zwarte onderrand (x14–18). Daaronder komt de staf maar **2 rijen** tevoorschijn: rij 47 x14–18 (3 px schacht die al naar rechts buigt), rij 48 x17–19. Daarna verdwijnt hij achter het lijf op (20,48).
- De omtrek linksonder loopt als ronde boog onder de staf door: (16,48) → (17,49) → (19,50) → (21,51) → (23,52) → dij (24,53). Zo overlapt het lijf de staf en hangt er niets meer in de lucht. Het lijf is daar weer iets voller dan in ronde 6, maar zonder bult: de stappen in de omtrek lopen geleidelijk op (1, 2, 2, 2, 1).
- De oude sliert (rij 48–51, x14–23) is weg.

## Controles (`controle6b.py`)
- **Stafpixels onder de vleugel:** (14–18,47) en (17–19,48). **Geen stafpixel onder rij 47 grenst aan transparant**: links van (17,48) ligt de zwarte lijfrand, eronder het donkere lijf en rechts ervan (20,48) donker lijf.
- **Diff t.o.v. ronde 6:** binnen de zone x12–26, rij 42–53 **33 px**; buiten de zone **0 px** (kroon, gezicht en ogen, rechtervleugel, buik, poten en de staf boven de hand ongewijzigd).
- **Silhouet:** +12 / −10 px (1620 → 1622): −10 waar de sliert hing, +12 voor de ronde lijfrand onder de staf.
- 0 open randen.

## Zelf gekeken (1× en 6× naast ronde 6, overlay)
- Geen sliert meer. De staf komt kort onder de vleugelpunt uit en verdwijnt meteen achter het lijf; op 1× is het een klein roestbruin haakje onder de hand.

## Eerlijk: wat nog niet klopt
- **Omtrek linksonder ligt 2–4 px buiten Jordi's rode boog** (de boog loopt van (20,45) via (22,48) naar (24,50); de nieuwe rand ligt op (16,48), (17,49), (19,50)). Dat was nodig om de staf echt achter het lijf te laten verdwijnen zonder dat er staf in de lucht hangt; het lijf is daar dus weer iets voller.
- **Staf onder de vleugel:** het zichtbare stuk is kort en roestbruin (de gouden schacht is daar niet meer te zien). Op 1× lees je het als een haakje en niet meer als dezelfde staf als erboven.
- De bocht is erg kort (2 rijen); "zacht" is op deze schaal beperkt.

## Lessen
- "Geen stafpixel onder rij N aan transparant" betekent dat het lijf onder het zichtbare stafeind door moet lopen. Een staf die 6 px opzij moet naar een verder weg liggende lijfrand kan daarom niet zonder het lijf daar voller te maken. Leg die afweging vooraf voor.
