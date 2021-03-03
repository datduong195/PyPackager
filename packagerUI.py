# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from filecmp import dircmp
from zipfile import ZipFile,ZIP_DEFLATED
import os

verUS = "RBWE"
verEU = "RBWP"
verJP = "RBWJ"
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
        self.browseBox = QtWidgets.QGroupBox(Dialog)
        self.browseBox.setGeometry(QtCore.QRect(10, 10, 441, 91))
        self.browseBox.setTitle("")
        self.browseBox.setObjectName("browseBox")
        self.baseText = QtWidgets.QLabel(self.browseBox)
        self.baseText.setGeometry(QtCore.QRect(10, 20, 47, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.baseText.setFont(font)
        self.baseText.setObjectName("baseText")
        self.inputBase = QtWidgets.QTextEdit(self.browseBox)
        self.inputBase.setGeometry(QtCore.QRect(60, 20, 291, 21))
        self.inputBase.setObjectName("inputBase")

        self.baseBtn = QtWidgets.QPushButton(self.browseBox)
        self.baseBtn.setGeometry(QtCore.QRect(360, 20, 75, 23))
        self.baseBtn.setObjectName("baseBtn")
        self.baseBtn.clicked.connect(self.browserBase)


        self.inputMod = QtWidgets.QTextEdit(self.browseBox)
        self.inputMod.setGeometry(QtCore.QRect(60, 50, 291, 21))
        self.inputMod.setObjectName("inputMod")
        self.modText = QtWidgets.QLabel(self.browseBox)
        self.modText.setGeometry(QtCore.QRect(10, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.modText.setFont(font)
        self.modText.setObjectName("modText")

        self.modBtn = QtWidgets.QPushButton(self.browseBox)
        self.modBtn.setGeometry(QtCore.QRect(360, 50, 75, 23))
        self.modBtn.setObjectName("modBtn")
        self.modBtn.clicked.connect(self.browserMod)

        self.showBox = QtWidgets.QGroupBox(Dialog)
        self.showBox.setGeometry(QtCore.QRect(10, 110, 441, 291))
        self.showBox.setTitle("")
        self.showBox.setObjectName("showBox")

        self.copyBtn = QtWidgets.QPushButton(self.showBox)
        self.copyBtn.setGeometry(QtCore.QRect(360, 10, 75, 23))
        self.copyBtn.setObjectName("copyBtn")
        self.copyBtn.clicked.connect(self.packager)

        self.listFile = QtWidgets.QTextEdit(self.showBox)
        self.listFile.setGeometry(QtCore.QRect(10, 40, 421, 251))
        self.listFile.setObjectName("listFile")

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
    
    def browserBase(self):
        data_path =QtWidgets.QFileDialog.getExistingDirectory(None, 'Open File', r"C:")
        self.inputBase.setText(data_path)
    
    def browserMod(self):
        data_path =QtWidgets.QFileDialog.getExistingDirectory(None, 'Open File', r"C:")
        self.inputMod.setText(data_path)
    
    def copyFile(self,name,dcmpRight):
        if((name not in self.excludeFileName) or not self.ignoreMainCB.isChecked()):
            mkDir = self.outputDir+dcmpRight.split(self.des)[1]
            fileToCopy = os.path.join(dcmpRight,name)
            if(not os.path.isdir(mkDir)):
                os.makedirs(mkDir)
            #print(fileToCopy)
            #print(mkDir)
            os.popen("copy " + fileToCopy + " " + mkDir)
            self.listFile.append(fileToCopy)
            if(name == "boot.bin"):
                self.bootBinDir = fileToCopy
   
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
    def zipdir(self,path, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(path):
            for file in files:
                ziph.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(path, '..')))

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

    def packager(self):
        try:
            self.src = self.inputBase.toPlainText().replace("/","\\")
            self.des = self.inputMod.toPlainText().replace("/","\\")
            dcmp = dircmp(self.src,self.des)
            self.copyFileChange(dcmp)
            
            
        except:
            pass
        self.zipOutput()
        self.msg.exec_()
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
