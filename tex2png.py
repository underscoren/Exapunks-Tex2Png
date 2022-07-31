from tex import TexReader, ColorFmt
from sys import argv,stderr
from pathlib import Path
from json import dumps
from array import array
from itertools import islice
import png

# reads tex file and returns TexFile instance
def readFile(filename):
    pathobj = Path(filename)

    if not pathobj.is_file():
        print(f"{filename} is not a valid file", file=stderr)
        exit(1)

    with pathobj.open("rb") as f:
        reader = TexReader(f)
        return reader.read()

# returns png.Image instance from TexFile
def getPng(texfile):
    width, height = texfile.data
    pixels = array("B")
    pixels.frombytes(texfile.pixels)

    # pypng expects pixels to be list of lists in format pixels[width][height]
    def rows(it, length):
        it = iter(it)
        return iter(lambda: tuple(islice(it, length)), ())

    pixelbytes = 4 if texfile.colorFmt.value == ColorFmt.RGBA.value else 1
    colormode = "RGBA" if texfile.colorFmt.value == ColorFmt.RGBA.value else "L"
    pixels = list(rows(pixels, width*pixelbytes))
    pixels.reverse() # flip image vertically

    return png.from_array(pixels, mode=colormode, info={"width": width, "height": height})

# return TexFile metadata as JSON string
def getJson(texfile):
    return dumps({
        "data": texfile.data,
        "colorFmt": texfile.colorFmt.value,
        "display": texfile.display,
        "bounds": texfile.bounds,
        "cropOff": texfile.cropOff,
        "link": texfile.link
    }, indent=2)

# reads in a tex file and outputs a png, with json metadata
def tex2png(filename):
    filepath = Path(filename)
    texfile = readFile(filename)
    
    pngfilepath = filepath.with_name(filepath.stem + ".png")
    pngfile = getPng(texfile)
    pngfile.save(pngfilepath)

    jsonfilepath = filepath.with_name(filepath.stem + ".json")
    jsondata = getJson(texfile)

    with jsonfilepath.open("w") as f:
        f.write(jsondata)
    
    # print(jsondata)


if __name__ == "__main__":
    if len(argv) != 2 or argv[1].endswith("-help") or argv[1].endswith("-h"):
        print(f"""Exapunks .tex to .png converter
Usage:
  {argv[0]} <input file>

Will dump texture metadata as JSON file alongside png""")
        exit(1)

    filename = argv[1]
    tex2png(filename)
