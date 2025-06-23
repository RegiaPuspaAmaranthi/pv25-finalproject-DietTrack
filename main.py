# main.py
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QFileDialog
from PyQt5.QtGui import QFont
import sys
import sqlite3
import csv
import style

class DietTrackApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("dietTrack.ui", self)
        self.setWindowTitle("DietTrack")
        self.resize(809, 640)
        self.setStyleSheet(style.style)
        QtWidgets.QApplication.setFont(QFont("Poppins", 10))

        # Status bar tetap
        self.statusLabel = QtWidgets.QLabel("Regia Puspa Amaranthi - F1D022156")
        self.statusBar.addWidget(self.statusLabel)

        # Set default page to input form
        self.stackedWidget.setCurrentWidget(self.pageInput)

        # DB setup
        self.conn = sqlite3.connect("diet.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS diet_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                makanan TEXT,
                kategori TEXT,
                kalori INTEGER,
                catatan TEXT
            )
        """)

        # Event bindings
        self.btnAdd.clicked.connect(self.add_entry)
        self.btnUpdate.clicked.connect(self.update_entry)
        self.btnDelete.clicked.connect(self.delete_entry)
        self.btnClear.clicked.connect(self.clear_input)
        self.btnExport.clicked.connect(self.export_csv)
        self.tableWidget.itemSelectionChanged.connect(self.fill_form_from_table)

        self.actionInput.triggered.connect(lambda: (self.clear_input(), self.stackedWidget.setCurrentWidget(self.pageInput)))
        self.actionRiwayat.triggered.connect(self.load_data)
        self.actionStatistik.triggered.connect(self.show_stats)
        self.actionExport.triggered.connect(self.export_csv)
        self.actionSimpan.triggered.connect(self.add_entry)
        self.actionKeluar.triggered.connect(self.close)
        self.actionTentang.triggered.connect(lambda: QMessageBox.information(self, "Tentang Aplikasi", "DietTrack adalah aplikasi sederhana yang dirancang untuk membantu pengguna dalam mencatat dan memantau asupan makanan dan kalori harian secara praktis. Aplikasi ini menyediakan fitur pencatatan makanan, kategori konsumsi, serta statistik kalori harian yang disajikan secara informatif. Dengan antarmuka yang mudah digunakan, pengguna dapat melihat riwayat konsumsi, menyaring data, serta mengekspor catatan ke dalam file CSV."))
        self.actionBantuan.triggered.connect(lambda: QMessageBox.information(self, "Bantuan", "Gunakan menu Input untuk menambahkan data, Riwayat untuk melihat dan ekspor data, serta Statistik untuk melihat total kalori."))

        self.lineEdit_search.textChanged.connect(self.load_data)
        self.comboBox_filter.currentTextChanged.connect(self.load_data)

        self.lineEdit_note.setPlaceholderText("Catatan tambahan...")

        self.spinBox_calories.setMaximum(10000)

        # Resize table header
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(True)

        self.calendarWidget.selectionChanged.connect(self.show_stats)


        self.load_data()
        self.stackedWidget.setCurrentWidget(self.pageInput)


    def add_entry(self):
        tgl = self.dateEdit.date().toString("yyyy-MM-dd")
        food = self.lineEdit_food.text().strip()
        kategori = self.comboBox_category.currentText()
        kalori = self.spinBox_calories.value()
        catatan = self.lineEdit_note.text().strip()

        if not food:
            QMessageBox.warning(self, "Peringatan", "Nama makanan/minuman harus diisi!")
            return

        self.cursor.execute("""
            INSERT INTO diet_entries (tanggal, makanan, kategori, kalori, catatan)
            VALUES (?, ?, ?, ?, ?)
        """, (tgl, food, kategori, kalori, catatan))
        self.conn.commit()
        QMessageBox.information(self, "Berhasil", "Data berhasil disimpan.")
        self.clear_input()
        self.load_data()

    def update_entry(self):
        selected = self.tableWidget.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin diubah!")
            return

        id_data = self.tableWidget.item(selected, 0).data(QtCore.Qt.UserRole)
        tgl = self.dateEdit.date().toString("yyyy-MM-dd")
        food = self.lineEdit_food.text().strip()
        kategori = self.comboBox_category.currentText()
        kalori = self.spinBox_calories.value()
        catatan = self.lineEdit_note.text().strip()

        if not food:
            QMessageBox.warning(self, "Peringatan", "Nama makanan/minuman tidak boleh kosong.")
            return

        self.cursor.execute("""
            UPDATE diet_entries SET tanggal=?, makanan=?, kategori=?, kalori=?, catatan=?
            WHERE id=?
        """, (tgl, food, kategori, kalori, catatan, id_data))
        self.conn.commit()
        QMessageBox.information(self, "Berhasil", "Data berhasil diubah.")
        self.clear_input()
        self.load_data()

    def delete_entry(self):
        selected = self.tableWidget.currentRow()
        if selected < 0:
            QMessageBox.warning(self, "Peringatan", "Pilih data yang ingin dihapus.")
            return

        reply = QMessageBox.question(self, "Konfirmasi", "Yakin ingin menghapus data ini?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            id_data = self.tableWidget.item(selected, 0).data(QtCore.Qt.UserRole)
            self.cursor.execute("DELETE FROM diet_entries WHERE id=?", (id_data,))
            self.conn.commit()
            QMessageBox.information(self, "Berhasil", "Data berhasil dihapus.")
            self.clear_input()
            self.load_data()

    def clear_input(self):
        self.lineEdit_food.clear()
        self.spinBox_calories.setValue(0)
        self.lineEdit_note.clear()
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        self.comboBox_category.setCurrentIndex(0)
        self.tableWidget.clearSelection()
        self.stackedWidget.setCurrentWidget(self.pageInput)

    def fill_form_from_table(self):
        selected = self.tableWidget.currentRow()
        if selected < 0:
            return
        self.dateEdit.setDate(QtCore.QDate.fromString(self.tableWidget.item(selected, 0).text(), "yyyy-MM-dd"))
        self.lineEdit_food.setText(self.tableWidget.item(selected, 1).text())
        self.comboBox_category.setCurrentText(self.tableWidget.item(selected, 2).text())
        self.spinBox_calories.setValue(int(self.tableWidget.item(selected, 3).text()))
        self.lineEdit_note.setText(self.tableWidget.item(selected, 4).text())
        self.stackedWidget.setCurrentWidget(self.pageInput)

    def load_data(self):
        keyword = self.lineEdit_search.text()
        kategori = self.comboBox_filter.currentText()
        query = "SELECT * FROM diet_entries WHERE 1=1"
        params = []

        if kategori != "Semua":
            query += " AND kategori = ?"
            params.append(kategori)
        if keyword:
            query += " AND (makanan LIKE ? OR catatan LIKE ?)"
            params.extend([f"%{keyword}%"] * 2)

        query += " ORDER BY tanggal DESC, id DESC"
        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Tanggal", "Makanan/Minuman", "Kategori", "Kalori", "Catatan"])

        for row_idx, row in enumerate(rows):
            self.tableWidget.insertRow(row_idx)
            for col_idx, val in enumerate(row[1:]):
                item = QTableWidgetItem(str(val))
                item.setData(QtCore.Qt.UserRole, row[0])
                self.tableWidget.setItem(row_idx, col_idx, item)

        self.stackedWidget.setCurrentWidget(self.pageHistory)

    def export_csv(self):
        path, _ = QFileDialog.getSaveFileName(self, "Simpan File", "", "CSV Files (*.csv)")
        if path:
            with open(path, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Tanggal", "Makanan", "Kategori", "Kalori", "Catatan"])
                for row in range(self.tableWidget.rowCount()):
                    data = []
                    for col in range(self.tableWidget.columnCount()):
                        data.append(self.tableWidget.item(row, col).text())
                    writer.writerow(data)
            QMessageBox.information(self, "Berhasil", "Data berhasil diekspor ke CSV.")
            self.clear_input()

    def show_stats(self):
        self.stackedWidget.setCurrentWidget(self.pageStats)

        selected_date = self.calendarWidget.selectedDate().toString("yyyy-MM-dd")

        # Total kalori pada tanggal yang dipilih
        self.cursor.execute("SELECT SUM(kalori) FROM diet_entries WHERE tanggal = ?", (selected_date,))
        total_on_selected = self.cursor.fetchone()[0] or 0
        self.labelTotalKalori.setText(f"Total Kalori ({selected_date}): {total_on_selected} kkal")

        # Total seluruh entri
        self.cursor.execute("SELECT COUNT(*) FROM diet_entries")
        total_entries = self.cursor.fetchone()[0] or 0
        self.labelTotalEntri.setText(f"Total Entri: {total_entries}")

        # Ringkasan kalori per kategori (untuk tanggal yang dipilih)
        self.cursor.execute("SELECT kategori, SUM(kalori) FROM diet_entries WHERE tanggal = ? GROUP BY kategori", (selected_date,))
        data = self.cursor.fetchall()

        if not data:
            self.labelChart.setText("Tidak ada data statistik untuk tanggal ini.")
            return

        # Susun teks per kategori
        stat_text = "Total Kalori per Kategori:\n"
        for kategori, jumlah in data:
            stat_text += f"• {kategori}: {jumlah} kkal\n"

        self.labelChart.setText(stat_text)
        self.labelChart.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = DietTrackApp()
    window.show()
    sys.exit(app.exec_())
