# keten ronde 2: r2b.txt -> (masker D samengevoegd met omlijning 1; D wordt karmijn) -> e_rep3.txt -> r3.txt
cd "$(dirname "$0")"
tr 'D' '1' < r2b.txt > basis2.txt
python3 ed.py basis2.txt r3.txt e_rep3.txt | grep -v "SILHOUET-afwijking 2[34] 2[3-6] \." 
cp r3.txt ../raster.txt
python3 png.py ../raster.txt ../normal.pal ../awki.png > /dev/null
