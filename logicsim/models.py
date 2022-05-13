from django.db import models

# Create your models here.

#This would probably be changed later to suit our needs.
class LogicGate(models.Model):
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
    input_a = models.IntegerField(default=0)
    input_b = models.IntegerField(default=0)
    output = models.IntegerField(default=0)
    image_url = models.TextField() #prob able to do based on gate_type

    #Truth table generator for printing pretty truth tables.
    def outputTable(self):
        input_a = self.input_a
        input_b = self.input_b
        output = self.output
        print("  | A | B | X |")
        print("  -------------")
        for i in range(2):
            for j in range(2):
                print("  | "+str(input_a)+" | "+str(input_b)+" | "+str(output)+" |")

    


