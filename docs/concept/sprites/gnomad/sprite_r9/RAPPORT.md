# Gnomad sprite r9: snoromlijning in de eigen tint (22 nov)

Bron: `../sprite_r8/gnomad.png`. Jordi: "maar die snor met roze omringd ziet er ook raar uit".

- 25 pixels donkerroze 6 → bruine snor-selout e (174,130,90), dezelfde tint als de linkersnor en de haarplukken (Dragonfly Cave: omlijning = donkere tint van het object zelf). Zo leest de rand niet meer als roze kader.
  - Bovenrand snor/wang: (23,32) (26,32) (27,33) (28,33) (29,34) (29,35) (30,36) (31,36) (32,36), rand snorpunt (32,37) (31,38).
  - Huidspleet en strengsplitsing: (18,37) (19,36) (20,37) (21,38) (26,38).
  - Onderlijn rechtersnor (22..30,39) (was 6 sinds de eindkeuring r7).
- Geen zwart teruggezet: op 1× en 3× scheidt e de crème snor duidelijk van de roze huid, ook bij de huidspleet.
- `r9.py` bewijst: alle wijzigingen binnen het snorkader (18,32)–(33,39), alleen van 6 naar e, silhouet gelijk; diff 0 elders t.o.v. r8. Zwart totaal blijft 15,4 % (235/1525).
- Bestanden: `gnomad.png`, `vergelijk_8x.png` (r8 | r9 | gewijzigde pixels cyaan omrand), `r9.py`.
