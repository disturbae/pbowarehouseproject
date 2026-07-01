from abc import ABC, abstractmethod


class Barang(ABC):

    def __init__(self, kode, nama, stok):
        self.__kode = kode
        self.__nama = nama
        self.set_stok(stok)

    def get_kode(self):
        return self.__kode

    def get_nama(self):
        return self.__nama

    def get_stok(self):
        return self.__stok

    def set_nama(self, nama):
        self.__nama = nama

    def set_stok(self, stok):
        if stok < 0:
            raise ValueError("Stok tidak boleh negatif")
        self.__stok = stok

    @abstractmethod
    def kategori(self):
        pass

    def to_dict(self):
        return {
            "kode": self.__kode,
            "nama": self.__nama,
            "stok": self.__stok,
            "kategori": self.kategori()
        }

    @classmethod
    def from_dict(cls, data):
        from models.barang_elektronik import BarangElektronik
        from models.barang_makanan import BarangMakanan

        kategori = data.get("kategori")
        if kategori == "Elektronik":
            return BarangElektronik(
                data["kode"],
                data["nama"],
                data["stok"]
            )
        elif kategori == "Makanan":
            return BarangMakanan(
                data["kode"],
                data["nama"],
                data["stok"]
            )
        else:
            raise ValueError(f"Kategori tidak dikenal: {kategori}")

    @staticmethod
    def validasi_kode(kode):
        if not kode:
            return False
        return kode.isdigit()