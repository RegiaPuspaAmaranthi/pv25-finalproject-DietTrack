# style.py
style = """
* {
    font-family: 'Poppins', sans-serif;
    font-size: 10pt;
}

QMainWindow {
    background-color: #f5f9fd;
}

QLabel {
    color: #2c3e50;
}

/* Headings */
QLabel#labelTambah, QLabel#labelRiwayat, QLabel#labelStats {
    font-size: 16pt;
    font-weight: bold;
}

QPushButton {
    border: none;
    border-radius: 6px;
    padding: 6px 12px;
    color: white;
    font-weight: bold;
    transition: all 0.3s ease;
}

QPushButton#btnAdd {
    background-color: #27ae60;
}

QPushButton#btnUpdate {
    background-color: #2980b9;
}

QPushButton#btnDelete {
    background-color: #c0392b;
}

QPushButton#btnClear {
    background-color: #f39c12;
}

QPushButton#btnExport {
    background-color: #27ae60;
    font-size: 11pt;
}

QPushButton:hover {
    opacity: 0.85;
    background-color: #1abc9c;
}

QLineEdit, QComboBox, QSpinBox, QDateEdit {
    background-color: white;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px;
    font-size: 10pt;
}

QTableWidget {
    background-color: white;
    border: 1px solid #dcdde1;
    border-radius: 5px;
    gridline-color: #ecf0f1;
    font-size: 9pt;
}

QTableWidget::item {
    padding: 6px;
}

QHeaderView::section {
    background-color: #2c3e50;
    color: white;
    padding: 5px;
    border: none;
    font-weight: bold;
    font-size: 10pt;
}

QStatusBar {
    background-color: #ecf0f1;
    color: #2c3e50;
    font-size: 9pt;
    padding-left: 8px;
}

QMenuBar {
    background-color: #2c3e50;
    color: white;
}

QMenuBar::item {
    background: transparent;
    padding: 6px 12px;
}

QMenuBar::item:selected {
    background: #34495e;
}
"""
