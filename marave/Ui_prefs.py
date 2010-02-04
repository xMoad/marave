# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'marave/prefs.ui'
#
# Created: Thu Feb  4 14:20:02 2010
#      by: PyQt4 UI code generator 4.6.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(396, 106)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.close = QtGui.QToolButton(Form)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/close.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.close.setIcon(icon)
        self.close.setObjectName("close")
        self.horizontalLayout_2.addWidget(self.close)
        spacerItem = QtGui.QSpacerItem(56, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.themeList = QtGui.QComboBox(Form)
        self.themeList.setObjectName("themeList")
        self.horizontalLayout.addWidget(self.themeList)
        self.saveTheme = QtGui.QToolButton(Form)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/save.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveTheme.setIcon(icon1)
        self.saveTheme.setObjectName("saveTheme")
        self.horizontalLayout.addWidget(self.saveTheme)
        self.formLayout.setLayout(0, QtGui.QFormLayout.FieldRole, self.horizontalLayout)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.langBox = QtGui.QComboBox(Form)
        self.langBox.setObjectName("langBox")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.langBox)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.buttonStyle = QtGui.QComboBox(Form)
        self.buttonStyle.setObjectName("buttonStyle")
        self.buttonStyle.addItem("")
        self.buttonStyle.addItem("")
        self.buttonStyle.addItem("")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.buttonStyle)
        self.horizontalLayout_2.addLayout(self.formLayout)
        spacerItem1 = QtGui.QSpacerItem(55, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.close.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Theme:", None, QtGui.QApplication.UnicodeUTF8))
        self.saveTheme.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Spell Checking:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Buttons:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonStyle.setItemText(0, QtGui.QApplication.translate("Form", "Icons", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonStyle.setItemText(1, QtGui.QApplication.translate("Form", "Text", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonStyle.setItemText(2, QtGui.QApplication.translate("Form", "Text + Icons", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

