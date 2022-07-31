from enum import Enum
from struct import unpack
from lz4.block import decompress

class ColorFmt(Enum):
    INVALID = 0,
    EIGHT_BPP = 1,
    RGBA = 2

# Custom exception class
class HeaderException(Exception):
    pass

# holds metadata and pixels bytearray
class TexFile:
    def __init__(self, data, colorFmt, display, bounds, cropOff, link, pixels):
        self.data = data
        self.colorFmt = colorFmt
        self.display = display
        self.bounds = bounds
        self.cropOff = cropOff
        self.link = link
        self.pixels = pixels

# reads a file and returns a TexFile instance
class TexReader:
    def __init__(self, file):
        self.file = file
    
    def readHeader(self):
        magic = self.file.read(4)
        if magic != b"\xEA\x03\x00\x00":
            raise HeaderException("Magic number wrong; File is not in valid tex format")
        
        return unpack("2ii2i4i2f2fi",self.file.read(56))
    
    def read(self):
        dataW, dataH, \
        colorFmt, \
        displayW, displayH, \
        boundsTL, boundsTR, boundsBL, boundsBR, \
        cropOffX, cropOffY, \
        linkX, linkY, \
        dataSize = self.readHeader()

        pixelData = decompress(self.file.read(dataSize), uncompressed_size=dataW*dataH*4, return_bytearray=True)

        return TexFile((dataW, dataH), ColorFmt(colorFmt), (displayW, displayH), (boundsTL, boundsTR, boundsBL, boundsBR), (cropOffX, cropOffY), (linkX, linkY), pixelData)




if __name__ == "__main__":
    from sys import argv
    from json import dumps
    from pathlib import Path
    
    if len(argv) != 2:
        print(f"Usage:\n  {argv[0]} <filename>")
        exit(1)

    filename = argv[1]
    
    with open(filename, "rb") as f:
        reader = TexReader(f)
        texfile = reader.read()
    
    pathobj = Path(filename)
    convertedfilename = pathobj.with_name(pathobj.stem + ".pixels")

    with convertedfilename.open("wb") as f:
        f.write(texfile.pixels)

    convertedfilename = pathobj.with_name(pathobj.stem + ".json")

    jsonData = dumps({
            "data": texfile.data,
            "colorFmt": texfile.colorFmt.value,
            "display": texfile.display,
            "bounds": texfile.bounds,
            "cropOff": texfile.cropOff,
            "link": texfile.link
        }, indent=2)

    with convertedfilename.open("w") as f:
        f.write(jsonData)
    
    print(jsonData)

    def humaniseBytes(bytes):
        sizes = [1024**3, 1024**2, 1024, 1]
        units = ["GiB", "MiB", "KiB", "B"] # binary prefixes

        for i,size in enumerate(sizes):
            if bytes//size > 0:
                return f"{bytes/size:.2f}{units[i]}"
        
        return f"{bytes}" # should never happen
    
    print(f"Decompressed size: {humaniseBytes(len(texfile.pixels))}")
