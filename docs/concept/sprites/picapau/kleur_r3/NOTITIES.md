# Picapau kleur r3: notities (maker, 5 nov)

Bestanden: `maak_r3.py` (handgekozen wijzigingen op r2-A/r2-B → `raster_A.txt`, `raster_B.txt`), `bouw.py` (→ `picapau_A.png`, `picapau_B.png`, `normal.pal`), `controle.py A|B` → `controle_A.txt`, `controle_B.txt`, `vel.py` → `vel.png` (1x boven, 8x onder: Taillow, r2-A, r3-A, r3-B, Pikachu). r2 onaangeroerd.

## Palet
- **e (iris) vervalt.** In het oog: e → k (2 px, (28,19) (28,20)); verder pixel voor pixel Pikachu.
- **Let op, kuiftoppen:** de binnentint van de kappen was óók e. Die 6 px, (33,5) (38,5) (32,6) (33,6) (37,6) (38,6), zijn nu **G (64,64,72)**: dezelfde posities, maar 1 tint lichter. Dat is Pikachu's eigen oortoptint. Vorm en posities zijn onveranderd; als Claude/Jordi de oude tint wil, kan het alleen met k (helemaal zwart). Vleugelschouder: 0 px gewijzigd.
- Vrije plek = **h bleke hoorn (240,232,184)**. **g = warm grijs (150,140,116)**: donkere hoorn (snavelboven- en onderrand) én lichte pootkleur (de nabije poot is daardoor warmer grijs dan in r2).

## Wijzigingen (A en B)
1. **Snavel**: bleke hoorn h, boven- en onderrand donkere hoorn g, punt en onderlijn zwart; de aanzet bij de kop is h, lichter dan de kop (2). Geen goudbruine bovenrand meer.
2. **Naad onder de wang weg**: de horizontale schaduwband (rij 26 x29–33, rij 27 x23–28) is weg; er blijft een sikkel aan de schaduwkant (rij 25 x33–34, rij 26 x31–32, rij 27 x31–33, rij 28 x33), die aansluit op de schaduw langs de vleugel. Kop en lijf lopen in elkaar over.
3. **Vleugel**: de derde schubbenrij (rij 35–37) is weg, er blijven twee duidelijke rijen; daaronder effen bruin tot de slagpennen.
4. **B, verre poot**: poot 2 px (35–36, rij 45), tenen rij 46 x35–37 en drie teentoppen op rij 47 (x34, 36, 38) met zwart ertussen, alles in de schaduwtint G. Kolom 33 lucht (rij 46–47).

## Controle
- **A**: silhouet buiten de zones 0; in de zones 7 (de kuiftoppen en snavelpunt van r2). Open randen 0, losse pixels 0, clusters < 3 px 0. 825 px.
- **B**: 21 silhouetwijzigingen (budget 30); lijst in controle_B.txt. Ten opzichte van r2-B: (38,47) erbij, (34,47) terug zoals in het silhouet. Open randen 0, losse 0, clusters 0. 829 px.
- Kanttekening: de 2 lichte teenpixels van de nabije poot (29,46) (28,47) tellen nu als "ok" omdat g ook omlijning (donkere hoorn) is; in r2 werden ze gemeld. Ze staan er nog.

## Zwakke punten (eerlijk)
1. **A-snavel**: leest nu als bleke snavel, maar blijft dun (silhouet, 3 px); als beitel leest alleen B echt.
2. **B, verre poot**: de tenen zijn op 8x duidelijk, op 1x is de poot een donker plukje met één teentje zichtbaar; "2 tenen leesbaar" haal ik op 1x maar net.
3. **Nabije poot** is warm grijs (gedeelde tint met de donkere hoorn); leest iets bruiner dan Pikipek/Taillow-poten.
4. Kuiftop-binnentint 1 tint lichter (zie palet), door het vrijmaken van e.
5. Vleugel blijft een lange strook langs de rug (modelvorm).

## Lessen
- Voordat je een tint "vrijmaakt": grep in het raster waar hij nog meer staat (e stond ook in de kuiftoppen).
- Een sikkel die alleen aan de schaduwkant ligt en aansluit op een bestaande schaduw scheidt de kop zonder naad.
