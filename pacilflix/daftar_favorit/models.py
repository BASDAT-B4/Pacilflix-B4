from django.db import models

class data_daftar_favorit(models.Model):
    username = models.CharField(max_length=255)
    timestamp = models.DateField(auto_now_add=True)
    judul = models.TextField()