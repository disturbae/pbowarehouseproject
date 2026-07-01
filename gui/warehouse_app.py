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
        self.root.geometry("950x600")
        self.root.configure(bg="#F3F4F6")

        # Configure Custom Styles
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Global font settings
        self.style.configure(".", font=("Segoe UI", 10), background="#F3F4F6", foreground="#1F2937")

        # Treeview styling
        self.style.configure(
            "Treeview",
            rowheight=28,
            font=("Segoe UI", 10),
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            foreground="#1F2937",
            borderwidth=0
        )
        self.style.map(
            "Treeview",
            background=[("selected", "#EEF2FF")],
            foreground=[("selected", "#4F46E5")]
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#E5E7EB",
            foreground="#374151",
            relief="flat",
            padding=5
        )

        # Combobox styling
        self.style.configure(
            "TCombobox",
            arrowcolor="#4F46E5",
            background="#FFFFFF",
            fieldbackground="#FFFFFF",
            darkcolor="#FFFFFF",
            lightcolor="#FFFFFF"
        )

        # Build UI layout
        self.buat_header()
        
        # Main Container
        self.main_container = tk.Frame(self.root, bg="#F3F4F6")
        self.main_container.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        # Split into Left Pane (Form) and Right Pane (Table)
        self.left_pane = tk.Frame(self.main_container, bg="#F3F4F6")
        self.left_pane.pack(side="left", fill="both", padx=(0, 10))

        self.right_pane = tk.Frame(self.main_container, bg="#F3F4F6")
        self.right_pane.pack(side="right", fill="both", expand=True, padx=(10, 0))

        self.buat_form()
        self.buat_tabel()

        self.refresh_table()

    def buat_header(self):
        header_frame = tk.Frame(self.root, bg="#4F46E5", height=60)
        header_frame.pack(fill="x", side="top")
        
        # Label Title
        title_label = tk.Label(
            header_frame,
            text=" 📦  Warehouse Inventory System",
            font=("Segoe UI", 16, "bold"),
            fg="#FFFFFF",
            bg="#4F46E5",
            pady=15
        )
        title_label.pack(side="left", padx=20)

    def buat_form(self):
        # Card container
        form_card = tk.Frame(self.left_pane, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E5E7EB", highlightthickness=1)
        form_card.pack(fill="both", expand=True, ipady=15)

        # Section Title
        tk.Label(
            form_card,
            text="Detail Barang",
            font=("Segoe UI", 12, "bold"),
            fg="#1F2937",
            bg="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(20, 15))

        # Helper to create styled labels and entries
        def create_field(parent, label_text):
            frame = tk.Frame(parent, bg="#FFFFFF")
            frame.pack(fill="x", padx=20, pady=6)

            lbl = tk.Label(
                frame,
                text=label_text,
                font=("Segoe UI", 9, "bold"),
                fg="#4B5563",
                bg="#FFFFFF"
            )
            lbl.pack(anchor="w", pady=(0, 4))

            entry = tk.Entry(
                frame,
                font=("Segoe UI", 10),
                bg="#F9FAFB",
                fg="#1F2937",
                relief="flat",
                highlightthickness=1,
                highlightbackground="#D1D5DB",
                highlightcolor="#4F46E5",
                insertbackground="#1F2937"
            )
            entry.pack(fill="x", ipady=6)
            return entry

        self.kode_entry = create_field(form_card, "Kode Barang")
        self.nama_entry = create_field(form_card, "Nama Barang")
        self.stok_entry = create_field(form_card, "Stok Barang")

        # Category field (Combobox)
        cat_frame = tk.Frame(form_card, bg="#FFFFFF")
        cat_frame.pack(fill="x", padx=20, pady=6)

        tk.Label(
            cat_frame,
            text="Kategori",
            font=("Segoe UI", 9, "bold"),
            fg="#4B5563",
            bg="#FFFFFF"
        ).pack(anchor="w", pady=(0, 4))

        self.kategori = ttk.Combobox(
            cat_frame,
            values=["Elektronik", "Makanan"],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.kategori.pack(fill="x", ipady=4)
        self.kategori.current(0)

        # Action Buttons frame
        btn_frame = tk.Frame(form_card, bg="#FFFFFF")
        btn_frame.pack(fill="x", padx=20, pady=(25, 10))

        # Modern Button Helper with hover effects
        def create_button(parent, text, color, hover_color, command, row, col, columnspan=1):
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                font=("Segoe UI", 9, "bold"),
                fg="#FFFFFF",
                bg=color,
                activebackground=hover_color,
                activeforeground="#FFFFFF",
                relief="flat",
                bd=0,
                cursor="hand2"
            )
            btn.grid(row=row, column=col, columnspan=columnspan, sticky="nsew", padx=4, pady=5, ipady=8)
            
            # Hover bindings
            btn.bind("<Enter>", lambda e: btn.configure(bg=hover_color))
            btn.bind("<Leave>", lambda e: btn.configure(bg=color))
            return btn

        # 2x2 Grid for buttons
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        create_button(btn_frame, "Tambah", "#10B981", "#059669", self.tambah_barang, row=0, col=0)
        create_button(btn_frame, "Update", "#F59E0B", "#D97706", self.update_barang, row=0, col=1)
        create_button(btn_frame, "Cari", "#3B82F6", "#2563EB", self.cari_barang, row=1, col=0)
        create_button(btn_frame, "Hapus", "#EF4444", "#DC2626", self.hapus_barang, row=1, col=1)

    def buat_tabel(self):
        # Card container for table
        table_card = tk.Frame(self.right_pane, bg="#FFFFFF", bd=1, relief="flat", highlightbackground="#E5E7EB", highlightthickness=1)
        table_card.pack(fill="both", expand=True)

        # Table Header/Title
        tk.Label(
            table_card,
            text="Daftar Inventaris",
            font=("Segoe UI", 12, "bold"),
            fg="#1F2937",
            bg="#FFFFFF"
        ).pack(anchor="w", padx=20, pady=(20, 15))

        kolom = (
            "Kode",
            "Nama",
            "Stok",
            "Kategori"
        )

        # Outer Frame for Treeview & Scrollbar
        tree_frame = tk.Frame(table_card, bg="#FFFFFF")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Create Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=kolom,
            show="headings"
        )

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Style layout for scrollbar and tree
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Headings and columns alignment/widths
        for col in kolom:
            self.tree.heading(col, text=col, anchor="w")
            if col == "Kode":
                self.tree.column(col, width=100, minwidth=80, anchor="w")
            elif col == "Nama":
                self.tree.column(col, width=250, minwidth=180, anchor="w")
            elif col == "Stok":
                self.tree.column(col, width=100, minwidth=80, anchor="w")
            elif col == "Kategori":
                self.tree.column(col, width=150, minwidth=120, anchor="w")

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
