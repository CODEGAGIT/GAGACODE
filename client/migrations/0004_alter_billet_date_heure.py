# Generated by Django 4.1.7 on 2023-04-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_billet_date_heure_alter_billet_infoligne_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billet',
            name='date_heure',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
