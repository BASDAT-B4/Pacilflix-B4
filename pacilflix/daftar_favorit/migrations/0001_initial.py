# Generated by Django 5.0.4 on 2024-05-02 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='daftar_favorit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('judul', models.TextField()),
            ],
        ),
    ]
