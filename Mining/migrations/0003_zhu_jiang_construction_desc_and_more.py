# Generated by Django 4.0.4 on 2022-06-08 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mining', '0002_delete_apply_record_hole_construction_desc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='zhu_jiang_construction',
            name='desc',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='zhu_jiang_construction',
            name='status',
            field=models.CharField(default='0', max_length=10),
        ),
        migrations.AlterField(
            model_name='hole_design',
            name='status',
            field=models.CharField(default='-1', max_length=10),
        ),
    ]