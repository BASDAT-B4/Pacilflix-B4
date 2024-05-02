from django.forms import ModelForm
from daftar_favorit.models import data_daftar_favorit

class data_daftar_favorit(ModelForm):
    class Meta:
        model = data_daftar_favorit
        fields = ["username", "judul"]