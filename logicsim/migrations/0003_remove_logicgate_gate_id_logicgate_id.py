# Generated by Django 4.0.4 on 2022-05-13 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logicsim', '0002_remove_logicgate_id_logicgate_gate_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logicgate',
            name='gate_id',
        ),
        migrations.AddField(
            model_name='logicgate',
            name='id',
            field=models.BigAutoField(auto_created=True, default=0, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
