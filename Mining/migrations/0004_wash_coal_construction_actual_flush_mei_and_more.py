# Generated by Django 4.0.4 on 2022-06-18 23:05

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Mining', '0003_zhu_jiang_construction_desc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='wash_coal_construction',
            name='actual_flush_mei',
            field=models.FloatField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='wash_coal_construction',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]