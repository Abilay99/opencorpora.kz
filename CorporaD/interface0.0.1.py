from PyQt5 import QtWidgets, QtCore, QtGui
from interfaceForm import Ui_MainWindow
import sys
import os
import glob
from CorporaDB import corporaDB
import collections, re
from execute import *
from Global import sozgebolu, bigram
papka_korpus = os.path.dirname(os.path.abspath(__file__))


#db connect
ob = corporaDB()

lencorp = int(ob.Count_corpora()[0]['sany'])

#-------------------------------------------------------------------------------------------------

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.clickbtn)
        self.ui.pushButton_3.clicked.connect(self.reload)
        self.ui.actionOpen.triggered.connect(self.openFileNameDialog)
        self.ui.actionSave.triggered.connect(self.saveFileDialog)
        self.tfidf = {}
        self.bi_tfidf = {}
    def openFileNameDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "","Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            with open(fileName, 'r', encoding="utf-8") as f:
                self.ui.plainTextEdit.setPlainText(f.read())
    def saveFileDialog(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","<filename>-keywords", "Text Files (*.txt);;All Files (*)", options=options)
        if fileName:
            with open(fileName+".txt", 'w', encoding="utf-8") as f:
                for x in self.tfidf:
                    f.write(str(x)+"\n")
                for x in self.bi_tfidf:
                    f.write(str(x)+"\n") 
    def reload(self):
        if self.ui.rettext() != "":
            self.ui.pushButton.setVisible(False)
            self.ui.progressBar.setVisible(True)
            self.ui.pushButton_2.setVisible(False)
            self.ui.pushButton_3.setVisible(False)
            with open(os.path.join(papka_korpus,'tmp/text.tmp'),'w', encoding="utf-8") as f:
                f.write(self.ui.rettext())
            os.system('''cd $HOME/sources/apertium-kaz-rus\ncat "{0}" | apertium -n -d. kaz-rus-tagger > "{1}"'''.format(os.path.join(papka_korpus,'tmp/text.tmp'), os.path.join(papka_korpus,'tmp/app.tmp')))
            apertium = open(os.path.join(papka_korpus,'tmp/app.tmp'),'r',encoding="utf-8").read()
            editedapertium = str(EditedApertium_DB(text = self.ui.rettext(), apertium = apertium))
            outtexts = str(outtexts_DB(aptext = editedapertium))
            train = str(train_DB(outtexts = outtexts))
            txt = outtexts
            #failda berilgen matinnen tek sozderdi wygaryp beredi
            soz = sozgebolu(txt)

            #bigram klasssyndagy konstruktordy qoldanyluy
            bi = bigram(text = txt)
            text = [bi.newlemm, bi.lastlemm]

            #TF_IDF klasssyndagy konstruktordy qoldanyluy
            TfIdf = tf_idf(text = soz, len_corp = lencorp, objectCorporaDB = ob)

            #esepteuler
            tf = TfIdf.tf_esepteu()
            self.ui.progressBar.setValue(16)
            idf = TfIdf.idf_esepteu()
            self.ui.progressBar.setValue(32)
            self.tfidf = TfIdf.tf_idf_esepteu()
            self.ui.progressBar.setValue(48)

            #bigram TF_IDF klasssyndagy konstruktordy qoldanyluy
            BiTfIdf = bi_tf_idf(text = text, len_corp = lencorp, objectCorporaDB = ob)
            bi_tf = BiTfIdf.bi_tf_esepteu()
            self.ui.progressBar.setValue(64)
            bi_idf = BiTfIdf.bi_idf_esepteu()
            self.ui.progressBar.setValue(80)
            self.bi_tfidf = BiTfIdf.bi_tf_idf_esepteu()
            self.ui.progressBar.setValue(100)

            row = 1
            col = 0
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Times New Roman")
            for x in tf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(tf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            for x in bi_tf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(bi_tf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1

            row = 1
            col = 2
            for x in idf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(idf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            for x in bi_idf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(bi_idf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1

            row = 1
            col = 4
            for x in self.tfidf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(self.tfidf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            for x in self.bi_tfidf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(self.bi_tfidf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            if self.ui.progressBar.value() == int(100):
                self.ui.clearbar()
    def clickbtn(self):
        if self.ui.rettext() != "":
            self.ui.pushButton.setVisible(False)
            self.ui.progressBar.setVisible(True)
            with open(os.path.join(papka_korpus,'tmp/text.tmp'),'w', encoding="utf-8") as f:
                f.write(self.ui.rettext())
            os.system('''cd $HOME/sources/apertium-kaz-rus\ncat "{0}" | apertium -n -d. kaz-rus-tagger > "{1}"'''.format(os.path.join(papka_korpus,'tmp/text.tmp'), os.path.join(papka_korpus,'tmp/app.tmp')))
            apertium = open(os.path.join(papka_korpus,'tmp/app.tmp'),'r',encoding="utf-8").read()
            editedapertium = str(EditedApertium_DB(text = self.ui.rettext(), apertium = apertium))
            outtexts = str(outtexts_DB(aptext = editedapertium))
            train = str(train_DB(outtexts = outtexts))
            txt = outtexts
            #failda berilgen matinnen tek sozderdi wygaryp beredi
            soz = sozgebolu(txt)

            #bigram klasssyndagy konstruktordy qoldanyluy
            bi = bigram(text = txt)
            text = [bi.newlemm, bi.lastlemm]

            #TF_IDF klasssyndagy konstruktordy qoldanyluy
            TfIdf = tf_idf(text = soz, len_corp = lencorp, objectCorporaDB = ob)

            #esepteuler
            tf = TfIdf.tf_esepteu()
            self.ui.progressBar.setValue(16)
            idf = TfIdf.idf_esepteu()
            self.ui.progressBar.setValue(32)
            self.tfidf = TfIdf.tf_idf_esepteu()
            self.ui.progressBar.setValue(48)

            #bigram TF_IDF klasssyndagy konstruktordy qoldanyluy
            BiTfIdf = bi_tf_idf(text = text, len_corp = lencorp, objectCorporaDB = ob)
            bi_tf = BiTfIdf.bi_tf_esepteu()
            self.ui.progressBar.setValue(64)
            bi_idf = BiTfIdf.bi_idf_esepteu()
            self.ui.progressBar.setValue(80)
            self.bi_tfidf = BiTfIdf.bi_tf_idf_esepteu()
            self.ui.progressBar.setValue(100)

            row = 1
            col = 0
            font = QtGui.QFont()
            font.setPointSize(12)
            font.setFamily("Times New Roman")
            for x in tf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(tf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            for x in bi_tf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(bi_tf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1

            row = 1
            col = 2
            for x in idf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(idf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            for x in bi_idf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(bi_idf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1

            row = 1
            col = 4
            for x in self.tfidf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(self.tfidf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            for x in self.bi_tfidf:
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(x))
                self.ui.tableWidget.setItem(row, col, item)
                item = QtWidgets.QTableWidgetItem()
                item.setBackground(QtGui.QColor(192,254,255))
                item.setFont(font)
                item.setText(str(round(self.bi_tfidf[x], 5)))
                self.ui.tableWidget.setItem(row, col+1, item)
                row += 1
            
            self.ui.label_2.setVisible(True)
            self.ui.tabledsgn()
            self.ui.resizewin()
            if self.ui.progressBar.value() == int(100):
                self.ui.clearbar()
    
    




if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setApplicationName("Кілттік сөз")
    app.setApplicationVersion("0.0.1")
    application = mywindow()
    application.show()
    sys.exit(app.exec())

    