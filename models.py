from database import get_connection

class Pasien:
    def __init__(self, nik, nama, alamat, no_telp):
        self.nik = nik
        self.nama = nama
        self.alamat = alamat
        self.no_telp = no_telp

    def simpan(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pasien VALUES (NULL, ?, ?, ?, ?)",
            (self.nik, self.nama, self.alamat, self.no_telp)
        )
        conn.commit()
        conn.close()

class Pendaftaran:
    def __init__(self, id_pasien):
        self.id_pasien = id_pasien

    def simpan(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO pendaftaran VALUES (NULL, ?, ?)",
            (self.id_pasien, "menunggu")
        )
        conn.commit()
        return cursor.lastrowid
    
class Antrian:
    def __init__(self, id_pendaftaran):
        self.id_pendaftaran = id_pendaftaran

    def generate(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM antrian")
        nomor = cursor.fetchone()[0]+1
        cursor.execute(
            "INSERT INTO antrian VALUES (NULL, ?, ?, ?)",
            (self.id_pendaftaran, nomor, "menunggu")
        )
        conn.commit()
        conn.close()
        return nomor
    
class Pemeriksaan:
    def __init__(self, id_pendaftaran, diagnosa, resep, biaya):
        self.id_pendaftaran = id_pendaftaran
        self.diagnosa = diagnosa
        self.resep = resep
        self.biaya = biaya
    
    def simpan(self):
        conn = get_connection()
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pemeriksaan VALUES (NULL, ?, ?, ?, ?)""",
            (self.id_pendaftaran, self.diagnosa, self.resep, self.biaya))
        conn.commit()

        cursor.execute("""
            UPDATE antrian 
            SET status = 'diperiksa' 
            WHERE id_pendaftaran = ?
        """, (self.id_pendaftaran,))

        conn.commit()
        conn.close()
        return cursor.lastrowid

class Pembayaran:
    def __init__(self, id_pemeriksaan, total):
        self.id_pemeriksaan = id_pemeriksaan
        self.total = total

    def bayar(self):
        conn = get_connection()
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO pembayaran VALUES (NULL, ?, ?, ?)""",
            (self.id_pemeriksaan, self.total, "Lunas"))
        
        cursor.execute("""
            UPDATE antrian 
            SET status = 'selesai' 
            WHERE id_pendaftaran = (
                SELECT id_pendaftaran
                FROM pemeriksaan
                WHERE id_pemeriksaan = ?)
        """, (self.id_pemeriksaan,))

        conn.commit()
        conn.close()
        