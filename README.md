# Exapunks Tex 2 Png

Two python scripts to help extract image data from EXAPUNKS .tex files

Requires `pypng` and `lz4`

## Usage

`tex.py` can be used to extract raw decompressed data (RGBA/greyscale pixels)

`tex2png.py` can be used to convert tex to png

Both scripts will also produce header information stored at the start of the texture as a JSON file

## Docs

`tex.py` contains a `TexReader` class that's used to read in the tex file and decompress the lz4 pixel data. It also has a `TexFile` class used to store header data and decompressed pixels

`tex2png.py` has functions to read in files, and save the image data as png and JSON

## Thanks

Thanks to [sigsev-mvm](https://gist.github.com/sigsegv-mvm/0f07b1c6d8dd56885f74e03758c11e58) for reverse engineering the tex file format