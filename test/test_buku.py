from unittest.mock import MagicMock
from models.buku_model import BukuModel

def test_create_buku_berhasil():
    # Menginisialisasi Model
    model = BukuModel()
    
    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    
    # Melakukan eksekusi fungsi
    hasil = model.create_buku("Buku Testing", "Penulis QA", 2026)
    
    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True
    # Memverifikasi apakah cursor.execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()
    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_get_all_buku():
    # Menginisialisasi Model
    model = BukuModel()
 
    # Mock koneksi dan cursor
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
 
    # Data palsu yang seolah-olah dikembalikan oleh database
    data_palsu = [
        {'id_buku': 1, 'judul': 'Pemrograman Python', 'penulis': 'Budi', 'tahun_terbit': 2023},
        {'id_buku': 2, 'judul': 'Basis Data', 'penulis': 'Siti', 'tahun_terbit': 2024},
    ]
    mock_cursor.fetchall.return_value = data_palsu
 
    # Eksekusi fungsi
    hasil = model.get_all_buku()
 
    # Verifikasi: query dijalankan satu kali
    mock_cursor.execute.assert_called_once()
    # Verifikasi: hasil sama dengan data dari database
    assert hasil == data_palsu
    assert len(hasil) == 2
    assert hasil[0]['judul'] == 'Pemrograman Python'