# Copyright (C) Fabulously Optimized 2022
# Licensed under the MIT License. The full license text can be found at https://github.com/Fabulously-Optimized/vanilla-installer/blob/main/LICENSE.md.
"""Runs the GUI for VanillaInstaller."""
# IMPORTS
import pathlib
import webbrowser
import sys

import minecraft_launcher_lib as mll
from PySide6.QtCore import QCoreApplication, QRect, QRunnable, Qt, QThreadPool, Slot
from PySide6.QtGui import QFont, QIcon, QFontDatabase
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QGraphicsColorizeEffect,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QWidget,
    QCheckBox,
)

# LOCAL
from vanilla_installer import main, theme

# ARGUMENTS
FONT_FILE = pathlib.Path("data/font.txt").resolve()


def run() -> None:
    """Runs the GUI."""
    global global_font
    if FONT_FILE.exists():
        setFont(FONT_FILE.read_text() == "OpenDyslexic")
    else:
        setFont(False)
    try:
        from . import fonts
    except:
        print("resource file for fonts isn't generated!\nrun `pyside6-rcc vanilla_installer/assets/fonts.qrc -o vanilla_installer/fonts.py` in the root directory of the project to generate them. you might need to source the venv.")

    app = QApplication([])
    QFontDatabase.addApplicationFont(":Inter-Regular.otf")
    QFontDatabase.addApplicationFont(":OpenDyslexic-Regular.otf")
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)
    get_versions_worker = Worker(ui.addVersions)
    ui.threadpool.start(get_versions_worker)
    window.show()
    app.exec()


def setFont(opendyslexic: bool):
    global global_font 
    if opendyslexic:
        global_font = "OpenDyslexic"
    else:
        # For some reason the Inter font on Linux is called `Inter` and on Windows it's called `Inter Regular`
        # And thus, this janky solution
        # I'm not sure what it's called on MacOS so hopefully it's the same as linux cause i can't test it
        # Either ways it would be a better idea to move to a font that doesn't have this issue
        inter_name = "Inter"
        if sys.platform.startswith("win32"):
            inter_name = "Inter Regular"
        global_font = inter_name
    FONT_FILE.write_text(global_font)
        
