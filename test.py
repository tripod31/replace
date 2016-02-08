# coding:utf-8
import unittest
import subprocess
import os
from replace import process #@UnresolvedImport

def create_file():
    if not os.path.exists('test'):
        os.mkdir('test')
    
    with open("test/utf8.txt","w",encoding="utf-8") as f:
        f.write("あああ\nabc変更前def\nいいい\n")
        f.close()
    with open("test/cp932.txt","w",encoding="cp932") as f:
        f.write("あああ\nabc変更前def\nいいい\n")
        f.close()

def byte2str(bytes):
    return bytes.decode("utf-8").replace("\r\n","\n")

def exec_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stdout_data, stderr_data = p.communicate()
    return p.returncode,byte2str(stdout_data),byte2str(stderr_data)

class Test1(unittest.TestCase):
    def setUp(self):
        create_file()
    
    def test_call(self):
        process('test','*.txt','変更前','変えたよ',False)
        with open("test/utf8.txt","r",encoding="utf-8") as f:
            data=f.read()
            f.close()
        self.assertEqual(data,"あああ\nabc変えたよdef\nいいい\n")         
    
    def test_exec(self):
        cmd = "python replace.py --start_dir test --file_pattern *.txt --from_str 変更前 --to_str 変えたよ"
        ret,stdout,stderr = exec_command(cmd)
        print( stderr+stdout)        
        self.assertEqual(ret,0)
        self.assertEqual(len(stderr), 0)
                #read file
        with open("test/utf8.txt","r",encoding="utf-8") as f:
            data=f.read()
            f.close()
        self.assertEqual(data,"あああ\nabc変えたよdef\nいいい\n") 
    
    def test_preview(self):
        cmd = "python replace.py --start_dir test --file_pattern *.txt --from_str 変更前 --to_str 変えたよ --preview"
        ret,stdout,stderr = exec_command(cmd)
        print( stderr+stdout)        
        self.assertEqual(ret,0)
        self.assertEqual(len(stderr), 0)
        #read file
        with open("test/utf8.txt","r",encoding="utf-8") as f:
            data=f.read()
            f.close()
        self.assertEqual(data,"あああ\nabc変更前def\nいいい\n") 
        
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
    '''
    suite = unittest.TestSuite()
    suite.addTest(Test1('test_call'))
    unittest.TextTestRunner(verbosity=2).run(suite)
    '''