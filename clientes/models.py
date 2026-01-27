from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nome


class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    placa = models.CharField(max_length=10)
    modelo = models.CharField(max_length=100)
    ano = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.modelo} - {self.placa}"
