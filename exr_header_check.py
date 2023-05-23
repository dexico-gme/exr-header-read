import os
import subprocess, shlex
from glob import glob
import sys
import argparse
import time
import asyncio
import re

# add command line arguements to the python script
parser = argparse.ArgumentParser(description='A program to return file count for a vfx pulls package')
# example parser.add_argument("print_string", help="Prints the supplied argument.")
parser.add_argument("-p", "--path", help="the input path", required=True)
parser.add_argument("-v", help="verbose mode", required=False )
args = parser.parse_args()

argv = vars(args)

input_path = args.path

# example
# oiiotool in.exr --attrib "FStop" 22.0 --attrib "IPTC:City" "Berkeley" -o out.exr
# to add multiple use --attrib in front of every key added
# oiiotool in.exr --attrib "{key string to add}" "value" -o out.exr
# will write FStop: 22.0

tic = time.perf_counter()
nfcount = 0
nfarray = []

async def getInfo():
    for i in glob(f"{input_path}/*/*/*/*.exr", recursive=True):
        #await asyncio.sleep(1)
        global nfcount
        print(i)
        cmd = f"oiiotool -v -a -info {i}"
        args_split = shlex.split(cmd)
        #subprocess.check_output
        p = subprocess.Popen(args_split, stdout=subprocess.PIPE)
        output = p.stdout.read().decode('utf-8')
        #await asyncio.sleep(1)
        if re.search("Format Extraction",output):
            print('\n ------ Found Format ------ \n')
        else:
            print('\n ------ Format Not Found ------ \n')
            nfcount+=1
            nfarray.append(i)
        #print("output: *----*\n" + str(output))

asyncio.run(getInfo())

print('Not Found Total = ' + str(nfcount))


for item in nfarray:
	print(item)
# toc = time.perf_counter()
# print(f'Time taken: {toc - tic:0.4f} seconds')
# print("DONE")