"""Runs the GUI for VanillaInstaller."""
# IMPORTS
import argparse
import webbrowser
import pathlib
from PySide6.QtCore import QCoreApplication, QRect, Qt, QRunnable, QThreadPool, Slot
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QWidget,
    QGraphicsColorizeEffect,
    QFileDialog
)
from PySide6.QtSvgWidgets import QSvgWidget
import minecraft_launcher_lib as mll

# External
import requests

# LOCAL
import main
import theme
from log import logger

# ARGUMENTS
parser = argparse.ArgumentParser()
parser.add_argument("--safegui", type=bool)
parser.add_argument("--litegui", type=bool)
args = parser.parse_args()
FONT = "Inter"


def run():
    """Runs the GUI."""
    app = QApplication([])
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    get_versions_worker = Worker(ui.addVersions)
    ui.threadpool.start(get_versions_worker)
    window.show()
    app.exec()
class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMinimumSize(600, 400)
        self.threadpool = QThreadPool(MainWindow)
        font = QFont()
        font.setFamily(FONT)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        fontSize24 = QFont()
        fontSize24.setPointSize(24)
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName("title")
        self.title.setGeometry(QRect(137, 42, 326, 40))
        self.title.setFont(fontSize24)
        self.title.setAlignment(Qt.AlignCenter)
        self.subtitle = QLabel(self.centralwidget)
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setGeometry(QRect(0, 100, 600, 30))
        fontSize15 = QFont()
        fontSize15.setPointSize(15)
        self.subtitle.setFont(fontSize15)
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.installButton = QPushButton(self.centralwidget)
        self.installButton.setObjectName("installButton")
        self.installButton.setGeometry(QRect(225, 164, 150, 50))
        self.installButton.setFont(fontSize15)
        self.installButton.clicked.connect(self.startInstall)
        fontSize12 = QFont()
        fontSize12.setPointSize(12)
        self.versionSelector = QComboBox(self.centralwidget)
        self.versionSelector.setObjectName("versionSelector")
        self.versionSelector.setGeometry(QRect(326, 240, 98, 20))
        self.versionSelector.setFont(fontSize12)
        self.versionLabel = QLabel(self.centralwidget)
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setGeometry(QRect(175, 240, 149, 20))
        self.versionLabel.setFont(fontSize12)
        self.versionLabel.setAlignment(Qt.AlignCenter)
        self.locationLabel = QLabel(self.centralwidget)
        self.locationLabel.setObjectName("locationLabel")
        self.locationLabel.setGeometry(QRect(130, 300, 100, 20))
        self.locationLabel.setFont(fontSize12)
        self.locationLabel.setAlignment(Qt.AlignCenter)

        self.selectedLocation = QTextEdit(self.centralwidget)
        self.selectedLocation.setObjectName("selectedLocation")
        self.selectedLocation.setGeometry(QRect(236, 295, 190, 30))
        self.selectedLocation.setFont(fontSize12)
        self.selectedLocation.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.selectedLocation.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.selectedLocation.setText(main.get_dir())
        self.selectedLocation.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self.locationSelector = QPushButton(self.centralwidget)
        self.locationSelector.setObjectName("locationSelector")
        self.locationSelector.setGeometry(QRect(440, 295, 30, 30))
        self.locationSelector.clicked.connect(
            lambda: self.selectDirectory(self.centralwidget))
        self.locationSelectorIcon = QSvgWidget(
            Ui_MainWindow.getAsset("folder.svg"), self.locationSelector)
        self.locationSelectorIcon.setGeometry(5, 5, 20, 20)

        self.infoButton = QPushButton("GitHub", self.centralwidget)
        self.infoButton.setObjectName("infoButton")
        self.infoButton.setGeometry(QRect(10, 366, 84, 24))
        self.infoButton.setFlat(True)
        self.infoButton.clicked.connect(lambda: webbrowser.open(
            "https://github.com/Fabulously-Optimized/vanilla-installer/"))
        self.infoButtonIcon = QSvgWidget(
            Ui_MainWindow.getAsset("github.svg"), self.infoButton)
        self.infoButtonIcon.setGeometry(0, 0, 24, 24)

        self.issuesButton = QPushButton("Report bugs", self.centralwidget)
        self.issuesButton.setObjectName("issuesButton")
        self.issuesButton.setGeometry(QRect(10, 332, 108, 24))
        self.issuesButton.setFlat(True)
        self.issuesButton.clicked.connect(lambda: webbrowser.open(
            "https://github.com/Fabulously-Optimized/vanilla-installer/issues"))
        self.issuesButtonIcon = QSvgWidget(
            Ui_MainWindow.getAsset("flag.svg"), self.issuesButton)
        self.issuesButtonIcon.setGeometry(0, 0, 24, 24)

        self.themeToggle = QPushButton(self.centralwidget)
        self.themeToggle.setObjectName("themeToggle")
        self.themeToggle.setGeometry(QRect(566, 366, 24, 24))
        self.themeToggle.setFlat(True)
        self.themeToggle.clicked.connect(self.toggleTheme)
        self.themeToggleIcon = QSvgWidget(self.themeToggle)
        self.themeToggleIcon.setGeometry(0, 0, 24, 24)

        self.reloadTheme()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Vanilla Installer", None)
        )
        self.title.setText(
            QCoreApplication.translate(
                "MainWindow", "Fabulously Optimized", None)
        )
        self.subtitle.setText(
            QCoreApplication.translate("MainWindow", "Vanilla Installer", None)
        )
        self.installButton.setText(
            QCoreApplication.translate("MainWindow", "Install", None)
        )
        self.versionLabel.setText(
            QCoreApplication.translate(
                "MainWindow", "Minecraft version:", None)
        )
        self.locationLabel.setText(
            QCoreApplication.translate("MainWindow", "Location:", None)
        )

    def reloadTheme(self):
        loaded_theme = theme.load()
        self.centralwidget.setStyleSheet(
            f'[objectName^="centralwidget"] {{ background-color: { loaded_theme.get("base")} }}'
        )
        self.title.setStyleSheet(f'color: { loaded_theme.get("text")}')
        self.subtitle.setStyleSheet(f'color: { loaded_theme.get("subtitle") }')

        self.installButton.setStyleSheet(
            f'QPushButton {{ border: none; background: {loaded_theme.get("blue")}; color: {loaded_theme.get("base")}; border-radius: 5px; }}'
            f'QPushButton:hover {{ background: {loaded_theme.get("lavender")};}}'
            f'QPushButton:pressed {{ background: {loaded_theme.get("installbuttonpressed")};}}'
        )
        self.locationSelector.setStyleSheet(
            f'QPushButton {{ border: none;background: {loaded_theme.get("button")}; border-radius: 5px; }}'
            f'QPushButton:hover {{ background: {loaded_theme.get("buttonhovered")}; }}'
            f'QPushButton:pressed {{ background: {loaded_theme.get("buttonpressed")}; }}'
        )
        self.infoButton.setStyleSheet(
            f'QPushButton{{ color: #00000000 }}'
            f'QPushButton:hover {{ color: {loaded_theme.get("label")}; text-align: left; padding-left: 30px}}'
        )
        self.issuesButton.setStyleSheet(
            f'QPushButton{{ color: #00000000 }}'
            f'QPushButton:hover {{ color: {loaded_theme.get("label")}; text-align: left; padding-left: 30px}}'
        )


        self.versionLabel.setStyleSheet(
            f'color: {loaded_theme.get("label")}')
        self.locationLabel.setStyleSheet(
            f'color: {loaded_theme.get("label")}')
        self.selectedLocation.setStyleSheet(
            f'color: {loaded_theme.get("text")}; background-color: {loaded_theme.get("crust")}'
        )
        self.themeToggleIcon.load(Ui_MainWindow.getAsset(
            "moon.svg" if theme.is_dark() else "sun.svg"))
        # each effect can only apply to one widget
        effect1 = QGraphicsColorizeEffect(self.centralwidget)
        effect1.setColor(loaded_theme.get("icon"))
        self.locationSelectorIcon.setGraphicsEffect(effect1)
        effect2 = QGraphicsColorizeEffect(self.centralwidget)
        effect2.setColor(loaded_theme.get("icon"))
        self.infoButtonIcon.setGraphicsEffect(effect2)
        effect3 = QGraphicsColorizeEffect(self.centralwidget)
        effect3.setColor(loaded_theme.get("icon"))
        self.issuesButtonIcon.setGraphicsEffect(effect3)
        effect4 = QGraphicsColorizeEffect(self.centralwidget)
        effect4.setColor(loaded_theme.get("icon"))
        self.themeToggleIcon.setGraphicsEffect(effect4)
    def addVersions(self):
        for version in main.get_pack_mc_versions():
            self.versionSelector.addItem(version)
        self.versionSelector.setCurrentIndex(0)

    def getAsset(asset) -> str:
        return str((pathlib.Path(__file__).parent / "assets" / asset).resolve())

    def toggleTheme(self):
        theme.toggle()
        self.reloadTheme()

    def selectDirectory(self, parent):
        dialog = QFileDialog(parent, QCoreApplication.translate(
            "MainWindow", "Select .minecraft folder", None))
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        current_path = pathlib.Path(
            self.selectedLocation.toPlainText()).absolute()
        if not current_path.exists():
            current_path = pathlib.Path(
                mll.utils.get_minecraft_directory()).absolute()
        dialog.setDirectory(str(current_path))
        if dialog.exec():
            self.selectedLocation.setText(dialog.selectedFiles()[0])

    def startInstall(self):
        version = self.versionSelector.itemText(
            self.versionSelector.currentIndex())
        location = self.selectedLocation.toPlainText()
        worker = Worker(lambda: main.run(self.subtitle, location, version))
        self.threadpool.start(worker)


class Worker(QRunnable):
    def __init__(self, fn):
        super(Worker, self).__init__()
        self.fn = fn

    @Slot()
    def run(self):
        self.fn()


if __name__ == "__main__":
    run()
