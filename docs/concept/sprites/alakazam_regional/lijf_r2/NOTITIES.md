# Charlatan-Alakazam: lijf r2 (vervangers voor het strikje)

Basis: `basis_O1r.txt` (= `../lijf_r1/samengevoegd/O1r.txt`). Jordi: "de strik is dus nog steeds een strik en geen onderdeel van het lichaam", "wat betreft strik vervanging, teken eens wat en doe ook een stropdas patroon proberen", "geef me meerdere opties".

Bouwen: `python3 strik.py` (schrijft `opt_S1..S8.txt/.png` en bewijst de diff), daarna `python3 vel.py`. Controle: `python3 controle.py opt_S3.txt`.

## Werkwijze
- Eerst gaat het strikje weg (`LEEG`): een witte keel met kinschaduw `a` onder de kinlijn en `a` langs de rechterrand. Daarna tekent elke optie haar rood of zwart erop.
- Geen eigen omlijning, geen knoop. Tinten t/r/s voor rood en n/m/k voor zwart. Licht van linksboven: lichte kant links, donkere sikkel rechts en onder.

## Opties (alleen x26–35, y25–33; vorm gelijk)
- **S1 keelwam:** een rode flap die vastzit aan de hele kinrand. In het midden is hij 1 rij hoog, naar links en rechts hangt hij lager (2–3 rijen), met een slagschaduw `a` eronder.
- **S2 sleutelbeenvlekken:** twee rode banen vanaf de hals langs de sleutelbeenderen. Ze komen samen in een punt op het borstbeen (rij 30).
- **S3 keelvlek (roodborstje):** de hele keel is rood, vast aan de kin, met een ronde onderkant op de bovenborst (rij 30) en een slagschaduw `a`.
- **S4 rode stropdastekening:** een streep van 3 px onder de kin die taps toeloopt naar 1 px (rij 33), over het midden van de plaat. Twee tinten: r, met s rechts.
- **S5 zwarte stropdastekening (koolmees) met rood accent:** 2 rijen rood onder de kin, daaronder een taps toelopende streep in n/m/k.
- **S6 geen rood:** alleen de witte keel en plaat.
- **S7 (eigen idee):** een rode ruit (kaartsymbool) als tekening op het borstbeen, zoals de ster en tekens op Kadabra.
- **S8 (eigen idee):** S5 zonder rood, een zwarte streep vanaf de kin.

## Controle
- Alle opties: alpha-diff 0, 0 px buiten de zone x26–36 / y24–38.
- Open randen 0, losse o 0. Palet 13 kleuren + transparant.
- Clusters < 3 px: alleen de 13 die al in O1r stonden, geen nieuwe.

## Hoe sterk leest het als lijf (oordeel maker)
- **S3** leest het sterkst als lijf: een gekleurde keel die bij de kop hoort, zoals bij een vogel.
- **S6** leest ook als lijf, maar dan is het rood weg.
- **S1** zit aan de kin vast, maar de twee hangende lobben lezen nog half als strikje.
- **S7** leest als tekening (Abra-familie, kaarten), maar ook een beetje als embleem.
- **S2** leest als een V-hals of halsketting, dus als kleding.
- **S4, S5 en S8** lezen als stropdas. Dat was de vraag, maar het blijft een kledingbeeld. S8 is het rustigst.
