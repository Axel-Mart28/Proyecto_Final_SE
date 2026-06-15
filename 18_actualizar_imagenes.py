import sqlite3
import os

assets_path = "assets"
conexion = sqlite3.connect("17_expertech_inventario.db")
cursor = conexion.cursor()

imagenes = [
    ("ryzen7_5700x",     "AMD Ryzen 7 5700X"),
    ("ryzen5_5600x",     "AMD Ryzen 5 5600X"),
    ("i7_13700k",        "Intel Core i7-13700K"),
    ("i5_13600k",        "Intel Core i5-13600K"),
    ("rtx4060",          "NVIDIA RTX 4060 8GB"),
    ("rtx4070",          "NVIDIA RTX 4070 12GB"),
    ("rx7600",           "AMD Radeon RX 7600 8GB"),
    ("rtx4090",          "NVIDIA RTX 4090 24GB"),
    ("ram_16gb_ddr4",    "Kingston 16GB DDR4 3200MHz (Para PC)"),
    ("ram_32gb_ddr4",    "Corsair 32GB DDR4 3200MHz (Para PC)"),
    ("ram_16gb_ddr5",    "Kingston 16GB DDR5 4800MHz (Para PC)"),
    ("ram_8gb_laptop",   "Kingston 8GB DDR4 3200MHz (Para Laptop)"),
    ("ram_mac",          "Crucial 16GB DDR4 3200MHz (Para Mac)"),
    ("ssd_970evo",       "Samsung 970 EVO 1TB NVMe SSD"),
    ("ssd_wd_blue",      "WD Blue 1TB SSD SATA (Para PC)"),
    ("hdd_seagate",      "Seagate 2TB HDD Interno (Para PC)"),
    ("ssd_laptop",       "WD 500GB SSD (Para Laptop)"),
    ("hdd_externo",      "Seagate 1TB Disco Externo USB"),
    ("asus_rog_b550",    "ASUS ROG Strix B550-F (AM4)"),
    ("msi_b660",         "MSI MAG B660 TOMAHAWK (LGA1700)"),
    ("gigabyte_b550m",   "Gigabyte B550M DS3H (AM4)"),
    ("evga_600w",        "EVGA 600W 80+ Bronze"),
    ("corsair_rm750x",   "Corsair RM750x 750W 80+ Gold"),
    ("seasonic_850w",    "Seasonic Focus GX-850 850W"),
    ("nzxt_h510",        "NZXT H510 ATX Mid Tower"),
    ("fractal_meshify",  "Fractal Design Meshify C"),
    ("masterbox_q300l",  "Cooler Master MasterBox Q300L"),
    ("hyper212",         "Cooler Master Hyper 212 Black"),
    ("nzxt_kraken",      "NZXT Kraken X63 280mm AIO"),
    ("bequiet_dark4",    "be quiet! Dark Rock Pro 4"),
    ("asus_rog_g15",     "ASUS ROG Strix G15 Ryzen 7"),
    ("lenovo_ideapad3",  "Lenovo IdeaPad 3 Core i5"),
    ("macbook_air_m2",   "MacBook Air M2 8GB 256GB"),
    ("hp_victus",        "HP Victus 15 RTX 3050"),
    ("g502_hero",        "Logitech G502 Hero Gaming"),
    ("razer_deathadder", "Razer DeathAdder V3"),
    ("mx_master3",       "Logitech MX Master 3"),
    ("redragon_k552",    "Redragon K552 Teclado Mecánico"),
    ("logitech_g915",    "Logitech G915 TKL Inalámbrico"),
    ("microsoft_sculpt", "Microsoft Sculpt Ergonomic"),
    ("redragon_s101",    "Redragon S101 Kit Gamer"),
    ("logitech_mk270",   "Logitech MK270 Kit Inalámbrico"),
    ("lg_27gp850",       "LG 27GP850-B 27\" 165Hz QHD"),
    ("samsung_24",       "Samsung 24\" FHD 75Hz IPS"),
    ("asus_rog_240hz",   "ASUS ROG Swift 27\" 240Hz"),
    ("hyperx_cloud2",    "HyperX Cloud II Gaming"),
    ("sony_wh1000xm5",   "Sony WH-1000XM5"),
    ("razer_blackshark", "Razer BlackShark V2 Pro"),
    ("steelseries_qck",  "SteelSeries QcK Large"),
    ("razer_goliathus",  "Razer Goliathus Extended Chroma"),
    ("tplink_ax21",      "TP-Link Archer AX21 Wi-Fi 6"),
    ("asus_rog_router",  "ASUS ROG Rapture GT-AX11000"),
    ("secretlab_titan",  "SecretLab Titan Evo 2022"),
    ("dxracer_formula",  "DXRacer Formula Series"),
    ("arozzi_arena",     "Arozzi Arena Gaming Desk"),
    ("flexispot_e7",     "Flexispot E7 Standing Desk"),
    ("xbox_controller",  "Xbox Controller Series X Inalámbrico"),
    ("dualsense_ps5",    "DualSense PS5 Blanco"),
    ("8bitdo_pro2",      "8BitDo Pro 2 Bluetooth"),
    ("tplink_pcie",      "TP-Link Archer TX3000E Wi-Fi 6 PCIe"),
    ("startech_usb",     "StarTech USB 3.0 PCIe 4 Puertos"),
    ("hp_aio",           "HP All-in-One 24 Core i5"),
    ("imac_m3",          "Apple iMac M3 8GB 256GB"),
    ("pc_gamer_ryzen5",  "PC Gamer Ryzen 5 + RTX 3060"),
    ("pc_oficina_i3",    "PC Oficina Intel i3 + SSD"),
]

actualizados = 0
no_encontrados = []

for nombre_base, nombre_producto in imagenes:
    ruta_encontrada = None

    # Buscar el archivo con cualquier extensión
    for ext in ["png", "jpg", "jpeg", "PNG", "JPG", "JPEG"]:
        ruta = os.path.join(assets_path, f"{nombre_base}.{ext}")
        if os.path.exists(ruta):
            ruta_encontrada = ruta.replace("\\", "/")
            break

    if ruta_encontrada:
        cursor.execute(
            "UPDATE productos SET imagen_url = ? WHERE nombre = ?",
            (ruta_encontrada, nombre_producto)
        )
        actualizados += 1
        print(f"✅ {nombre_producto} → {ruta_encontrada}")
    else:
        no_encontrados.append(nombre_producto)
        print(f"❌ No encontrada: {nombre_base} ({nombre_producto})")

conexion.commit()
conexion.close()

print(f"\n✅ {actualizados} productos actualizados.")
if no_encontrados:
    print(f"❌ {len(no_encontrados)} sin imagen:")
    for p in no_encontrados:
        print(f"   - {p}")