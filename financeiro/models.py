from django.db import models

class MovimentoFinanceiro(models.Model):
    data = models.DateField(auto_now_add=True)
    tipo = models.CharField(
        max_length=10,
        choices=[("entrada","Entrada"),("saida","Saída")]
    )
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo} - {self.valor}"
