import tkinter as tk

from storage.json_storage import JsonStorage
from services.warehouse_manager import WarehouseManager
from gui.warehouse_app import WarehouseApp


def main():

    storage = JsonStorage(
        "data/warehouse.json"
    )

    manager = WarehouseManager(
        storage
    )

    root = tk.Tk()

    WarehouseApp(
        root,
        manager
    )

    root.mainloop()


if __name__ == "__main__":
    main()