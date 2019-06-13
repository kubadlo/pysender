import sys

from PyQt5.QtWidgets import *


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
        quit_action.setShortcut("Ctrl+Q")
        quit_action.setStatusTip("Close the application")
        quit_action.triggered.connect(self.quit_application)

        send_action = QAction("&Send", self)
        send_action.setShortcut("Ctrl+Enter")
        send_action.setStatusTip("Send message to all recipients")
        send_action.triggered.connect(self.send_message)

        reset_action = QAction("&Reset", self)
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
        action_menu.addAction(send_action)
        action_menu.addAction(reset_action)

        about_menu = menu_bar.addMenu("&Help")
        about_menu.addAction(about_action)

    @staticmethod
    def send_message():
        dialog = ErrorDialog("Missing implementation", "The action is not implemented yet")
        dialog.exec_()

    @staticmethod
    def reset_input():
        dialog = ErrorDialog("Missing implementation", "The action is not implemented yet")
        dialog.exec_()

    @staticmethod
    def show_info(self):
        dialog = AboutDialog()
        dialog.exec_()

    @staticmethod
    def quit_application():
        sys.exit(0)
