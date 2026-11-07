# keten ronde 3: r2.txt (= kleur_r2/raster.txt) -> e_rep3.txt (handwerk, ed.py-formaat) -> r3.txt = ../raster.txt -> ../awki.png
cd "$(dirname "$0")"
python3 ed.py r2.txt r3.txt e_rep3.txt | grep -v "SILHOUET-afwijking 2[34] 2[3-6] \."
cp r3.txt ../raster.txt
python3 png.py ../raster.txt ../normal.pal ../awki.png > /dev/null
