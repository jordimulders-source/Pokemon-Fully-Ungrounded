from PIL import Image, ImageDraw
PAL = {'.': None, 'K': (16, 16, 16), 'L': (57, 24, 16), 'S': (98, 65, 49), 'B': (139, 90, 65), 'H': (164, 115, 74),
       'g': (189, 172, 156), 'G': (148, 123, 106), 'q': (115, 98, 90), 'Q': (90, 82, 74),
       'E': (104, 24, 40), 'e': (160, 40, 56), 'P': (205, 140, 140), 'p': (164, 98, 106), 'C': (230, 222, 205), 'W': (248, 248, 248)}
def show(grid, path, z=8):
    im = Image.new('RGB', (64 * z, 64 * z), (152, 208, 160)); d = ImageDraw.Draw(im)
    for y in range(64):
        for x in range(64):
            c = PAL.get(grid[y, x])
            if c: d.rectangle([x * z, y * z, x * z + z - 1, y * z + z - 1], fill=c)
    im.save(path)
