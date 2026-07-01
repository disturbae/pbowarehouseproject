from models.barang import Barang


class WarehouseManager:

    def __init__(self, storage):
        self.storage = storage
        self.barang_list = []
        self.load_data()

    def load_data(self):

        data = self.storage.load()

        for item in data:
            barang = Barang.from_dict(item)
            self.barang_list.append(barang)

    def save_data(self):

        data = [barang.to_dict() for barang in self.barang_list]
        self.storage.save(data)

    def tambah_barang(self, barang):

        if self.cari_barang(barang.get_kode()):
            raise ValueError("Kode barang sudah ada")

        self.barang_list.append(barang)
        self.save_data()

    def tampilkan_semua(self):
        return self.barang_list

    def cari_barang(self, kode):

        for barang in self.barang_list:
            if barang.get_kode() == kode:
                return barang

        return None

    def update_barang(self, kode, nama, stok):

        barang = self.cari_barang(kode)

        if barang:
            barang.set_nama(nama)
            barang.set_stok(stok)
            self.save_data()

    def hapus_barang(self, kode):

        barang = self.cari_barang(kode)

        if barang:
            self.barang_list.remove(barang)
            self.save_data()