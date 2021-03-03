# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from filecmp import dircmp
from zipfile import ZipFile,ZIP_DEFLATED
import os

#Define Version for each region, will be use in name of zip file
verUS = "RBWE"
verEU = "RBWP"
verJP = "RBWJ"

#Class for UI
class Ui_Dialog(object):
    def __init__(self):
        self.src = ""
        self.des = "" 
        self.excludeFileName = ["main.dol"]
        self.outputDir = "packagerOutput\\"
        self.modVersion = ""
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(461, 405)
        #Browser Box for Base and Mod
        self.browseBox = QtWidgets.QGroupBox(Dialog)
        self.browseBox.setGeometry(QtCore.QRect(10, 10, 441, 91))
        self.browseBox.setTitle("")
        self.browseBox.setObjectName("browseBox")
        #Text for Base Browser
        self.baseText = QtWidgets.QLabel(self.browseBox)
        self.baseText.setGeometry(QtCore.QRect(10, 20, 47, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.baseText.setFont(font)
        self.baseText.setObjectName("baseText")
        #Display Base Directory
        self.inputBase = QtWidgets.QTextEdit(self.browseBox)
        self.inputBase.setGeometry(QtCore.QRect(60, 20, 291, 21))
        self.inputBase.setObjectName("inputBase")
        #Browser Button for Base
        self.baseBtn = QtWidgets.QPushButton(self.browseBox)
        self.baseBtn.setGeometry(QtCore.QRect(360, 20, 75, 23))
        self.baseBtn.setObjectName("baseBtn")
        self.baseBtn.clicked.connect(self.browserBase)
        #Display Mod Directory
        self.inputMod = QtWidgets.QTextEdit(self.browseBox)
        self.inputMod.setGeometry(QtCore.QRect(60, 50, 291, 21))
        self.inputMod.setObjectName("inputMod")
        #Text for Mod Browser
        self.modText = QtWidgets.QLabel(self.browseBox)
        self.modText.setGeometry(QtCore.QRect(10, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.modText.setFont(font)
        self.modText.setObjectName("modText")
        #Browser Button for Mod
        self.modBtn = QtWidgets.QPushButton(self.browseBox)
        self.modBtn.setGeometry(QtCore.QRect(360, 50, 75, 23))
        self.modBtn.setObjectName("modBtn")
        self.modBtn.clicked.connect(self.browserMod)
        #Display Mod Directory
        self.showBox = QtWidgets.QGroupBox(Dialog)
        self.showBox.setGeometry(QtCore.QRect(10, 110, 441, 291))
        self.showBox.setTitle("")
        self.showBox.setObjectName("showBox")
        #Copy Button
        self.copyBtn = QtWidgets.QPushButton(self.showBox)
        self.copyBtn.setGeometry(QtCore.QRect(360, 10, 75, 23))
        self.copyBtn.setObjectName("copyBtn")
        self.copyBtn.clicked.connect(self.packager)
        #Display Changed Files
        self.listFile = QtWidgets.QTextEdit(self.showBox)
        self.listFile.setGeometry(QtCore.QRect(10, 40, 421, 251))
        self.listFile.setObjectName("listFile")
        #Checkbox for Ignore main.dol
        self.ignoreMainCB = QtWidgets.QCheckBox(self.showBox)
        self.ignoreMainCB.setGeometry(QtCore.QRect(249, 10, 101, 20))
        self.ignoreMainCB.setObjectName("ignoreMainCB")

        self.fileText = QtWidgets.QLabel(self.showBox)
        self.fileText.setGeometry(QtCore.QRect(10, 0, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.fileText.setFont(font)
        self.fileText.setObjectName("fileText")
        #Popup message for Done
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("Done!")
        self.msg.setWindowTitle("Copy Result")
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.baseText.setText(_translate("Dialog", "Base:"))
        self.baseBtn.setText(_translate("Dialog", "Browse"))
        self.modText.setText(_translate("Dialog", "Mod:"))
        self.modBtn.setText(_translate("Dialog", "Browse"))
        self.copyBtn.setText(_translate("Dialog", "Copy"))
        self.listFile.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.ignoreMainCB.setText(_translate("Dialog", "Ignore main.dol"))
        self.fileText.setText(_translate("Dialog", "File Changes"))
    #Method for browsing the Base Directory
    def browserBase(self):
        data_path =QtWidgets.QFileDialog.getExistingDirectory(None, 'Open File', r"C:")
        self.inputBase.setText(data_path)
    #Method for browsing the Modded Directory
    def browserMod(self):
        data_path =QtWidgets.QFileDialog.getExistingDirectory(None, 'Open File', r"C:")
        self.inputMod.setText(data_path)
    #Method for recursively walking through the directory for getting file names and absolute path
    def copyFile(self,name,dcmpRight):

        #Check condition for Ignore main.dol file or if file name is in exclude list of files
        if((name not in self.excludeFileName) or not self.ignoreMainCB.isChecked()):
            mkDir = self.outputDir+dcmpRight.split(self.des)[1]
            fileToCopy = os.path.join(dcmpRight,name)
            if(not os.path.isdir(mkDir)):
                os.makedirs(mkDir)
            os.popen("copy " + fileToCopy + " " + mkDir)
            self.listFile.append(fileToCopy)
            #Get absolute directory of boot.bin for detecting region
            if(name == "boot.bin"):
                self.bootBinDir = fileToCopy
    #Method for comparing changed file and copy them into output folder   
    def copyFileChange(self,dcmp):
        #print("Copying ...")
        for name in dcmp.diff_files:
            #print("diff_file %s found in %s and %s" % (name, dcmp.left,dcmp.right))
            self.copyFile(name,dcmp.right)
        for name in dcmp.right_only:
            #print("right file only %s found in %s" % (name,dcmp.right))
            self.copyFile(name,dcmp.right)
        for sub_dcmp in dcmp.subdirs.values():
            self.copyFileChange(sub_dcmp)
    #Method for zipping all files recursively
    def zipdir(self,path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))
    #Method for calling zipdir method and name the output zip file
    def zipOutput(self):
        with open(self.bootBinDir, "r") as f:
            version = f.read(4)
            if(version == verUS):
                self.modVersion = "US"
            elif(version == verEU):
                self.modVersion = "EU"
            elif(version == verJP):
                self.modVersion = "JP"
        zipName = "packagerOutput"+self.modVersion+".zip"
        # create a ZipFile object
        zipf = ZipFile(zipName, 'w', ZIP_DEFLATED)
        self.zipdir(self.outputDir, zipf)
        zipf.close()
    #Will be execute when User press Copy Button, consider this as main of all logic for this packager tool
    def packager(self):
        try:
            #Have to replace "/" with "\\" because PyQT by default using "/" for directory
            self.src = self.inputBase.toPlainText().replace("/","\\")
            self.des = self.inputMod.toPlainText().replace("/","\\")
            dcmp = dircmp(self.src,self.des)
            self.copyFileChange(dcmp)
            self.zipOutput()
            self.msg.exec_()   
        except:
            pass

if __name__ == "__main__":
    import sys
    #Initialize GUI
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
