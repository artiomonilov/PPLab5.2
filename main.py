import sys
import random
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preia citat aleatoriu")
        self.resize(600, 300)
        
        citat_zilnic = self.alege_citat("citate.txt")

        print(citat_zilnic)

    def randomCitat(self, locatie):
        if not os.path.exists(locatie):
            return "Fișierul citate.txt nu a putut fi găsit."
        try:
            with open(locatie, "r", encoding="utf-8") as file:
                linii = [linie.strip() for linie in file.readlines() if linie.strip()]
                print(linii)
            if not linii:
                return "Fișierul de citate este gol."
            return random.choice(linii)
        except Exception as e:
            return f"Eroare la citirea fișierului: {str(e)}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