class Ui_MainWindow(object):
    def setupUi(self, MainWindow: QMainWindow) -> None:
        """Setup the PySide6 (aka Qt) UI.

        Args:
            MainWindow (QMainWindow): The main window.
        """
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 400)
        MainWindow.setMinimumSize(600, 400)

        self.threadpool = QThreadPool(MainWindow)
        self.installing = False

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.title = QLabel(self.centralwidget)
        self.title.setObjectName("title")
        self.title.setGeometry(QRect(0, 42, 600, 40))
        self.title.setAlignment(Qt.AlignCenter)
        self.subtitle = QLabel(self.centralwidget)
        self.subtitle.setObjectName("subtitle")
        self.subtitle.setGeometry(QRect(0, 100, 600, 30))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.installButton = QPushButton(self.centralwidget)
        self.installButton.setObjectName("installButton")
        self.installButton.setGeometry(QRect(225, 164, 150, 50))
        self.installButton.clicked.connect(
            lambda: self.threadpool.start(Worker(self.startInstall))
        )
        self.versionSelector = QComboBox(self.centralwidget)
        self.versionSelector.setObjectName("versionSelector")
        self.versionSelector.setGeometry(QRect(326, 240, 98, 20))
        self.versionLabel = QLabel(self.centralwidget)
        self.versionLabel.setObjectName("versionLabel")
        self.versionLabel.setGeometry(QRect(130, 240, 195, 25))
        self.versionLabel.setAlignment(Qt.AlignLeft)
        self.locationLabel = QLabel(self.centralwidget)
        self.locationLabel.setObjectName("locationLabel")
        self.locationLabel.setGeometry(QRect(130, 300, 100, 25))
        self.locationLabel.setAlignment(Qt.AlignLeft)

        self.selectedLocation = QTextEdit(self.centralwidget)
        self.selectedLocation.setObjectName("selectedLocation")
        self.selectedLocation.setGeometry(QRect(236, 295, 190, 30))
        self.selectedLocation.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.selectedLocation.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.selectedLocation.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.selectedLocation.setText(main.get_dir())

        self.locationSelector = QPushButton(self.centralwidget)
        self.locationSelector.setObjectName("locationSelector")
        self.locationSelector.setGeometry(QRect(440, 295, 30, 30))
        self.locationSelector.clicked.connect(
            lambda: self.selectDirectory(self.centralwidget)
        )
        self.locationSelectorIcon = QSvgWidget(
            Ui_MainWindow.getAsset("folder.svg"), self.locationSelector
        )
        self.locationSelectorIcon.setGeometry(5, 5, 20, 20)

        self.infoButton = QPushButton(self.centralwidget)
        self.infoButton.setObjectName("infoButton")
        self.infoButton.setGeometry(QRect(10, 366, 84, 24))
        self.infoButton.setFlat(True)
        self.infoButton.clicked.connect(
            lambda: webbrowser.open(
                "https://github.com/Fabulously-Optimized/vanilla-installer/"
            )
        )
        self.infoButtonIcon = QSvgWidget(
            Ui_MainWindow.getAsset("github.svg"), self.infoButton
        )
        self.infoButtonIcon.setGeometry(0, 0, 24, 24)

        self.issuesButton = QPushButton(self.centralwidget)
        self.issuesButton.setObjectName("issuesButton")
        self.issuesButton.setGeometry(QRect(10, 332, 108, 24))
        self.issuesButton.setFlat(True)
        self.issuesButton.clicked.connect(
            lambda: webbrowser.open(
                "https://github.com/Fabulously-Optimized/vanilla-installer/issues"
            )
        )
        self.issuesButtonIcon = QSvgWidget(
            Ui_MainWindow.getAsset("flag.svg"), self.issuesButton
        )
        self.issuesButtonIcon.setGeometry(0, 0, 24, 24)

        self.themeToggle = QPushButton(self.centralwidget)
        self.themeToggle.setObjectName("themeToggle")
        self.themeToggle.setGeometry(QRect(456, 366, 134, 24))
        self.themeToggle.setFlat(True)
        self.themeToggle.clicked.connect(self.toggleTheme)
        self.themeToggleIcon = QSvgWidget(self.themeToggle)
        self.themeToggleIcon.setGeometry(110, 0, 24, 24)

        self.settingsButton = QPushButton(self.centralwidget)
        self.settingsButton.setObjectName("settingsButton")
        self.settingsButton.setGeometry(QRect(496, 332, 94, 24))
        self.settingsButton.setFlat(True)
        self.settingsButton.clicked.connect(self.openSettings)
        self.settingsButtonIcon = QSvgWidget(
            Ui_MainWindow.getAsset("settings.svg"), self.settingsButton
        )
        self.settingsButtonIcon.setGeometry(70, 0, 24, 24)

        self.reloadTheme()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow: QMainWindow) -> None:
        """Retranslate the UI.

        Args:
            MainWindow (QMainWindow): The main window.
        """
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "Vanilla Installer", None)
        )
        self.title.setText(
            QCoreApplication.translate("MainWindow", "Fabulously Optimized", None)
        )
        self.subtitle.setText(
            QCoreApplication.translate("MainWindow", "Vanilla Installer", None)
        )
        self.installButton.setText(
            QCoreApplication.translate("MainWindow", "Install", None)
        )
        self.versionLabel.setText(
            QCoreApplication.translate("MainWindow", "Minecraft version:", None)
        )
        self.locationLabel.setText(
            QCoreApplication.translate("MainWindow", "Location:", None)
        )
        self.infoButton.setText(
            QCoreApplication.translate("MainWindow", "GitHub", None)
        )
        self.issuesButton.setText(
            QCoreApplication.translate("MainWindow", "Report bugs", None)
        )
        self.themeToggle.setText(
            QCoreApplication.translate("MainWindow", "Toggle theme", None)
        )
        self.settingsButton.setText(
            QCoreApplication.translate("MainWindow", "Settings", None)
        )

    def reloadTheme(self) -> None:
        """Reload the theme. Doesn't take any arguments."""
        loaded_theme = theme.load()
        self.centralwidget.setStyleSheet(
            f'[objectName^="centralwidget"] {{ background-color: { loaded_theme.get("base")} }}'
        )
        self.title.setStyleSheet(
            f'color: { loaded_theme.get("text")}; font: 24pt "{global_font}"'
        )
        self.subtitle.setStyleSheet(
            f'color: { loaded_theme.get("subtitle") }; font: 15pt "{global_font}"'
        )

        self.installButton.setStyleSheet(
            f'QPushButton {{ border: none; background: {loaded_theme.get("blue")}; color: {loaded_theme.get("base")}; border-radius: 5px; font: 15pt "{global_font}"}}'
            f'QPushButton:hover {{ background: {loaded_theme.get("lavender")};}}'
            f'QPushButton:pressed {{ background: {loaded_theme.get("installbuttonpressed")};}}'
        )
        self.locationSelector.setStyleSheet(
            f'QPushButton {{ border: none;background: {loaded_theme.get("button")}; border-radius: 5px; font-family: "{global_font}" }}'
            f'QPushButton:hover {{ background: {loaded_theme.get("buttonhovered")}; }}'
            f'QPushButton:pressed {{ background: {loaded_theme.get("buttonpressed")}; }}'
        )
        self.infoButton.setStyleSheet(
            f'QPushButton{{ color: #00000000; font-family: "{global_font}"}}'
            f'QPushButton:hover {{ color: {loaded_theme.get("label")}; text-align: left; padding-left: 30px}}'
        )
        self.issuesButton.setStyleSheet(
            f'QPushButton{{ color: #00000000; font-family: "{global_font}"}}'
            f'QPushButton:hover {{ color: {loaded_theme.get("label")}; text-align: left; padding-left: 30px}}'
        )
        self.themeToggle.setStyleSheet(
            f'QPushButton{{ color: #00000000; font-family: "{global_font}"}}'
            f'QPushButton:hover {{ color: {loaded_theme.get("label")}; text-align: right; padding-right: 30px}}'
        )
        self.settingsButton.setStyleSheet(
            f'QPushButton{{ color: #00000000; font-family: "{global_font}"}}'
            f'QPushButton:hover {{ color: {loaded_theme.get("label")}; text-align: right; padding-right: 30px}}'
        )

        self.versionLabel.setStyleSheet(
            f'color: {loaded_theme.get("label")}; font: 12pt "{global_font}"'
        )
        self.versionSelector.setStyleSheet(
            f'font: 12pt "{global_font}"'
        )
        self.locationLabel.setStyleSheet(
            f'color: {loaded_theme.get("label")}; font: 12pt "{global_font}"'
        )
        self.selectedLocation.setStyleSheet(
            f'color: {loaded_theme.get("text")}; background-color: {loaded_theme.get("crust")}; font: 12pt "{global_font}"'
        )
        self.themeToggleIcon.load(
            Ui_MainWindow.getAsset("moon.svg" if theme.is_dark() else "sun.svg")
        )
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
        effect5 = QGraphicsColorizeEffect(self.centralwidget)
        effect5.setColor(loaded_theme.get("icon"))
        self.settingsButtonIcon.setGraphicsEffect(effect5)

    def addVersions(self) -> None:
        """Adds the versions to the version selector."""
        for version in main.get_pack_mc_versions().keys():
            self.versionSelector.addItem(version)
        self.versionSelector.setCurrentIndex(0)

    def getAsset(asset) -> str:
        """Get the path to a given asset.

        Args:
            asset (str): The asset to get.

        Returns:
            str: The complete path to the asset.
        """
        return str((pathlib.Path(__file__).parent / "assets" / asset).resolve())

    def toggleTheme(self) -> None:
        """Toggle the theme."""
        theme.toggle()
        self.reloadTheme()

    def selectDirectory(self, parent) -> None:
        """Select a directory

        Args:
            parent (str): The parent directory.
        """
        dialog = QFileDialog(
            parent,
            QCoreApplication.translate("MainWindow", "Select .minecraft folder", None),
        )
        dialog.setFileMode(QFileDialog.FileMode.Directory)
        current_path = pathlib.Path(self.selectedLocation.toPlainText()).absolute()
        if not current_path.exists():
            current_path = pathlib.Path(mll.utils.get_minecraft_directory()).absolute()
        dialog.setDirectory(str(current_path))
        if dialog.exec():
            self.selectedLocation.setText(dialog.selectedFiles()[0])

    def openSettings(self) -> None:
        """Open the settings."""
        dialog = SettingsDialog(self)
        dialog.exec()

    def startInstall(self) -> None:
        """Start the installation process."""
        # make sure the installation process is only running once
        if self.installing is True:
            return
        version = self.versionSelector.itemText(self.versionSelector.currentIndex())
        location = self.selectedLocation.toPlainText()
        self.installing = True
        if version.startswith("1.16"):
            java_ver = 8
        elif version.startswith("1.17"):
            java_ver = 16
        else:
            java_ver = 17.3
        main.run(location, version, java_ver, widget=self.subtitle)
        self.installing = False


