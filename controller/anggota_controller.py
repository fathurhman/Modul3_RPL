import tkinter.messagebox as messagebox
from models.anggota_model import AnggotaModel
from views.anggota_view import AnggotaView
 
 
class AnggotaController:
    def __init__(self):
        # Inisialisasi Model dan View
        self.model = AnggotaModel()
        self.view = AnggotaView()
 
        # Menyimpan id_anggota dari baris tabel yang sedang dipilih
        self.selected_id = None
 
        # Binding tombol di View dengan fungsi di Controller
        self.view.btn_simpan.configure(command=self.simpan_data)
        self.view.btn_hapus.configure(command=self.hapus_data)
        self.view.btn_perbarui.configure(command=self.perbarui_data)
 
        # Event: klik baris tabel -> isi form
        self.view.tabel.bind("<<TreeviewSelect>>", self.pilih_baris)
 
        # Muat data awal
        self.muat_data_tabel()
 
    # ------------------------------------------------------------------
    # Helper
    # ------------------------------------------------------------------
    def muat_data_tabel(self):
        for item in self.view.tabel.get_children():
            self.view.tabel.delete(item)
 
        data_anggota = self.model.get_all_anggota()
        for a in data_anggota:
            self.view.tabel.insert(
                "", "end",
                values=(a['id_anggota'], a['nama'], a['email'], a['telepon'])
            )
 
    def bersihkan_form(self):
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_email.delete(0, 'end')
        self.view.entry_telepon.delete(0, 'end')
        self.selected_id = None
 
    def pilih_baris(self, event=None):
        selection = self.view.tabel.selection()
        if not selection:
            return
 
        values = self.view.tabel.item(selection[0])['values']
        self.selected_id = values[0]  # kolom pertama = id_anggota
 
        self.view.entry_nama.delete(0, 'end')
        self.view.entry_nama.insert(0, values[1])
        self.view.entry_email.delete(0, 'end')
        self.view.entry_email.insert(0, values[2])
        self.view.entry_telepon.delete(0, 'end')
        self.view.entry_telepon.insert(0, values[3])
 
    # ------------------------------------------------------------------
    # Aksi tombol
    # ------------------------------------------------------------------
    def simpan_data(self):
        nama = self.view.entry_nama.get()
        email = self.view.entry_email.get()
        telepon = self.view.entry_telepon.get()
 
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
 
        berhasil = self.model.create_anggota(nama, email, telepon)
 
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil disimpan!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menyimpan data.")
 
    def hapus_data(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin dihapus!")
            return
 
        konfirmasi = messagebox.askyesno(
            "Konfirmasi", f"Yakin ingin menghapus anggota dengan ID {self.selected_id}?"
        )
        if not konfirmasi:
            return
 
        berhasil = self.model.delete_anggota(self.selected_id)
 
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil dihapus!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat menghapus data.")
 
    def perbarui_data(self):
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih data di tabel yang ingin diperbarui!")
            return
 
        nama = self.view.entry_nama.get()
        email = self.view.entry_email.get()
        telepon = self.view.entry_telepon.get()
 
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom form harus diisi!")
            return
 
        berhasil = self.model.update_anggota(self.selected_id, nama, email, telepon)
 
        if berhasil:
            messagebox.showinfo("Sukses", "Data anggota berhasil diperbarui!")
            self.bersihkan_form()
            self.muat_data_tabel()
        else:
            messagebox.showerror("Error", "Terjadi kesalahan saat memperbarui data.")
 
    def run(self):
        self.view.mainloop()
 