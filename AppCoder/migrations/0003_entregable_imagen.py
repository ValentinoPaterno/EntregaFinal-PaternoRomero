# Generated by Django 4.1.7 on 2023-04-05 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppCoder', '0002_alter_curso_id_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='entregable',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]