class SettingsDialog(QDialog):
    """The settings dialog.

    Args:
        QDialog (QDialog): The dialog.
    """

    parentWindow: Ui_MainWindow

    def __init__(self, parent) -> None:
        self.parentWindow = parent
        super().__init__(self.parentWindow.centralwidget)
        self.setupUi()

    def setupUi(self) -> None:
        """Setup the UI for the settings dialog."""
        if not self.objectName():
            self.setObjectName("Dialog")
        self.setMinimumSize(400, 250)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setGeometry(QRect(180, 190, 200, 40))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Save
        )
        self.buttonBox.setCenterButtons(False)

        for button in self.buttonBox.buttons():
            button.setIcon(QIcon())  # remove the button icons

        self.fontDyslexicCheckbox = QCheckBox(self)
        self.fontDyslexicCheckbox.setCheckState(
            Qt.CheckState.Checked
            if global_font == "OpenDyslexic"
            else Qt.CheckState.Unchecked
        )
        self.fontDyslexicCheckbox.stateChanged.connect(self.changeFont)
        self.fontDyslexicCheckbox.setGeometry(QRect(10, 10, 380, 20))

        self.errorLabel = QLabel(self)
        self.errorLabel.setWordWrap(True)
        self.errorLabel.setGeometry(QRect(20, 200, 200, 20))
        self.reloadTheme()
        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def accept(self) -> None:
        """Accept Button actions"""
        super().accept()

    def retranslateUi(self, Dialog) -> None:
        """Retranslate UI for the set dialog.

        Args:
            Dialog: The dialog.
        """
        Dialog.setWindowTitle(
            QCoreApplication.translate("Dialog", "Vanilla Installer Settings", None)
        )
        self.fontDyslexicCheckbox.setText(
            QCoreApplication.translate("Dialog", "Enable dyselxia friendly font", None)
        )

    def reloadTheme(self) -> None:
        """Reload the theme."""
        loaded_theme = theme.load()
        self.setStyleSheet(
            f'[objectName^="Dialog"] {{ background-color: {loaded_theme.get("base")}}}'
        )
        self.buttonBox.setStyleSheet(
            f'QPushButton {{ border: none; background-color: { loaded_theme.get("button") } ; color: {loaded_theme.get("text")}; padding: 8px; border-radius: 5px; font-family: "{global_font}"}}'
            f'QPushButton:hover {{ background-color: { loaded_theme.get("buttonhovered") }}}'
            f'QPushButton:hover {{ background-color: { loaded_theme.get("buttonpressed") }}}'
        )
        self.fontDyslexicCheckbox.setStyleSheet(
            f'color: {loaded_theme.get("label")}; font-family: "{global_font}"'
        )

        self.errorLabel.setStyleSheet(
            f'color: {loaded_theme.get("red")}; font: 8pt "{global_font}"'
        )

    def changeFont(self, state) -> None:
        """Toggle font between OpenDyslexic and Inter

        Args:
            state: int, 2 implies a checked state and 0 would mean unchecked
        """
        setFont(state == 2)
        self.reloadTheme()
        self.parentWindow.reloadTheme()


class Worker(QRunnable):
    def __init__(self, fn) -> None:
        super(Worker, self).__init__()
        self.fn = fn

    @Slot()
    def run(self):
        self.fn()


if __name__ == "__main__":
    run()
