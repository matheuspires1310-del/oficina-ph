from django.contrib import admin
from .models import Cliente, Veiculo


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nome", "telefone")
    search_fields = ("nome", "telefone", "email")


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ("modelo", "placa", "cliente")
    search_fields = ("modelo", "placa")
    list_filter = ("cliente",)
