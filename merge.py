from PyPDF2 import PdfFileReader, PdfFileWriter
import os
from multiprocessing import Process, freeze_support
from docx2pdf import convert
import time
import sys
import argparse


def searchPDF(paths):
    pdf = []
    for p in paths:
        for (dirpath, dirnames, filenames) in os.walk(p, topdown=True):
            for filename in filenames:
                cur = os.path.join(dirpath, filename)
                if(cur[-4:] == ".pdf"):  # [-4:] means last 4 characters in the filename
                    pdf.append(cur)

    return pdf


def merge_pdfs(paths, output):
    pdf_writer = PdfFileWriter()

    for path in paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            # Add each page to the writer object
            pdf_writer.addPage(pdf_reader.getPage(page))

    # Write out the merged PDF
    with open(output, 'wb') as out:
        pdf_writer.write(out)


if __name__ == '__main__':
# def main():

    parser = argparse.ArgumentParser(description='Merge PDFs')
    parser.add_argument('Files', nargs='+', action='extend', help='Merge given files to one output pdf')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Silence all output while running')
    parser.add_argument('-r', '--recursive', action='store_true', help='Merge all pdf files in a given folder')

    args = parser.parse_args()

    # vars from arguments
    quiet = args.quiet
    recurse = args.recursive
    argsIn = args.Files

    # no -r but argument was a folder
    if(not recurse and (os.path.isdir(argsIn[0]))):
        if(not quiet):
            print("Folder given, but -r not specified. Terminating.")
        exit()

    # -r but argument was a file
    if(recurse and (os.path.isfile(argsIn[0]))):
        if(not quiet):
            print("Recurse option given but file passed, -r ignored.")
        recurse = False
        
    if(len(argsIn) > 1 and not quiet):
        print("Multiple folders given. Finding PDFs in all of them")
 
    if(recurse):
        pdfs = searchPDF(argsIn)  # use pdfs from folder
    else:
        pdfs = argsIn  # use pdfs from args

    if(len(pdfs) >= 2):
        if(not quiet):
            print("Merging the following files:")
            print(pdfs)
        merge_pdfs(pdfs, output='merged.pdf')
    else:
        print("<2 PDFs given. Terminating.")
