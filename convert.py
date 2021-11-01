from PyPDF2 import PdfFileReader, PdfFileWriter
import os
from multiprocessing import Process, freeze_support
from docx2pdf import convert
import time
import contextlib
import sys
import argparse


def searchWord(paths):
    word = []
    for p in paths:
        for (dirpath, dirnames, filenames) in os.walk(p, topdown=True):
            for filename in filenames:
                cur = os.path.join(dirpath, filename)
                if(cur[-5:] == ".docx"):
                    word.append(cur)

    return word


def convertWord(words):
    for word in words:
        convert(word)


def convertWordMultiProc(words):
    processes = []

    for wordFile in words:
        processes.append(Process(target=convert, args=(wordFile,)))

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == '__main__':
# def main():

    parser = argparse.ArgumentParser(description='Convert .docx files to .pdf')
    parser.add_argument('Files', nargs='+', action='extend', help='Given files to convert')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Silence all output while running')
    parser.add_argument('-r', '--recursive', action='store_true', help='Convert all docx files in a given folder')

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
        docs = searchWord(argsIn)  # use docs from folder
        print(docs)
    else:
        docs = argsIn  # use docs from args

    if(len(docs) > 0):
        if(not quiet):
            start_time = time.time()
        else:
            with contextlib.redirect_stdout(None):
                convertWordMultiProc(docs)
        if(not quiet):
            print("%s seconds" % (time.time() - start_time))

    else:
        print("No documents given. Terminating.")
