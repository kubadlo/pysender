import re
import sys

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import *

from pysender.outlook import OutlookClient


class FormLabel(QLabel):
    def __init__(self, text):
        super(FormLabel, self).__init__()
        self.setText(text)
        self.setMinimumWidth(60)


class AboutDialog(QMessageBox):
    def __init__(self):
        super(AboutDialog, self).__init__()
        self.setWindowTitle("About")

        self.setIcon(QMessageBox.Information)
        self.setText("PySender version 1.0.0")
        self.setInformativeText("Bulk email sender for slow computers. "
                                "Make sure you have Outlook installed on your system.")

        self.setStandardButtons(QMessageBox.Close)


class ErrorDialog(QMessageBox):
    def __init__(self, title, message):
        super(ErrorDialog, self).__init__()
        self.setWindowTitle("Error")

        self.setIcon(QMessageBox.Warning)
        self.setText(title)
        self.setInformativeText(message)

        self.setStandardButtons(QMessageBox.Ok)


class MessageForm(QWidget):
    def __init__(self):
        super(MessageForm, self).__init__()

        self.from_field = QLineEdit()
        self.from_field.setDisabled(True)
        self.to_field = QTextEdit()
        self.subject_field = QLineEdit()
        self.message_field = QTextEdit()

        self.init_widgets()

    def init_widgets(self):
        address_form = QGridLayout()
        address_form.setSpacing(10)
        address_form.addWidget(FormLabel("From:"), 1, 0)
        address_form.addWidget(self.from_field, 1, 1)
        address_form.addWidget(FormLabel("To:"), 2, 0)
        address_form.addWidget(self.to_field, 2, 1, 2, 1)

        message_form = QGridLayout()
        message_form.setSpacing(10)
        message_form.addWidget(FormLabel("Subject:"), 1, 0)
        message_form.addWidget(self.subject_field, 1, 1)
        message_form.addWidget(FormLabel("Body:"), 2, 0)
        message_form.addWidget(self.message_field, 2, 1, 2, 1)

        address_group = QGroupBox("Addresses")
        address_group.setLayout(address_form)

        message_group = QGroupBox("Message")
        message_group.setLayout(message_form)

        main_layout = QBoxLayout(QBoxLayout.Down)
        main_layout.addWidget(address_group)
        main_layout.addWidget(message_group)

        self.setLayout(main_layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.message_form = MessageForm()

        self.init_window()
        self.init_menubar()

        self.statusBar()
        self.show()

    def init_window(self):
        self.setWindowTitle("PySender")
        self.setCentralWidget(self.message_form)
        self.resize(800, 600)

    def init_menubar(self):
        quit_action = QAction("&Quit", self)
        quit_action.setIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton))
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Close the application")
        quit_action.triggered.connect(self.quit_application)

        send_action = QAction("&Send", self)
        send_action.setIcon(self.style().standardIcon(QStyle.SP_DialogApplyButton))
        send_action.setShortcut("Ctrl+Enter")
        send_action.setStatusTip("Send message to all recipients")
        send_action.triggered.connect(self.send_message)

        reset_action = QAction("&Reset", self)
        reset_action.setIcon(self.style().standardIcon(QStyle.SP_DialogResetButton))
        reset_action.setShortcut("Ctrl+Del")
        reset_action.setStatusTip("Reset all entered data")
        reset_action.triggered.connect(self.reset_input)

        about_action = QAction("&About", self)
        about_action.setStatusTip("Show application info")
        about_action.triggered.connect(self.show_info)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(quit_action)

        action_menu = menu_bar.addMenu("&Action")
        action_menu.addActions([send_action, reset_action])

        about_menu = menu_bar.addMenu("&Help")
        about_menu.addAction(about_action)

        tool_bar = self.addToolBar("Main")
        tool_bar.setIconSize(QSize(18, 18))
        tool_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tool_bar.addActions([send_action, reset_action])

    def send_message(self):
        address_to = self.message_form.to_field.toPlainText()
        subject = self.message_form.subject_field.text()
        body_plain = self.message_form.message_field.toPlainText()
        body_html = self.message_form.message_field.toHtml()

        if not address_to:
            dialog = ErrorDialog("Missing data", "Please fill \"To\" field with recipients email addresses.")
            dialog.exec_()
            return
        else:
            address_to = re.sub(r"\s+", ";", address_to)

        if not subject:
            dialog = ErrorDialog("Missing data", "Please fill \"Subject\" field with email subject.")
            dialog.exec_()
            return

        if not body_plain or not body_html:
            dialog = ErrorDialog("Missing data", "Please fill \"Body\" field with some content.")
            dialog.exec_()
            return

        outlook_client = OutlookClient()
        outlook_client.send_email(address_to, subject, body_plain, body_html)

    def reset_input(self):
        self.message_form.to_field.setText("")
        self.message_form.subject_field.setText("")
        self.message_form.message_field.setText("")

    @staticmethod
    def show_info(self):
        dialog = AboutDialog()
        dialog.exec_()

    @staticmethod
    def quit_application():
        sys.exit(0)
