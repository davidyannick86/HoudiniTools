from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

import hou

class live_renamer(QtWidgets.QDialog):
     
    def __init__(self,nodes):
        super(live_renamer,self).__init__(hou.qt.mainWindow())
        self.nodes=nodes
        self.updateMode=hou.updateModeSetting()
        
        hou.setUpdateMode(hou.updateMode.Manual)

        self.storeNames()
        self.configure_dialog()
        self.widgets()
        self.layout()
        self.connections()

    def configure_dialog(self):
        self.setWindowTitle("Live node renamer")
        self.setFixedWidth(240)
        self.setFixedHeight(260)

        self.setWindowFlags(self.windowFlags()^QtCore.Qt.WindowContextHelpButtonHint^QtCore.Qt.WindowCloseButtonHint)

    def widgets(self):
        self.search=QtWidgets.QLineEdit()
        self.search.setPlaceholderText("Search")
        self.replace=QtWidgets.QLineEdit()
        self.replace.setPlaceholderText("Replace")

        self.sep=hou.qt.Separator()

        self.prefix=QtWidgets.QLineEdit()
        self.suffix=QtWidgets.QLineEdit()

        self.remDig=QtWidgets.QCheckBox()

        self.okBtn=QtWidgets.QPushButton("Rename")
        self.cancelBtn=QtWidgets.QPushButton("Cancel")

    def layout(self):
        self.mainLayout=QtWidgets.QVBoxLayout(self)

        self.mainLayout.addWidget(self.search)
        self.mainLayout.addWidget(self.replace)

        self.optionsLayout=QtWidgets.QFormLayout()
        self.optionsLayout.addRow("Prefix",self.prefix)
        self.optionsLayout.addRow("Suffix",self.suffix)
        self.optionsLayout.addRow("Remove Digits",self.remDig)

        self.mainLayout.addLayout(self.optionsLayout)

        self.mainLayout.addWidget(self.sep)

        self.bottomLayout=QtWidgets.QHBoxLayout()
        self.bottomLayout.addWidget(self.cancelBtn)
        self.bottomLayout.addWidget(self.okBtn)

        self.mainLayout.addLayout(self.bottomLayout)

    def storeNames(self):
        self.nodeNames={}
        for node in self.nodes:
            self.nodeNames[node]=node.name()

    def restoreNames(self):
        for node in self.nodes:
            node.setName(self.nodeNames[node])
        self.restoreUpdateMode()
        self.close()

    def removeDigits(self,text):
        filtered=text
        numbers="0123456789_"

        for letter in text:
            last=filtered[-1:]
            if last in numbers:
                filtered=filtered[:-1]
            else:
                break
        return filtered

    def rename(self):
        searchText=self.search.text().replace(" ","_")
        replaceText=self.replace.text().replace(" ","_")
        prefixText=self.prefix.text().replace(" ","_")
        suffixText=self.suffix.text().replace(" ","_")

        for node in self.nodes:
            originalName=self.nodeNames[node]

            if searchText in originalName and searchText :
                modifiedName=originalName.replace(searchText,replaceText)
            else:
                modifiedName=originalName

            checked=self.remDig.isChecked()

            if checked :
                modifiedName=self.removeDigits(modifiedName)

            modifiedName=prefixText+modifiedName+suffixText

            node.setName(modifiedName,unique_name=True)
        
    def exitApp(self):
        self.restoreUpdateMode()
        self.close()

    def connections(self):
        self.cancelBtn.clicked.connect(self.restoreNames)
        self.cancelBtn.clicked.connect(self.close)
        

        self.okBtn.clicked.connect(self.exitApp)
        

        self.search.textChanged.connect(self.rename)
        self.replace.textChanged.connect(self.rename)
        self.prefix.textChanged.connect(self.rename)
        self.suffix.textChanged.connect(self.rename)

        self.remDig.stateChanged.connect(self.rename)

    def restoreUpdateMode(self):
        hou.setUpdateMode(self.updateMode)
