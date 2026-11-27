# Eindkeuring ek4 (DC, onafhankelijk) – r16

Getoetst: de benen (omtrek, ringen, enkels/voeten, aansluiting romp), de zes groene plekken uit `sprite/r16/NOTITIES.md` en Jordi's krabbel `jordi/krabbel_r16.png` ("2 losse pixels, oog te rechthoekig, lijn in de voet en hoofd/been wat niet helemaal lekker aansluit"). Krabbel gemeten op de figuur: ±5,0 px per spritepixel.

## Benen (r16)
- Trapbeen: links kol 42/41/40/39/38 (runs 6-5-3-2-2), rechts 48/47/46/45 (8-5-4-2): gelijkmatig, 1 px, selout links, zwart rechts. Ringen alleen binnenin, raken netjes de omtrek, zelfde patroon per ring. OK.
- Standbeen: links kol 51/50, rechts 56/57/58: glad. OK. Licht/schaduw consistent. Leest op 1×/2× als getapete Hitmonlee-benen.

## Wijzigingen (19 px, palet ongewijzigd)
| plek | gezien | gedaan |
|---|---|---|
| romp → standbeen rechts (55,43) | zwarte klont van 2 (55+56) = inkeping in de omtrek | (55,43) zwart → 2 (donkerrood, zoals de ringuiteinden) |
| losse pixel verre hand (36,54) | 1 px uitsteeksel links aan de vinger | weg; (37,54) → 2 zodat de vinger omlijnd blijft |
| losse pixel standvoet/enkel (49,55) | 1 px uitsteeksel (hielpunt) links van de enkel | weg; omtrek nu kol 50 rij 52–56, dan de voetrand |
| lijn in de trapvoet | onderrand plooi was een rechte streep van 11 px op rij 6 (kol 37–47), tegen de zwarte zool; gat op (40,5) | (37–39,6) → 4 (basisrood tussen plooi en zool, zoals in het model), (40,5) → 3: plooi is nu een schuine band van 2 px (rij 4: 39–40, rij 5: 37–43, rij 6: 40–47) |
| verre oog | blok 3×5 met gevulde hoeken | ovaal: hoeken (29,24) → 4 en (29,28) → 5; (29,25) → 2, (30,25) → 3, (29,26) → 1, rechterkant (31,27) → 1 (dikkere zwarte rand rechts zoals het model) |
| romp → trapbeen (hoofd/been) | omtrek liep 2 horizontaal (33–34, rij 26) en dan 4 verticaal (kol 35, rij 27–30): hoek | omtrek diagonaal zoals het model: (33,26), (34,27–28), (35,29–30), (36,31); (34,26), (35,27), (35,28) weg, (34,27), (34,28) zwart |

## Open
- Oog blijft met de bovenkant tegen de romprand (model: heel smalle oranje rand ertussen; geen plek zonder de koepel te verschuiven).
- Twijfelpunten maker (buiging trapbeen hoger dan model ≤0,8 px; standbeen 6 → 8 naar de voet; (d) vlak) geaccepteerd: binnen het model.

Bestanden: `ek4.png`, `ek4_8x.png`, `vel4.png` (r16 8× | ek4 8× met gewijzigde px omkaderd | model | Gen 3 + 1×/2× licht/donker).
