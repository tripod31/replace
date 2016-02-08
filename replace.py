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

from yoshi.util import find_all_files,is_match_patterns_fnmatch,get_encoding,EncodeException    #@UnresolvedImport

def preview(file,from_str):
    hit=False
    try:
        enc,data = get_encoding(file)
        if data.find(from_str) != -1:
            hit = True
    except Exception as e:
        sys.stderr.write(e)
        return
    finally:
        pass
            
    if hit:
        print("hit:%s" % (file))

def replace(file,from_str,to_str):
    hit =False
    try:
        enc,data = get_encoding(file)
        if data.find(from_str) != -1:
            hit = True
        
            data = data.replace(from_str, to_str)
            bytes_data = data.encode(enc) 
            temp_file= tempfile.mkstemp()
            ft = os.fdopen(temp_file[0],mode='w+b') #binary mode,to prevent end of line to be changed
            ft.write(bytes_data)
    except Exception as e:
        sys.stderr.write(str(e))
        return
    
    if not hit:
        return
    
    #verify data
    ft.seek(0)
    new_bytes = ft.read()
    ft.close()
    data_new =new_bytes.decode(enc)
    
    if data_new != data:
        raise EncodeException('verify data failed')
    try:
        os.remove(file)
    except Exception as e:
        sys.stderr.write(str(e))
        os.remove(temp_file[1])
        return
    
    shutil.copyfile(temp_file[1], file)
    os.remove(temp_file[1])
    
    print("replaced:%s" % (file))

def process(start_dir,file_pattern,from_str,to_str,p_preview):
    files = find_all_files(start_dir)
    for file in files:
        if is_match_patterns_fnmatch(file, file_pattern.split()):
            if p_preview:
                preview(file,from_str)
            else:
                replace(file,from_str,to_str)
    
    print("finished.")

if __name__ == '__main__':
    
    #arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_dir',
                        default=".")
    parser.add_argument('--file_pattern',
                        help="pattern of the name of file to be replaced,in wild card format.ex)'*.txt,*.bat'")
    parser.add_argument('--from_str')
    parser.add_argument('--to_str')
    parser.add_argument('--preview',
                        action='store_true',default=False,
                        help="do not change files when specified")
    args=parser.parse_args()
    #print(args)
    process(args.start_dir,args.file_pattern,args.from_str,args.to_str,args.preview)
            
    sys.exit(0)