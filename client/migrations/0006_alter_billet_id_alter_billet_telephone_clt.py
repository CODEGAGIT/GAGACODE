# Generated by Django 4.1.7 on 2023-04-28 13:57

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_billet_infoligne_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billet',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='billet',
            name='telephone_clt',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='TG'),
        ),
    ]
