replace
=====
tool to convert string in files that are in specified directory.

development environment
-----
python3.5

required libraries
-----

replace.py
-----
Command line tool.

####usage

    usage: replace.py [-h] [--start_dir START_DIR] [--file_pattern FILE_PATTERN]
                      [--from_str FROM_STR] [--to_str TO_STR] [--preview]
    
    optional arguments:
      -h, --help            show this help message and exit
      --start_dir START_DIR
      --file_pattern FILE_PATTERN
                            pattern of the name of file to be replaced,in wild
                            card format,separeted by ','.
                            example:'*.txt,*.bat'
      --from_str FROM_STR
      --to_str TO_STR
      --preview             do not change files when specified