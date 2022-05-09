# Generated by Django 4.0.3 on 2022-05-04 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logicsim', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='logicgate',
            name='id',
        ),
        migrations.AddField(
            model_name='logicgate',
            name='gate_id',
            field=models.AutoField(default=0, primary_key=True, serialize=False),
        ),
        migrations.AddField(
            model_name='logicgate',
            name='input_a',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logicgate',
            name='input_b',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='logicgate',
            name='output',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='logicgate',
            name='gate_type',
            field=models.CharField(choices=[('and', 'AND'), ('nand', 'NAND'), ('or', 'OR'), ('nor', 'NOR'), ('xor', 'XOR'), ('xnor', 'XNOR'), ('not', 'NOT')], default='AND', max_length=9),
        ),
    ]