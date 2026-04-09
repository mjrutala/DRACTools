#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:58:02 2026

@author: mrutala
"""

def pip_install(req_file, download_dir):
    import subprocess
    import sys
    import glob
    import os
    
    # Get absolute paths for saving later on
    req_file = os.path.abspath(req_file)
    download_dir = os.path.abspath(download_dir)
    
    # If the download directory is missing the final /, add one
    if download_dir[-1] != '/':
        download_dir += '/'
        
    # # Parse the original requirements.txt for a new filename
    # output_file = req_file.split('.txt')[0] + '_DRAC.txt'
    
    # Read all packages in the requirements.txt
    with open(req_file) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    # For each requirement, either install it from DRAC (--no-index) or 
    # download and install it (--no-deps)
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-index', req])
        except:
            subprocess.check_call([sys.executable, '-m', 'pip', 'download', '--no-deps', req, '-d', download_dir])
            path = glob.glob(download_dir + '/*{}*-none-any*'.format(req.split('=')[0]))
            if len(path) > 0:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', path[0]])
    
    # print(output_file)
    # # Generate a requirements.txt
    # subprocess.check_call([sys.executable, '-m', 'pip', 'freeze', '--local', '>', output_file])
    
if __name__ == "__main__":
    desc = """This python function can be used from the command line to convert pip-style requirements.txt to that expected by DRAC."""

    usage = """
    Following this example, but using this function instead of individually installing packages:
            https://docs.alliancecan.ca/wiki/Python#Creating_virtual_environments_inside_of_your_jobs
    That is, enter the following, paying care that you know what each step does:
        > module load python/3.11
        > ENVDIR=/tmp/$RANDOM
        > virtualenv --no-download $ENVDIR
        > source $ENVDIR/bin/activate
        > pip install --no-index --upgrade pip
        > python convert_requirements.py PATH/TO/REQUIREMENTS.TXT -d ../PATH/TO/DOWNLOAD/
        > deactivate
        """
    import argparse
    parser = argparse.ArgumentParser(description=desc, usage=usage, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("req", help="The original, non-DRAC requirements file (e.g., requirements.txt)", default='requirements.txt')
    parser.add_argument("-d", "--download-dir", help="Location for pip files that aren't on DRAC to be downloaded.", default='./')
    args = parser.parse_args()
    
    pip_install(args.req, args.download_dir)