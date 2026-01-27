from django.db import models
from clientes.models import Cliente, Veiculo
from estoque.models import Produto
from servicos.models import Servico

class Orcamento(models.Model):
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="orcamentos_app"
    )

    veiculo = models.ForeignKey(
        Veiculo,
        on_delete=models.CASCADE,
        related_name="orcamentos_app"
    )


    data = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("rascunho","Rascunho"),("aprovado","Aprovado"),("recusado","Recusado")]
    )

    def __str__(self):
        return f"Orçamento {self.id}"

class OrcamentoPeca(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    custo_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)


class OrcamentoServico(models.Model):
    orcamento = models.ForeignKey(Orcamento, on_delete=models.CASCADE)
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    preco = models.DecimalField(max_digits=10, decimal_places=2)

