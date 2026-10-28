import tkinter.messagebox as messagebox
from models.buku_model import BukuModel
from views.buku_view import BukuView

class BukuController:
    def __init__(self, user_role="anggota"):
        self.user_role = user_role
        self.model = BukuModel()
        self.view = BukuView()
        self.selected_id = None  # Ditambahkan untuk menyimpan ID buku yang dipilih

        # Menampilkan informasi role pada judul jendela aplikasi
        self.view.title(f"Sistem Manajemen Perpustakaan - Mode: {self.user_role.upper()}")

        # Binding tombol ke fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_update.configure(command=self.perbarui_data)  # Ditambahkan
        self.view.btn_delete.configure(command=self.hapus_data)        # Ditambahkan
        self.view.btn_logout.configure(command=self.logout)          # TUGAS 3: Ditambahkan

        # Binding event klik baris tabel
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_data)   # Ditambahkan

        # OTORISASI: Jika bukan admin, nonaktifkan form input dan SELURUH tombol aksi (TUGAS 2)
        if self.user_role != "admin":
            self.view.btn_simpan.configure(state="disabled", text="Akses Terkunci (Khusus Admin)")
            self.view.btn_update.configure(state="disabled")        # TUGAS 2: Nonaktifkan Perbarui
            self.view.btn_delete.configure(state="disabled")           # TUGAS 2: Nonaktifkan Hapus
            self.view.entry_judul.configure(state="disabled")
            self.view.entry_penulis.configure(state="disabled")
            self.view.entry_tahun.configure(state="disabled")
    
        self.muat_data_tabel()

    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
        data_buku = self.model.get_all_buku()
        for buku in data_buku:
            self.view.tabel.insert("", "end", values=(buku['id_buku'], buku['judul'], buku['penulis'], buku['tahun_terbit']))

    # Ditambahkan: Fungsi untuk mengambil data saat baris tabel diklik
    def pilih_data(self, event):
        selected_item = self.view.tabel.selection()
        if selected_item:
            item_data = self.view.tabel.item(selected_item[0])['values']
            self.selected_id = item_data[0]

            if self.user_role == "admin":
                self.view.entry_judul.delete(0, 'end')
                self.view.entry_judul.insert(0, item_data[1])
                self.view.entry_penulis.delete(0, 'end')
                self.view.entry_penulis.insert(0, item_data[2])
                self.view.entry_tahun.delete(0, 'end')
                self.view.entry_tahun.insert(0, item_data[3])

    # Ditambahkan: Fungsi untuk membersihkan form input
    def bersihkan_form(self):
        if self.user_role == "admin":
            self.view.entry_judul.delete(0, 'end')
            self.view.entry_penulis.delete(0, 'end')
            self.view.entry_tahun.delete(0, 'end')
        self.selected_id = None

    def simpan_data(self):
        # Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menambah data!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        if self.model.create_buku(judul, penulis, tahun):
            messagebox.showinfo("Sukses", "Data buku berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Gagal menyimpan data.")

    def hapus_data(self):
        # TUGAS 2: Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk menghapus data!")
            return

        # Pastikan ada baris yang dipilih
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin dihapus!")
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi", f"Yakin ingin menghapus buku dengan ID {self.selected_id}?"
        )
        if not konfirmasi:
            return

        berhasil = self.model.delete_buku(self.selected_id)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")

    def perbarui_data(self):
        # TUGAS 2: Proteksi ganda di level controller
        if self.user_role != "admin":
            messagebox.showerror("Akses Ditolak", "Anda tidak memiliki izin untuk memperbarui data!")
            return

        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin diperbarui!")
            return

        judul = self.view.entry_judul.get()
        penulis = self.view.entry_penulis.get()
        tahun = self.view.entry_tahun.get()

        if not judul or not penulis or not tahun:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return

        berhasil = self.model.update_buku(self.selected_id, judul, penulis, tahun)

        if berhasil:
            messagebox.showinfo("Sukses", "Data buku berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")

    # TUGAS 3: Fungsi Logout ditambahkan
    def logout(self):
        from controller.auth_controller import AuthController
        self.view.destroy()
        auth_app = AuthController()
        auth_app.run()

    def run(self):
        self.view.mainloop()