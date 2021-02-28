replace
=====
指定されたフォルダ以下のファイルの中の文字列を書き換えるツール

windows実行ファイル
-----
+ replace.exe  
+ replace_gui.exe(GUI)  

pythonと必要なライブラリが含まれています。  

開発環境
-----
python3.5

必要なライブラリ
-----
yoshi.util:  
<https://github.com/tripod31/common_python>  
pyqt4(GUI)

replace.py
-----
コマンドラインツール

#### 使い方

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

replace_gui.pyw
-----
GUIツール   
<img src="https://user-images.githubusercontent.com/6335693/50577296-a9394080-0e68-11e9-8293-ceafc8ba7e76.jpg">
