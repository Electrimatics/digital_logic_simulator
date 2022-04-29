from django.db import models

# Create your models here.

#This would probably be changed later to suit our needs.
class LogicGate(models.Model):

    gate_id = models.AutoField(primary_key=True)

    AND = 'and'
    NAND = 'nand'
    OR = 'or'
    NOR = 'nor'
    XOR = 'xor'
    XNOR = 'xnor'
    NOT = 'not'
    gate_choices = (
        (AND, "AND"),
        (NAND, "NAND"),
        (OR, "OR"),
        (NOR, "NOR"),
        (XOR, "XOR"),
        (XNOR, "XNOR"),
        (NOT, "NOT")
    )
    gate_type = models.CharField(max_length=9, choices=gate_choices, default="AND")

    input_a = models.IntegerField()
    input_b = models.IntegerField()
    output = models.IntegerField()
    image_url = models.TextField() prob able to do based on gate_type

