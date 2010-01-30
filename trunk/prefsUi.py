# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefs.ui'
#
# Created: Sat Jan 30 17:24:13 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(243, 101)
        self.formLayout = QtGui.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadTheme = QtGui.QToolButton(Form)
        self.loadTheme.setObjectName("loadTheme")
        self.horizontalLayout.addWidget(self.loadTheme)
        self.saveTheme = QtGui.QToolButton(Form)
        self.saveTheme.setObjectName("saveTheme")
        self.horizontalLayout.addWidget(self.saveTheme)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.labelbuttons = QtGui.QCheckBox(Form)
        self.labelbuttons.setObjectName("labelbuttons")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelbuttons)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label)
        self.langBox = QtGui.QComboBox(Form)
        self.langBox.setObjectName("langBox")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.langBox)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Theme:", None, QtGui.QApplication.UnicodeUTF8))
        self.loadTheme.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.saveTheme.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.labelbuttons.setText(QtGui.QApplication.translate("Form", "Label buttons", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Spell Checking:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

