from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    categoria = models.CharField(max_length=50)
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    estoque_atual = models.IntegerField(default=0)

    def lucro_unitario(self):
        return self.preco_venda - self.custo_unitario

    def __str__(self):
        return self.nome
