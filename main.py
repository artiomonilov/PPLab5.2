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
        
        self.init_dbs()
        self.importa_citate_default()
        
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

    def init_dbs(self):
        quotesConn = sqlite3.connect("quotes.db")
        quotesCursor = quotesConn.cursor()
        quotesCursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            content TEXT
        )
        ''')
        quotesConn.commit()
        quotesConn.close()
    
        jurnalConn = sqlite3.connect("journal.db")
        jurnalCursor = jurnalConn.cursor()
        jurnalCursor.execute('''
            CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            content TEXT
        ) ''')
        jurnalConn.commit()
        jurnalConn.close()

    def importa_citate_default(self):
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM quotes")
        if cursor.fetchone()[0] == 0:
            citate_initiale = [
                ("Nelson Mandela", "Cea mai mare glorie in viata nu sta in a nu cadea niciodata, ci in a ne ridica de fiecare data cand cadem."),
                ("Steve Jobs", "Singurul mod de a realiza o munca excelenta este sa iubesti ceea ce faci."),
                ("Albert Einstein", "Imaginatia este mai importanta decat cunoasterea."),
                ("Eleanor Roosevelt", "Viitorul apartine celor care cred in frumusetea visurilor lor.")
            ]
            cursor.executemany("INSERT INTO quotes (author, content) VALUES (?, ?)", citate_initiale)
            conn.commit()
        conn.close()

    def preia_citat_random(self):
        try:
            conn = sqlite3.connect("quotes.db")
            cursor = conn.cursor()
            cursor.execute("SELECT author, content FROM quotes ORDER BY RANDOM() LIMIT 1")
            rezultat = cursor.fetchone()
            conn.close()
            
            if not rezultat:
                return "Nimic gasit in baza de date."
            
            return f'"{rezultat[1]}"\n\n— {rezultat[0]}'
        except Exception as e:
            return f"Eroare DB: {str(e)}"
    
    def add_quote(self, author, content):
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO quotes (author, content) VALUES (?, ?)", (author, content))
        conn.commit()
        conn.close()
        
    def add_jr(self, date, val):
        conn = sqlite3.connect("journal.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO entries (date, content) VALUES (?, ?)", (date, val))
        conn.commit()
        conn.close()
    
    def get_quotes(self):
        conn = sqlite3.connect("quotes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quotes")
        data = cursor.fetchall()
        conn.close()
        return data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
