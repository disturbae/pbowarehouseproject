import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from models.barang import Barang
from models.barang_elektronik import BarangElektronik
from models.barang_makanan import BarangMakanan


class WarehouseApp:

    def __init__(self, root, manager):

        self.root = root
        self.manager = manager

        self.root.title("Warehouse Management System")
        self.root.geometry("850x500")

        self.buat_form()
        self.buat_tabel()

        self.refresh_table()

    def buat_form(self):

        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        tk.Label(frame, text="Kode").grid(row=0, column=0)
        self.kode_entry = tk.Entry(frame)
        self.kode_entry.grid(row=0, column=1)

        tk.Label(frame, text="Nama").grid(row=1, column=0)
        self.nama_entry = tk.Entry(frame)
        self.nama_entry.grid(row=1, column=1)

        tk.Label(frame, text="Stok").grid(row=2, column=0)
        self.stok_entry = tk.Entry(frame)
        self.stok_entry.grid(row=2, column=1)

        tk.Label(frame, text="Kategori").grid(row=3, column=0)

        self.kategori = ttk.Combobox(
            frame,
            values=["Elektronik", "Makanan"]
        )

        self.kategori.grid(row=3, column=1)
        self.kategori.current(0)

        tk.Button(
            frame,
            text="Tambah",
            command=self.tambah_barang
        ).grid(row=4, column=0, pady=10)

        tk.Button(
            frame,
            text="Update",
            command=self.update_barang
        ).grid(row=4, column=1)

        tk.Button(
            frame,
            text="Hapus",
            command=self.hapus_barang
        ).grid(row=4, column=2)

        tk.Button(
            frame,
            text="Cari",
            command=self.cari_barang
        ).grid(row=4, column=3)

    def buat_tabel(self):

        kolom = (
            "Kode",
            "Nama",
            "Stok",
            "Kategori"
        )

        self.tree = ttk.Treeview(
            self.root,
            columns=kolom,
            show="headings"
        )

        for col in kolom:
            self.tree.heading(col, text=col)

        self.tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.pilih_data
        )

    def refresh_table(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        for barang in self.manager.tampilkan_semua():

            self.tree.insert(
                "",
                tk.END,
                values=(
                    barang.get_kode(),
                    barang.get_nama(),
                    barang.get_stok(),
                    barang.kategori()
                )
            )

    def tambah_barang(self):

        try:

            kode = self.kode_entry.get().strip()
            nama = self.nama_entry.get().strip()
            stok_text = self.stok_entry.get().strip()
            kategori = self.kategori.get().strip()

            if kode == "":
                raise ValueError("Kode barang tidak boleh kosong")

            if nama == "":
                raise ValueError("Nama barang tidak boleh kosong")

            if stok_text == "":
                raise ValueError("Stok tidak boleh kosong")

            if not Barang.validasi_kode(kode):
                raise ValueError("Kode barang harus berupa angka")

            if not stok_text.isdigit():
                raise ValueError("Stok harus berupa angka")

            stok = int(stok_text)

            if kategori == "Elektronik":
                barang = BarangElektronik(
                    kode,
                    nama,
                    stok
                )
            else:
                barang = BarangMakanan(
                    kode,
                    nama,
                    stok
                )

            self.manager.tambah_barang(barang)

            self.refresh_table()
            self.clear_form()

            messagebox.showinfo(
                "Sukses",
                "Data berhasil ditambahkan"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def update_barang(self):

        try:

            kode = self.kode_entry.get().strip()
            nama = self.nama_entry.get().strip()
            stok_text = self.stok_entry.get().strip()

            if kode == "":
                raise ValueError("Kode barang tidak boleh kosong")

            if nama == "":
                raise ValueError("Nama barang tidak boleh kosong")

            if stok_text == "":
                raise ValueError("Stok tidak boleh kosong")

            if not Barang.validasi_kode(kode):
                raise ValueError("Kode barang harus berupa angka")

            if not stok_text.isdigit():
                raise ValueError("Stok harus berupa angka")

            stok = int(stok_text)

            barang = self.manager.cari_barang(kode)

            if barang is None:
                raise ValueError("Kode barang tidak ditemukan")

            self.manager.update_barang(
                kode,
                nama,
                stok
            )

            self.refresh_table()
            self.clear_form()

            messagebox.showinfo(
                "Sukses",
                "Data berhasil diupdate"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def hapus_barang(self):

        try:

            kode = self.kode_entry.get().strip()

            if kode == "":
                raise ValueError("Masukkan kode barang terlebih dahulu")

            barang = self.manager.cari_barang(kode)

            if barang is None:
                raise ValueError("Kode barang tidak ditemukan")

            self.manager.hapus_barang(kode)

            self.refresh_table()
            self.clear_form()

            messagebox.showinfo(
                "Sukses",
                "Data berhasil dihapus"
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    def cari_barang(self):

        kode = self.kode_entry.get().strip()

        barang = self.manager.cari_barang(kode)

        if barang:

            self.nama_entry.delete(0, tk.END)
            self.nama_entry.insert(
                0,
                barang.get_nama()
            )

            self.stok_entry.delete(0, tk.END)
            self.stok_entry.insert(
                0,
                barang.get_stok()
            )

            self.kategori.set(
                barang.kategori()
            )

        else:

            messagebox.showwarning(
                "Info",
                "Data tidak ditemukan"
            )

    def pilih_data(self, event):

        selected = self.tree.focus()

        if not selected:
            return

        data = self.tree.item(selected)["values"]

        self.clear_form()

        self.kode_entry.insert(0, data[0])
        self.nama_entry.insert(0, data[1])
        self.stok_entry.insert(0, data[2])
        self.kategori.set(data[3])

    def clear_form(self):

        self.kode_entry.delete(0, tk.END)
        self.nama_entry.delete(0, tk.END)
        self.stok_entry.delete(0, tk.END)
