from django.contrib import admin
from .models import (
    Cliente, Veiculo, Peca,
    Orcamento, ServicoOrcamento, PecaOrcamento,
    OrdemServico, MovimentoFinanceiro
)

@admin.register(Peca)
class PecaAdmin(admin.ModelAdmin):
    list_display = ("nome", "quantidade", "custo", "preco_venda")


class ServicoInline(admin.TabularInline):
    model = ServicoOrcamento
    extra = 1


class PecaInline(admin.TabularInline):
    model = PecaOrcamento
    extra = 1


@admin.register(Orcamento)
class OrcamentoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "veiculo", "data", "aprovado")
    inlines = [ServicoInline, PecaInline]


@admin.register(OrdemServico)
class OrdemServicoAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "veiculo", "criado_em", "status")



@admin.register(MovimentoFinanceiro)
class MovimentoFinanceiroAdmin(admin.ModelAdmin):
    list_display = ("data", "tipo", "descricao", "valor")
