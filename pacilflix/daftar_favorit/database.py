import psycopg2

# Menghubungkan ke database
conn = psycopg2.connect(
    host="hostname",
    database="pacilflix",
    user="lizidelyx",
    password="password"
)

# Membuat kursor
cur = conn.cursor()

# Menjalankan query untuk mengambil data dari tabel daftar_favorit
cur.execute("SELECT * FROM pacilflix.daftar_favorit")
daftar_favorit_rows = cur.fetchall()

# Menampilkan hasil
print("Data dari tabel daftar_favorit:")
for row in daftar_favorit_rows:
    print(row)

# Menjalankan query untuk mengambil data dari tabel daftar_unduhan
cur.execute("SELECT * FROM pacilflix.daftar_unduhan")
daftar_unduhan_rows = cur.fetchall()

# Menampilkan hasil
print("Data dari tabel daftar_unduhan:")
for row in daftar_unduhan_rows:
    print(row)

# Menutup koneksi
cur.close()
conn.close()
