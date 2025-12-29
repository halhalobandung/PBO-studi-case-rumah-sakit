import sqlite3

def get_connection():
    return sqlite3.connect("hospital.db")

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pasien (
        id_pasien INTEGER PRIMARY KEY AUTOINCREMENT,
        nik TEXT UNIQUE,
        nama TEXT,
        alamat TEXT,
        no_telp TEXT       
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pendaftaran (
        id_pendaftaran INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pasien INTEGER,
        status TEXT,
        FOREIGN KEY (id_pasien) REFERENCES pasien(id_pasien)       
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS antrian (
        id_antrian INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pendaftaran INTEGER,
        nomor INTEGER,
        status TEXT,
        FOREIGN KEY (id_pendaftaran) REFERENCES pendaftaran(id_pendaftaran)       
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pemeriksaan (
        id_pemeriksaan INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pendaftaran INTEGER,
        diagnosa TEXT,
        resep TEXT,
        biaya INTEGER,
        FOREIGN KEY (id_pendaftaran) REFERENCES pendaftaran(id_pendaftaran)       
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pembayaran (
        id_pembayaran INTEGER PRIMARY KEY AUTOINCREMENT,
        id_pemeriksaan INTEGER,
        total INTEGER,
        status TEXT,
        FOREIGN KEY (id_pemeriksaan) REFERENCES pemeriksaan(id_pemeriksaan)    
    )
    """)

    conn.commit()
    conn.close()