import sys
import random
import os
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Preia citat aleatoriu")
        self.resize(600, 300)
        
        # citat_zilnic = self.randomCitat("citate.txt")
        citat_zilnic = self.preia_citat_random()

        widget_central = QWidget()
        layout = QVBoxLayout()
        
        eticheta_citat = QLabel(citat_zilnic)
        eticheta_citat.setAlignment(Qt.AlignCenter)
        eticheta_citat.setWordWrap(True)
        eticheta_citat.setStyleSheet("font-size: 18px; font-style: italic; padding: 20px; font-family: 'Segoe UI';")
        
        layout.addWidget(eticheta_citat)
        widget_central.setLayout(layout)
        self.setCentralWidget(widget_central)

    def preia_citat_random(self):
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT content FROM quotes")
        rezultate = cursor.fetchall()
        
        conn.close()
        
        if not rezultate:
            return "Nimic gasit"
        
        return random.choice(rezultate)[0]
    
    
    def randomCitat(self, locatie):
        if not os.path.exists(locatie):
            return "Fișierul citate.txt nu a putut fi găsit."
        try:
            with open(locatie, "r", encoding="utf-8") as file:
                linii = [linie.strip() for linie in file.readlines() if linie.strip()]
            if not linii:
                return "Fișierul de citate este gol."
            return random.choice(linii)
        except Exception as e:
            return f"Eroare la citirea fișierului: {str(e)}"

    def add_quote(author, content):
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO quotes (author, content) VALES (?, ?)",
            (author, content))

        conn.commit()
        conn.close()
        
    def add_jr(date, val):
        conn = sqlite3.connect("journal.db")
        cursor = conn.cursor()
        
        cursor.execute(
            "INSERT INTO entries (date, content) VALUES (?, ?)",
            (date, val))

        conn.commit()
        conn.close()
    
    def get_quotes():
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes")
        data = cursor.fetchall()
        
        conn.close()
        return data
        

    def init_dbs(self):
        quotesConn = sqlite3.connect("quotes.db")
        quotesCursor = quotesConn.cursor()
        quotesCursor.execute("""
            CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            content TEXT
        )
        """)
        quotesConn.commit()
        quotesConn.close()
    
        jurnalConn = sqlite3.connect("journal.db")
        jurnalCursor = jurnalConn.cursor()
        jurnalCursor.execute("""
            CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            content TEXT
        ) """)
        jurnalConn.commit()
        jurnalConn.close()

if __name__ == '__main__':

    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.init_dbs()
    sys.exit(app.exec_())
