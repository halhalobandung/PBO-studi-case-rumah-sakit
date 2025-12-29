import tkinter as tk
from tkinter import messagebox, ttk
from database import create_table, get_connection
from models import Pasien, Pendaftaran, Antrian, Pemeriksaan, Pembayaran

create_table()

root = tk.Tk()
root.title("Sistem Rumah Sakit")
root.geometry("400x550")

def clear_frame():
    for widget in root.winfo_children():
        widget.destroy()

def tampilkan_antrian(frame):
    for widget in frame.winfo_children():
        if isinstance(widget, ttk.Treeview):
            widget.destroy()    

    tree = ttk.Treeview(frame, columns=("id", "nomor", "status"), show="headings")
    tree.heading("id", text="ID Daftar")
    tree.heading("nomor", text="No Antrian")
    tree.heading("status", text="Status")

    tree.column("id", width=80)    
    tree.column("nomor", width=80)    
    tree.column("status", width=100)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.id_pendaftaran, a.nomor, a.status
        FROM antrian a
        ORDER BY a.nomor
    """)
    rows = cur.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

    tree.pack(pady=10) 

def menu_frontdesk():
    clear_frame()
    tk.Label(root, text="MENU FRONT DESK", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="NIK").pack()
    nik_entry = tk.Entry(root)
    nik_entry.pack()

    tk.Label(root, text="Nama").pack()
    nama_entry = tk.Entry(root)
    nama_entry.pack()

    tk.Label(root, text="Alamat").pack()
    alamat_entry = tk.Entry(root)
    alamat_entry.pack()

    tk.Label(root, text="No Telp").pack()
    telp_entry = tk.Entry(root)
    telp_entry.pack()

    def daftar_pasien():
        pasien = Pasien(
            nik_entry.get(),
            nama_entry.get(),
            alamat_entry.get(),
            telp_entry.get()
        )
        pasien.simpan()
        messagebox.showinfo("Sukses", "Pasien berhasil didaftarkan")

    def daftar_antrian():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id_pasien FROM pasien ORDER BY id_pasien DESC LIMIT 1")
        id_pasien = cur.fetchone()[0]

        daftar = Pendaftaran(id_pasien)
        id_daftar = daftar.simpan()

        antrian = Antrian(id_daftar)
        nomor = antrian.generate()

        messagebox.showinfo("Antrian", f"Nomor Antrian: {nomor}")
        tampilkan_antrian(root)

    tk.Button(root, text="Daftar Pasien", command=daftar_pasien).pack(pady=5)
    tk.Button(root, text="Ambil Antrian", command=daftar_antrian).pack(pady=5)
    tk.Label(root, text="Daftar Antrian").pack(pady=10)
    tampilkan_antrian(root)
    tk.Button(root, text="Kembali", command=menu_awal).pack(pady=10)

def menu_dokter():
    clear_frame()
    tk.Label(root, text="MENU DOKTER", font=("Arial", 14)).pack(pady=10)

    tk.Label(root, text="ID Pendaftaran").pack()
    id_daftar_entry = tk.Entry(root)
    id_daftar_entry.pack()

    tk.Label(root, text="Diagnosa").pack()
    diagnosa_entry = tk.Entry(root)
    diagnosa_entry.pack()

    tk.Label(root, text="Resep").pack()
    resep_entry = tk.Entry(root)
    resep_entry.pack()

    tk.Label(root, text="Biaya").pack()
    biaya_entry = tk.Entry(root)
    biaya_entry.pack()

    def simpan_pemeriksaan():
        periksa = Pemeriksaan(
            int(id_daftar_entry.get()),
            diagnosa_entry.get(),
            resep_entry.get(),
            int(biaya_entry.get())
        )
        periksa.simpan()
        messagebox.showinfo("Sukses", "Pemeriksaan disimpan")

    tk.Button(root, text="Simpan Pemeriksaan", command=simpan_pemeriksaan).pack(pady=5)
    tk.Label(root, text="Daftar Antrian").pack(pady=10)
    tampilkan_antrian(root)
    tk.Button(root, text="Kembali", command=menu_awal).pack(pady=10)

def menu_admin():
    clear_frame()
    tk.Label(root, text="MENU ADMINISTRASI", font=("Arial", 14)).pack(pady=10)
    tk.Label(root, text="Daftar Antrian").pack()
    tampilkan_antrian(root)

    tk.Label(root, text="ID Pemeriksaan").pack()
    id_periksa_entry = tk.Entry(root)
    id_periksa_entry.pack()

    tk.Label(root, text="Total Bayar").pack()
    total_entry = tk.Entry(root)
    total_entry.pack()

    def proses_bayar():
        bayar = Pembayaran(
            int(id_periksa_entry.get()),
            int(total_entry.get())
        )
        bayar.bayar()
        messagebox.showinfo("Pembayaran", "Pembayaran Berhasil")

    tk.Button(root, text="Bayar", command=proses_bayar).pack(pady=5)
    tk.Label(root, text="Daftar Antrian").pack(pady=10)
    tampilkan_antrian(root)
    tk.Button(root, text="Kembali", command=menu_awal).pack(pady=10)

def menu_awal():
    clear_frame()
    tk.Label(root, text="SISTEM RUMAH SAKIT", font=("Arial", 16)).pack(pady=20)

    tk.Button(root, text="Front Desk", width=20, command=menu_frontdesk).pack(pady=10)
    tk.Button(root, text="Dokter", width=20, command=menu_dokter).pack(pady=10)
    tk.Button(root, text="Administrasi", width=20, command=menu_admin).pack(pady=10)

menu_awal()
root.mainloop()