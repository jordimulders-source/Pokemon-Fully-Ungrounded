# Natief raster van Gemini claydol_r3 (ongewijzigd), met natief.py uit claydol_sprite_r1.
import sys; sys.path.insert(0,'../claydol_sprite_r1'); from natief import natief
from PIL import Image
out,gr=natief('../gemini/claydol_r3.png'); print('pitch x %.3f fase %.2f | y %.3f fase %.2f'%gr, out.shape)
Image.fromarray(out).save('natief.png')
