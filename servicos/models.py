from django.db import models

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    custo_interno = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    preco_cobrado = models.DecimalField(max_digits=10, decimal_places=2)

    def lucro(self):
        return self.preco_cobrado - self.custo_interno

    def __str__(self):
        return self.nome
