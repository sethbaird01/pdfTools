# What's "pdfTools"?

A set of python scripts that allows you to:
* Convert `.docx` files to `.pdf`
* Merge `.pdf` files


# Usage

## First steps

1. `git clone https://github.com/sethbaird01/pdfTools && cd pdfTools`
2. `pip install -r requirements.txt`

## Converting `docx` files to `.pdf`

`python3 convert.py file1.pdf file2.pdf ...`

This will convert all specified files to their resulting `.pdf`s. Conversions will happen in FIFO order, and output files will be in the parent directory.


## Merging `.pdf` Files

`python3 merge.py file1.pdf file2.pdf ...`

Works in a similar fashion to `convert.py`, but merges all given files into a new file `merged.pdf`



# Options (flags)

- `-q` Quiet mode: print nothing while running
- `-r` Recursive mode: Traverse a folder given as argument

### Example: using flags to merge all files in a folder
1. `python3 merge.py -r /path/to/folder`

This will recursively find all .pdf files in the folder you specify, and append them all to the output file, `merged.pdf` in the parent folder. The order in which this script finds files can be found [here](https://www.geeksforgeeks.org/os-walk-python/). By default it uses `topdown=True`, meaning your tree of files will be parsed in a top-down fashion.