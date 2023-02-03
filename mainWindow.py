import os.path
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPixmap
from HealthApp.diseases import PneumoniaDetect
from mail import SendMail
import sys
import time



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        uic.loadUi('./UI/mainWindow.ui', self)
        self.pushButtonHome.clicked.connect(self.setPageHome)
        self.pushButtonPneumonia.clicked.connect(self.setPagePneumonia)
        self.pushButtonBrainTumor.clicked.connect(self.setPageBrainTumor)
        self.pushButtonBreastCancer.clicked.connect(self.setPageBreastCancer)

        self.pushButtonCheck.clicked.connect(self.checkPneumonia)

    def setPageHome(self):
        self.stackedWidget.setCurrentWidget(self.home)
        self.selectButton('pushButtonHome')

    def setPagePneumonia(self):
        self.stackedWidget.setCurrentWidget(self.pagePneumonia)
        self.selectButton('pushButtonPneumonia')


    def setPageBrainTumor(self):
        self.stackedWidget.setCurrentWidget(self.pageBrainTumor)
        self.selectButton('pushButtonBrainTumor')

    def setPageBreastCancer(self):
        self.stackedWidget.setCurrentWidget(self.pageBrainTumor)
        self.selectButton('pushButtonBreastCancer')

    def selectButton(self, buttonType):
        styleSheet = """QPushButton{\n
                            color: rgb(255, 255, 255);\n
                            border-radius: 10px;\n
                            text-color: #FFFFF;\n
                            padding-top: 7px;\n
                            padding-bottom: 7px;\n
                            padding-left: 20px;\n
                            padding-right: 20px;    \n
                            background-color: rgb(19, 157, 242);}\n
                        QPushButton:hover {\n
                            background-color: rgb(15, 90, 251);}"""

        styleSheetClick = (styleSheet.replace('19, 157, 242', '15, 90, 252')).replace('15, 90, 251', '19, 157, 242')

        if buttonType == 'pushButtonHome':
            self.pushButtonHome.setStyleSheet(styleSheetClick)
            self.pushButtonPneumonia.setStyleSheet(styleSheet)
            self.pushButtonBrainTumor.setStyleSheet(styleSheet)
            self.pushButtonBreastCancer.setStyleSheet(styleSheet)

        elif buttonType == 'pushButtonPneumonia':
            self.pushButtonHome.setStyleSheet(styleSheet)
            self.pushButtonPneumonia.setStyleSheet(styleSheetClick)
            self.pushButtonBrainTumor.setStyleSheet(styleSheet)
            self.pushButtonBreastCancer.setStyleSheet(styleSheet)


        elif buttonType == 'pushButtonBrainTumor':
            self.pushButtonHome.setStyleSheet(styleSheet)
            self.pushButtonPneumonia.setStyleSheet(styleSheet)
            self.pushButtonBrainTumor.setStyleSheet(styleSheetClick)
            self.pushButtonBreastCancer.setStyleSheet(styleSheet)

        elif buttonType == 'pushButtonBreastCancer':
            self.pushButtonHome.setStyleSheet(styleSheet)
            self.pushButtonBrainTumor.setStyleSheet(styleSheet)
            self.pushButtonPneumonia.setStyleSheet(styleSheet)
            self.pushButtonBreastCancer.setStyleSheet(styleSheetClick)

    def sendDetail(self, anaylsis, analysisType, value):
        patientName = self.lineEditPatientName.text()
        patientID = self.lineEditPatientID.text()
        doctorMail = self.lineEditDoctorMail.text()

        sender = SendMail()
        try:
            sender.Send(patientName, patientID, doctorMail, anaylsis, analysisType, value)
            self.labelInfo.setText('Forwarded')
            self.message('Information',
                         'Details have been successfully communicated to the doctor.',
                         buttonStatusOk=True)
            self.lineEditPatientName.clear()
            self.lineEditPatientID.clear()
            self.lineEditDoctorMail.clear()
        except:
            self.labelInfo.setText('Error')
            self.message('Warning',
                         'Something went wrong!',
                         buttonStatusOk=True)

    def checkPneumonia(self):
        self.selectButton('pushButtonPneumonia')
        StyleSheet = "QProgressBar {\n    naborder-radius: 10px;\n    background-color: rgb(236, 236, 236);\n}\n\nQProgressBar:chunk{\n    border-radius: 10px;\n    background-color: rgb(4, 191, 123);\n}"
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File',os.path.basename('/test/PneumoniaTest/'), "All Files (*);; PNG Files (*.png);; JPG Files (*.jpg)")
        url = fname[0].replace('/','\\')
        self.pixmap = QPixmap(url)
        self.label_3.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        self.label_3.setScaledContents(True)
        self.label_3.setPixmap(self.pixmap)
        self.progressBar.setStyleSheet(StyleSheet.replace('242, 56, 71', '4, 191, 123'))

        img = PneumoniaDetect.Preprocessing(self,url)
        value = PneumoniaDetect.detect(self,img)
        self.Progress(value, StyleSheet)
        value = '%.4f' % value
        self.pushButtonSendDetail.clicked.connect(lambda: self.sendDetail(url, 'Pneumonia', value))

    def Progress(self, value, StyleSheet):
        i = 0
        while i <= value:
            if i > 50 and i < 74:
                self.progressBar.setStyleSheet(StyleSheet.replace('4, 191, 123', '211, 154, 9'))
            elif i > 75:
                self.progressBar.setStyleSheet(StyleSheet.replace('4, 191, 123', '242, 56, 71'))
            time.sleep(0.02)
            self.progressBar.setValue(i)
            i += 1

    def message(self, mType, message, buttonStatusOk=False, buttonStatusYes=False, buttonStatusNo=False,
                buttonOpen=False, buttonCancel=False):
        messageBox = QtWidgets.QMessageBox()
        # <------ Information / Warning / Question / Critical ------>
        if mType == "Information":
            messageBox.setIcon(QtWidgets.QMessageBox.Information)
        elif mType == "Warning":
            messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        elif mType == "Question":
            messageBox.setIcon(QtWidgets.QMessageBox.Question)
        elif mType == "Critical":
            messageBox.setIcon(QtWidgets.QMessageBox.Critical)

        messageBox.setText(message)
        messageBox.setWindowTitle(mType)
        if not buttonStatusOk == False:
            messageBox.addButton(QtWidgets.QMessageBox.Ok)
        if not buttonStatusYes == False:
            messageBox.addButton(QtWidgets.QMessageBox.Yes)
        if not buttonStatusNo == False:
            messageBox.addButton(QtWidgets.QMessageBox.No)
        if not buttonOpen == False:
            messageBox.addButton(QtWidgets.QPushButton("Open"), QtWidgets.QMessageBox.YesRole)
        if not buttonCancel == False:
            messageBox.addButton(QtWidgets.QPushButton("Cancel"), QtWidgets.QMessageBox.NoRole)

        retval = messageBox.exec_()
        return retval

if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = Ui()
        window.show()
        app.exec_()
    except Exception as f:
        print(f)