from django.db import models
from clientes.models import Cliente, Veiculo


# =========================
# PEÇAS / ESTOQUE
# =========================
class Peca(models.Model):
    nome = models.CharField(max_length=120)
    custo = models.DecimalField(max_digits=10, decimal_places=2)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


# =========================
# ORÇAMENTO
# =========================
class Orcamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data = models.DateField(auto_now_add=True)
    aprovado = models.BooleanField(default=False)

    def __str__(self):
        return f"Orçamento #{self.id}"


class ServicoOrcamento(models.Model):
    orcamento = models.ForeignKey(
        Orcamento,
        related_name="servicos",
        on_delete=models.CASCADE
    )
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)


class PecaOrcamento(models.Model):
    orcamento = models.ForeignKey(
        Orcamento,
        related_name="pecas",
        on_delete=models.CASCADE
    )
    peca = models.ForeignKey(Peca, on_delete=models.CASCADE)
    quantidade = models.IntegerField()

    @property
    def total(self):
        return self.peca.preco_venda * self.quantidade


# =========================
# ORDEM DE SERVIÇO
# =========================
STATUS_CHOICES = (
    ('aberta', 'Aberta'),
    ('andamento', 'Em andamento'),
    ('finalizada', 'Finalizada'),
)


class OrdemServico(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)

    km = models.IntegerField()
    observacao = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='aberta'
    )

    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    orcamento = models.ForeignKey(
        Orcamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    @property
    def total_servicos(self):
        return sum(s.valor for s in self.servicos.all())

    @property
    def total_pecas(self):
        return sum(p.total for p in self.pecas.all())

    @property
    def total(self):
        return self.total_servicos + self.total_pecas

    def __str__(self):
        return f"OS #{self.id}"


class ServicoOS(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        related_name='servicos',
        on_delete=models.CASCADE
    )
    descricao = models.CharField(max_length=255)
    valor = models.DecimalField(max_digits=10, decimal_places=2)


    @property
    def total(self):
        return self.valor


class PecaOS(models.Model):
    ordem_servico = models.ForeignKey(
        OrdemServico,
        related_name='pecas',
        on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=150)
    quantidade = models.IntegerField()
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total(self):
        return self.quantidade * self.valor_unitario

class Veiculo(models.Model):
    placa = models.CharField(max_length=10, unique=True)


# =========================
# FINANCEIRO
# =========================
class MovimentoFinanceiro(models.Model):

    TIPO_CHOICES = (
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
    )

    CATEGORIA_CHOICES = (
        ('mao_obra', 'Mão de Obra'),
        ('peca', 'Peça'),
        ('compra_peca', 'Compra de Peça'),
        ('nf_emitida', 'Nota Fiscal Emitida'),
        ('nf_recebida', 'Nota Fiscal Recebida'),
        ('outros', 'Outros'),
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES
    )

    categoria = models.CharField(
        max_length=20,
        choices=CATEGORIA_CHOICES
    )

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    descricao = models.CharField(
        max_length=255
    )

    ordem_servico = models.ForeignKey(
        OrdemServico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='movimentos_financeiros'
    )

    data = models.DateField(
        auto_now_add=True
    )

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.get_tipo_display()} - R$ {self.valor}'
