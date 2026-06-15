import sqlite3

def inicializar_bd():
    conexion = sqlite3.connect('17_expertech_inventario.db')
    cursor = conexion.cursor()

    # Tabla productos con subcategoria
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            categoria TEXT NOT NULL,
            subcategoria TEXT DEFAULT 'Normal',
            precio REAL NOT NULL,
            stock INTEGER NOT NULL,
            detalles TEXT,
            imagen_url TEXT
        )
    ''')

    # Tabla historial de compras
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historial_compras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            articulos_comprados TEXT NOT NULL,
            total REAL NOT NULL,
            justificacion_ia TEXT
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM productos")
    if cursor.fetchone()[0] == 0:
        productos_demo = [

            # ─────────────────────────────────────────
            # CATEGORÍA: Procesadores
            # ─────────────────────────────────────────
            ("AMD Ryzen 7 5700X", "Procesadores", "Normal", 3200.0, 10,
             "8 núcleos, 16 hilos, 3.4GHz base, 4.6GHz boost. Socket AM4. Ideal para productividad y virtualización.", "assets/amd_ryzen_7_5700x.jpg"),
            ("AMD Ryzen 5 5600X", "Procesadores", "Normal", 2400.0, 12,
             "6 núcleos, 12 hilos, 3.7GHz base, 4.6GHz boost. Socket AM4. Excelente relación precio-rendimiento.", ""),
            ("Intel Core i7-13700K", "Procesadores", "Normal", 5800.0, 6,
             "16 núcleos (8P+8E), 24 hilos, 3.4GHz base, 5.4GHz boost. Socket LGA1700.", ""),
            ("Intel Core i5-13600K", "Procesadores", "Normal", 4200.0, 8,
             "14 núcleos (6P+8E), 20 hilos, 3.5GHz base, 5.1GHz boost. Socket LGA1700.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Tarjetas de Video
            # ─────────────────────────────────────────
            ("NVIDIA RTX 4060 8GB", "Tarjetas de Video", "Gamer", 6500.0, 5,
             "8GB GDDR6, 128-bit, DLSS 3, ray tracing. Ideal para gaming 1080p/1440p.", ""),
            ("NVIDIA RTX 4070 12GB", "Tarjetas de Video", "Gamer", 11000.0, 4,
             "12GB GDDR6X, 192-bit, DLSS 3, ray tracing. Gaming 1440p/4K fluido.", ""),
            ("AMD Radeon RX 7600 8GB", "Tarjetas de Video", "Gamer", 5500.0, 7,
             "8GB GDDR6, 128-bit, FSR 3. Excelente opción para gaming 1080p.", ""),
            ("NVIDIA RTX 4090 24GB", "Tarjetas de Video", "Gamer", 35000.0, 2,
             "24GB GDDR6X, 384-bit. La GPU más potente para gaming y creación de contenido 4K.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Memorias RAM
            # ─────────────────────────────────────────
            ("Kingston 16GB DDR4 3200MHz (Para PC)", "Memorias RAM", "Normal", 750.0, 20,
             "16GB DDR4 3200MHz CL16. Compatible con plataformas AMD e Intel.", ""),
            ("Corsair 32GB DDR4 3200MHz (Para PC)", "Memorias RAM", "Normal", 1600.0, 15,
             "Kit 2x16GB DDR4 3200MHz CL16. Ideal para multitarea y virtualización.", ""),
            ("Kingston 16GB DDR5 4800MHz (Para PC)", "Memorias RAM", "Normal", 1400.0, 10,
             "16GB DDR5 4800MHz. Compatible con plataformas Intel 12th/13th gen y AMD AM5.", ""),
            ("Kingston 8GB DDR4 3200MHz (Para Laptop)", "Memorias RAM", "Normal", 450.0, 18,
             "8GB DDR4 3200MHz SO-DIMM. Compatible con la mayoría de laptops.", ""),
            ("Crucial 16GB DDR4 3200MHz (Para Mac)", "Memorias RAM", "Normal", 900.0, 8,
             "16GB DDR4 3200MHz SO-DIMM. Compatible con iMac y MacBook Pro.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Discos Duros
            # ─────────────────────────────────────────
            ("Samsung 970 EVO 1TB NVMe SSD", "Discos Duros", "Normal", 1400.0, 12,
             "1TB NVMe PCIe 3.0, lectura 3500MB/s, escritura 3300MB/s. Para PC.", ""),
            ("WD Blue 1TB SSD SATA (Para PC)", "Discos Duros", "Normal", 900.0, 15,
             "1TB SSD SATA III, lectura 560MB/s. Upgrade ideal para PC de escritorio.", ""),
            ("Seagate 2TB HDD Interno (Para PC)", "Discos Duros", "Normal", 700.0, 20,
             "2TB HDD 7200RPM SATA III. Almacenamiento masivo para PC.", ""),
            ("WD 500GB SSD (Para Laptop)", "Discos Duros", "Normal", 650.0, 14,
             "500GB SSD M.2 SATA. Upgrade de almacenamiento para laptops.", ""),
            ("Seagate 1TB Disco Externo USB", "Discos Duros", "Normal", 800.0, 10,
             "1TB HDD externo USB 3.0. Portátil y compatible con PC, Mac y consolas.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Tarjetas Madre
            # ─────────────────────────────────────────
            ("ASUS ROG Strix B550-F (AM4)", "Tarjetas Madre", "Gamer", 3500.0, 6,
             "Socket AM4, DDR4, PCIe 4.0, Wi-Fi 6, 2.5G LAN. Compatible Ryzen 5000.", ""),
            ("MSI MAG B660 TOMAHAWK (LGA1700)", "Tarjetas Madre", "Normal", 3200.0, 8,
             "Socket LGA1700, DDR4, PCIe 4.0, 2.5G LAN. Compatible Intel 12th/13th gen.", ""),
            ("Gigabyte B550M DS3H (AM4)", "Tarjetas Madre", "Normal", 1800.0, 10,
             "Socket AM4, DDR4, Micro-ATX. Opción económica para builds AMD.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Fuentes de Poder
            # ─────────────────────────────────────────
            ("EVGA 600W 80+ Bronze", "Fuentes de Poder", "Normal", 1100.0, 12,
             "600W, 80+ Bronze, semi-modular. Suficiente para builds de gama media.", ""),
            ("Corsair RM750x 750W 80+ Gold", "Fuentes de Poder", "Gamer", 2200.0, 8,
             "750W, 80+ Gold, totalmente modular. Ideal para GPUs de alta gama.", ""),
            ("Seasonic Focus GX-850 850W", "Fuentes de Poder", "Gamer", 2800.0, 5,
             "850W, 80+ Gold, totalmente modular. Para sistemas de alto rendimiento.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Gabinetes
            # ─────────────────────────────────────────
            ("NZXT H510 ATX Mid Tower", "Gabinetes", "Gamer", 1800.0, 7,
             "ATX Mid Tower, panel lateral de vidrio templado, 2 ventiladores incluidos.", ""),
            ("Fractal Design Meshify C", "Gabinetes", "Normal", 2100.0, 5,
             "ATX Mid Tower, malla frontal de alto flujo de aire, excelente para enfriamiento.", ""),
            ("Cooler Master MasterBox Q300L", "Gabinetes", "Normal", 900.0, 10,
             "Micro-ATX, panel magnético, diseño compacto y versátil.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Enfriamiento y Ventilación
            # ─────────────────────────────────────────
            ("Cooler Master Hyper 212 Black", "Enfriamiento y Ventilación", "Normal", 650.0, 15,
             "Cooler de aire, compatible AM4/AM5/LGA1700, TDP 150W.", ""),
            ("NZXT Kraken X63 280mm AIO", "Enfriamiento y Ventilación", "Gamer", 3200.0, 6,
             "Enfriamiento líquido AIO 280mm, pantalla LCD, compatible AM4/AM5/LGA1700.", ""),
            ("be quiet! Dark Rock Pro 4", "Enfriamiento y Ventilación", "Normal", 1800.0, 5,
             "Cooler de aire de doble torre, ultra silencioso, TDP 250W.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Laptops
            # ─────────────────────────────────────────
            ("ASUS ROG Strix G15 Ryzen 7", "Laptops", "Gamer", 22000.0, 4,
             "Ryzen 7 6800H, RTX 3060 6GB, 16GB RAM, 512GB SSD, pantalla 144Hz.", ""),
            ("Lenovo IdeaPad 3 Core i5", "Laptops", "Normal", 12000.0, 8,
             "Intel Core i5-1235U, 8GB RAM, 512GB SSD, pantalla 15.6 FHD. Windows 11.", ""),
            ("MacBook Air M2 8GB 256GB", "Laptops", "Normal", 28000.0, 3,
             "Apple M2, 8GB RAM unificada, 256GB SSD, pantalla Liquid Retina 13.6.", ""),
            ("HP Victus 15 RTX 3050", "Laptops", "Gamer", 16500.0, 6,
             "Intel Core i5-12450H, RTX 3050 4GB, 8GB RAM, 512GB SSD, 144Hz.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Mouse
            # ─────────────────────────────────────────
            ("Logitech G502 Hero Gaming", "Mouse", "Gamer", 1200.0, 15,
             "25600 DPI, 11 botones programables, peso ajustable, RGB.", ""),
            ("Razer DeathAdder V3", "Mouse", "Gamer", 1800.0, 10,
             "30000 DPI, sensor Focus Pro, 90 horas de batería, ultra ligero.", ""),
            ("Logitech MX Master 3", "Mouse", "Normal", 1500.0, 12,
             "4000 DPI, rueda electromagnética, Bluetooth/USB, para productividad.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Teclados
            # ─────────────────────────────────────────
            ("Redragon K552 Teclado Mecánico", "Teclados", "Gamer", 750.0, 20,
             "Switches azules, TKL 87 teclas, retroiluminación RGB, anti-ghosting.", ""),
            ("Logitech G915 TKL Inalámbrico", "Teclados", "Gamer", 4500.0, 5,
             "Switches GL Linear, inalámbrico, RGB, ultra delgado, 40 horas batería.", ""),
            ("Microsoft Sculpt Ergonomic", "Teclados", "Normal", 1800.0, 8,
             "Diseño ergonómico dividido, inalámbrico, ideal para largas jornadas.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Kits de Teclado y Mouse
            # ─────────────────────────────────────────
            ("Redragon S101 Kit Gamer", "Kits de Teclado y Mouse", "Gamer", 850.0, 15,
             "Teclado retroiluminado rojo + mouse 3200 DPI RGB. Combo para gaming.", ""),
            ("Logitech MK270 Kit Inalámbrico", "Kits de Teclado y Mouse", "Normal", 600.0, 20,
             "Teclado + mouse inalámbrico, receptor nano USB, hasta 24 meses de batería.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Monitores
            # ─────────────────────────────────────────
            ("LG 27GP850-B 27\" 165Hz QHD", "Monitores", "Gamer", 7500.0, 5,
             "27 pulgadas, 2560x1440 QHD, 165Hz, 1ms, IPS, G-Sync compatible.", ""),
            ("Samsung 24\" FHD 75Hz IPS", "Monitores", "Normal", 3200.0, 10,
             "24 pulgadas, 1920x1080 FHD, 75Hz, panel IPS, HDMI+VGA.", ""),
            ("ASUS ROG Swift 27\" 240Hz", "Monitores", "Gamer", 12000.0, 3,
             "27 pulgadas, 1920x1080, 240Hz, 1ms, G-Sync, ideal para esports.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Audífonos
            # ─────────────────────────────────────────
            ("HyperX Cloud II Gaming", "Audífonos", "Gamer", 1400.0, 12,
             "Sonido 7.1 virtual, micrófono desmontable, compatible PC/PS/Xbox.", ""),
            ("Sony WH-1000XM5", "Audífonos", "Normal", 7500.0, 4,
             "Cancelación de ruido líder, 30 horas batería, Bluetooth 5.2.", ""),
            ("Razer BlackShark V2 Pro", "Audífonos", "Gamer", 4200.0, 6,
             "Inalámbrico, THX Spatial Audio, 70 horas batería, micrófono cardioide.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Mousepads
            # ─────────────────────────────────────────
            ("SteelSeries QcK Large", "Mousepads", "Gamer", 450.0, 25,
             "45x40cm, superficie micro-texturizada, base antideslizante.", ""),
            ("Razer Goliathus Extended Chroma", "Mousepads", "Gamer", 1200.0, 10,
             "920x294mm, RGB perimetral, superficie optimizada para todos los DPI.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Routers
            # ─────────────────────────────────────────
            ("TP-Link Archer AX21 Wi-Fi 6", "Routers", "Normal", 1500.0, 10,
             "Wi-Fi 6, AX1800, dual band, 4 antenas, ideal para hogar.", ""),
            ("ASUS ROG Rapture GT-AX11000", "Routers", "Gamer", 8500.0, 3,
             "Wi-Fi 6, AX11000, tri-band, VPN, optimización para gaming.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Sillas Gamer
            # ─────────────────────────────────────────
            ("SecretLab Titan Evo 2022", "Sillas Gamer", "Gamer", 12000.0, 4,
             "Espuma fría de alta densidad, reposabrazos 4D, reclinable hasta 165°.", ""),
            ("DXRacer Formula Series", "Sillas Gamer", "Gamer", 6500.0, 7,
             "Estructura de acero, cojines lumbar y cervical, reclinable 135°.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Escritorios Gamer
            # ─────────────────────────────────────────
            ("Arozzi Arena Gaming Desk", "Escritorios Gamer", "Gamer", 8000.0, 3,
             "160x80cm, superficie completa de mousepad, diseño en forma de curva.", ""),
            ("Flexispot E7 Standing Desk", "Escritorios Gamer", "Normal", 9500.0, 3,
             "Escritorio de pie eléctrico, altura ajustable 60-125cm, 125kg capacidad.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Controles de Juego
            # ─────────────────────────────────────────
            ("Xbox Controller Series X Inalámbrico", "Controles de Juego", "Gamer", 1200.0, 15,
             "Compatible PC/Xbox, Bluetooth, entrada 3.5mm, 40 horas batería.", ""),
            ("DualSense PS5 Blanco", "Controles de Juego", "Gamer", 1500.0, 10,
             "Compatible PC/PS5, vibración háptica, gatillos adaptativos, Bluetooth.", ""),
            ("8BitDo Pro 2 Bluetooth", "Controles de Juego", "Normal", 1100.0, 8,
             "Compatible PC/Android/iOS/Switch, Bluetooth+USB, 20 horas batería.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: Tarjetas de Expansión
            # ─────────────────────────────────────────
            ("TP-Link Archer TX3000E Wi-Fi 6 PCIe", "Tarjetas de Expansión", "Normal", 900.0, 10,
             "Wi-Fi 6 AX3000, Bluetooth 5.0, PCIe para desktop.", ""),
            ("StarTech USB 3.0 PCIe 4 Puertos", "Tarjetas de Expansión", "Normal", 550.0, 12,
             "4 puertos USB 3.0, PCIe x1, compatible Windows/Linux.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: PC All in One
            # ─────────────────────────────────────────
            ("HP All-in-One 24 Core i5", "PC All in One", "Normal", 18000.0, 4,
             "Intel Core i5-1235U, 8GB RAM, 512GB SSD, pantalla 23.8 FHD touch.", ""),
            ("Apple iMac M3 8GB 256GB", "PC All in One", "Normal", 42000.0, 2,
             "Apple M3, 8GB RAM, 256GB SSD, pantalla Retina 4.5K 24 pulgadas.", ""),

            # ─────────────────────────────────────────
            # CATEGORÍA: PC ya armadas
            # ─────────────────────────────────────────
            ("PC Gamer Ryzen 5 + RTX 3060", "PC ya armadas", "Gamer", 18500.0, 3,
             "Ryzen 5 5600X, RTX 3060 12GB, 16GB DDR4, 1TB SSD, gabinete RGB.", ""),
            ("PC Oficina Intel i3 + SSD", "PC ya armadas", "Normal", 8500.0, 5,
             "Intel Core i3-12100, 8GB DDR4, 256GB SSD, Windows 11 Home.", ""),
        ]

        cursor.executemany('''
            INSERT INTO productos (nombre, categoria, subcategoria, precio, stock, detalles, imagen_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', productos_demo)
        print("✅ Catálogo completo inyectado en la base de datos.")

    conexion.commit()
    conexion.close()
    print("✅ Base de datos '17_expertech_inventario.db' lista y estructurada.")

if __name__ == "__main__":
    inicializar_bd()