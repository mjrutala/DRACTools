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
    
    req_file = os.path.abspath(req_file)
    download_dir = os.path.abspath(download_dir)
    
    if download_dir[-1] != '/':
        download_dir += '/'
    output_file = req_file.split('.txt')[0] + '_DRAC.txt'
    
    with open(req_file) as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--no-index', req])
        except:
            subprocess.check_call([sys.executable, '-m', 'pip', 'download', '--no-deps', req, '-d', download_dir])
            path = glob.glob(download_dir + '/*{}*-none-any*'.format(req.split('=')[0]))
            if len(path) > 0:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', path[0]])
    
    # Generate a requirements.txt
    print('---------------------------------')
    print(output_file)
    subprocess.check_call([sys.executable, '-m', 'pip', 'freeze', '--local', '>', output_file])
    
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Convert pip requirements for DRAC use.")
    parser.add_argument("req", help="The original, non-DRAC requirements file (e.g., requirements.txt)", default='requirements.txt')
    parser.add_argument("-d", "--download-dir", help="Location for pip files that aren't on DRAC to be downloaded.", default='./')
    args = parser.parse_args()
    
    pip_install(args.req, args.download_dir)