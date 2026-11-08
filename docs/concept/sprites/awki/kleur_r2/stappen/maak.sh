# keten ronde 2: r1.txt -> (masker D samengevoegd met omlijning 1; D wordt karmijn) -> e_rep2.txt -> r2.txt
cd "$(dirname "$0")"
tr 'D' '1' < r1.txt > basis2.txt
python3 ed.py basis2.txt r2.txt e_rep2.txt | grep -v "SILHOUET-afwijking 2[34] 2[3-6] \." 
cp r2.txt ../raster.txt
python3 png.py ../raster.txt ../normal.pal ../awki.png > /dev/null
