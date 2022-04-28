from django.db import models

# Create your models here.

#This would probably be changed later to suit our needs.
class LogicGate(models.Model):

    #you have an id col, then gate type(may need to be edited to account for custom components)
    #then input output cols, these may need to edited based on how we configure connections and stuff

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
    gate_type = models.CharField(max_length=9,
                                 choices=gate_choices,
                                 default="AND")

    input_a = models.IntegerField()
    input_b = models.IntegerField()
    output = models.IntegerField()