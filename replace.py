#!/usr/bin/env python3
# coding:utf-8
'''
replace string in files in specified directory.
'''
import argparse
#import re
import os
import sys
import tempfile
import shutil

from yoshi.util import find_all_files,is_match_patterns_fnmatch,\
            get_encoding,EncodeException,replace_str,print_arr,DecodeException    #@UnresolvedImport

import gettext
#translation
translation = gettext.translation(
    domain='replace',
    localedir=os.path.join(os.path.dirname(__file__), 'translations'),
    fallback=True,
    codeset='utf-8'
    )
_=translation.gettext

def process(start_dir,file_pattern,from_str,to_str,preview):
    if not os.path.exists(start_dir):
        print(_("%s: does'nt exists") % start_dir )
        return
    
    files = find_all_files(start_dir)
    count =0
    files_processed=[]  #files to be processed
    files_dec_ng=[]     #files that can't be decoded
    
    #gather information of files.current encoding,end of line
    for path in files:
        if not is_match_patterns_fnmatch(path, file_pattern.split(',')):
            continue
        try:
            encoding,data = get_encoding(path)
        except DecodeException:
            files_dec_ng.append(path)
            continue
        
        if from_str in data: 
            files_processed.append(path)
    
    #print files that can't be decoded
    if len(files_dec_ng)>0:
        print(_("Can't decode these files.They are not processed:"))
        for path in files_dec_ng:
            print(path)
        print("---")
        
    #print files to be converted
    if len(files_processed)>0:
        print(_("files to replace:"))
        for path in files_processed:
            print(path)
        print("---")
    else:
        print(_("nothing to do."))
        return
    
    #return here if preview mode
    if preview:
        print (_("***preview mode***"))
        return
    
    #convert
    for path in files_processed:
        replace_str(path,from_str,to_str)
        count+=1

    print (count,_("files changed."))   


if __name__ == '__main__':
    
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_dir',
                        default=".")
    parser.add_argument('--file_pattern',
                        help="pattern of the name of file to be replaced,in wild card format,separeted by ','. example:'*.txt,*.bat'")
    parser.add_argument('--from_str')
    parser.add_argument('--to_str')
    parser.add_argument('--preview',
                        action='store_true',default=False,
                        help="do not change files when specified")
    args=parser.parse_args()
    #print(args)
    process(args.start_dir,args.file_pattern,args.from_str,args.to_str,args.preview)
            
    sys.exit(0)