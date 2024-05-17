from django.db import models

class daftar_favorit(models.Model):
    username = models.CharField(max_length=255)
    timestamp = models.DateField(auto_now_add=True)
    id_tayangan = models.TextField()


class DaftarFavorit(models.Model):
    # Definisikan bidang sesuai dengan struktur tabel
    nama = models.CharField(max_length=100)
    # Tambahkan bidang lain jika diperlukan

    def __str__(self):
        return self.nama
