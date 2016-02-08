#!/usr/bin/env python3
# coding:utf-8
'''
Created on 2015/06/16

@author: yoshi
'''
import sys
import io
import os
from mainform import QtGui,Ui_MainWindow,_translate    # @UnresolvedImport
from replace import process
from PyQt4.QtCore import QSettings,QObject,SIGNAL,QTranslator
from PyQt4.Qt import QFont, QDialog

#dialog
from select_lang_form import Ui_Dialog  #@UnresolvedImport

class MyForm(QtGui.QMainWindow):
    '''
    settings file
    '''
    SAVE_FILE=os.path.join(os.path.dirname(__file__), "form_value.txt")
    
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.lineEdit_pattern.setText("*.txt")
        
        #set callback for widgets     
        self.ui.pushButton_dir.clicked.connect(self.choose_dir)
        self.ui.pushButton_exec.clicked.connect(self.execClick)
        self.ui.pushButton_preview.clicked.connect(self.previewClick)
        
        #set callback function for menu item
        QObject.connect(self.ui.actionFont, SIGNAL('triggered()'), self.choose_font)
        QObject.connect(self.ui.actionLanguage, SIGNAL('triggered()'), self.select_lang)
        
        #translations
        self._lang = "en" #defalut lang
        self._translator = QTranslator()
        app.installTranslator(self._translator)
        
        self.load_settings()    #read settings file
        
    '''
    window close event
    '''
    def closeEvent(self, *args, **kwargs):
        self.save_settings()
        return QtGui.QMainWindow.closeEvent(self, *args, **kwargs)
    
    def choose_dir(self):
        dialog = QtGui.QFileDialog()
        dialog.setFileMode(QtGui.QFileDialog.DirectoryOnly)
        start_dir = self.ui.lineEdit_start_dir.text()
        if os.path.exists(start_dir):
            dialog.setDirectory(start_dir)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()
            if len(fileNames)>0:
                self.ui.lineEdit_start_dir.setText(fileNames[0])

    def choose_font(self):
        cur_f = self.font()
        f,ok = QtGui.QFontDialog.getFont(cur_f)
        if ok:
            self.setFont(f)
            self.ui.centralwidget.setFont(f)    #when font of container is changed,font of all child wigets are changed
    
    def select_lang(self):
        dialog = QDialog()
        ui = Ui_Dialog()
        ui.setupUi(dialog)
        
        ui.comboBox.addItem(_translate("MainWindow",'english',None),'en')
        ui.comboBox.addItem(_translate("MainWindow",'japanese',None),'ja')
        idx = ui.comboBox.findData(self._lang)
        ui.comboBox.setCurrentIndex(idx)
        if dialog.exec_()==QDialog.Accepted:
            idx = ui.comboBox.currentIndex()
            lang = ui.comboBox.itemData(idx)
            self.set_lang(lang)
    
    '''
    execute button
    '''
            
    def execClick(self):
        self.execute(False)
    
    def previewClick(self):
        self.execute(True)
        
    def execute(self,preview):
        start_dir = self.ui.lineEdit_start_dir.text()
        pattern = self.ui.lineEdit_pattern.text()
        from_str = self.ui.lineEdit_from_str.text()
        to_str = self.ui.lineEdit_to_str.text()
        
        #confirm
        if not preview:
            confirmObject = QtGui.QMessageBox.question(self,
                _translate("MainWindow", "Confirm", None),
                _translate("MainWindow", "Are you sure to execute?", None),
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                QtGui.QMessageBox.No)
            if confirmObject != QtGui.QMessageBox.Yes:
                return
        
        os.environ['LANGUAGE']=self._lang   #does'nt work?
        
        #display standard output to textedit
        output = io.StringIO()
        sys.stdout = output
        process(start_dir,pattern,from_str,to_str,preview)
        s= output.getvalue()
        sys.stdout = sys.__stdout__
        self.ui.textEdit_output.setPlainText(s)
    
    def save_settings(self):
        start_dir = self.ui.lineEdit_start_dir.text()
        pattern = self.ui.lineEdit_pattern.text()
        from_str = self.ui.lineEdit_from_str.text()
        to_str = self.ui.lineEdit_to_str.text()

        settings = QSettings(self.SAVE_FILE,
                                  QSettings.IniFormat)
        if settings.Status != QSettings.AccessError:
            settings.beginGroup("form_value")
            settings.setValue("geometry",self.saveGeometry())
            settings.setValue("font",self.font().toString())
            settings.setValue("lang",self._lang)   
            
            settings.setValue("start_dir", start_dir)
            settings.setValue("pattern", pattern)
            settings.setValue("from_str", from_str)
            settings.setValue("to_str", to_str)

            settings.endGroup()
    
    def load_settings(self):
        if not os.path.exists(self.SAVE_FILE):
            return
        
        settings = QSettings(self.SAVE_FILE,
                                  QSettings.IniFormat)
        if settings.Status != QSettings.AccessError:
            settings.beginGroup("form_value")

            self.restoreGeometry(settings.value("geometry"))
            self.font().fromString(settings.value("font"))
            f=QFont()
            if f.fromString(settings.value("font")):
                self.setFont(f)
            
            self.set_lang(settings.value("lang"))
            
            self.ui.lineEdit_start_dir.setText(settings.value('start_dir'))
            self.ui.lineEdit_pattern.setText(settings.value('pattern'))
            self.ui.lineEdit_from_str.setText(settings.value('from_str'))
            self.ui.lineEdit_to_str.setText(settings.value('to_str'))
            
            settings.endGroup()
    
    def set_lang(self,lang):
        if self._translator.load("replace."+lang,
                                 os.path.join(os.path.dirname(__file__), 'translations')) or lang == "en":
            self._lang = lang
            self.ui.retranslateUi(self)
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    form = MyForm()
    form.show()
    sys.exit(app.exec_())
