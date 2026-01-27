from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    # ORDENS DE SERVIÇO
    path('ordens/', views.ordem_list, name='ordem_list'),
    path('ordens/nova/', views.ordem_create, name='ordem_create'),
    path('ordens/<int:pk>/', views.ordem_detail, name='ordem_detail'),
    path('ordens/<int:pk>/editar/', views.ordem_edit, name='ordem_edit'),
    path('ordem/<int:pk>/editar/', views.ordem_update, name='ordem_update'),
    path('ordem/<int:pk>/excluir/', views.ordem_delete, name='ordem_delete'),



    # SERVIÇOS (editar / remover)
    path('ordens/<int:os_id>/servico/novo/', views.servico_create, name='servico_create'),
    path('ordens/servico/<int:pk>/editar/', views.servico_edit, name='servico_edit'),
    path('ordens/servico/<int:pk>/excluir/', views.servico_delete, name='servico_delete'),

    # PEÇAS (editar / remover)
    path('ordens/<int:os_id>/peca/nova/',views.peca_create,name='peca_create'),
    path('ordens/peca/<int:pk>/editar/', views.peca_edit, name='peca_edit'),
    path('ordens/peca/<int:pk>/excluir/', views.peca_delete, name='peca_delete'),

    # FINALIZAÇÃO
    path('ordens/<int:pk>/finalizar/', views.ordem_finalizar, name='ordem_finalizar'),

    # FINANCEIRO
    path('financeiro/novo/', views.financeiro_create, name='financeiro_create'),
    path('financeiro/', views.financeiro_dashboard, name='financeiro_dashboard'),
    path("financeiro/excluir/<int:pk>/", views.excluir_lancamento, name="excluir_lancamento"),


    # CLIENTES / VEÍCULOS
    path('clientes/', views.cliente_list, name='cliente_list'),
    path('veiculos/', views.veiculo_list, name='veiculo_list'),
    path('clientes/historico/', views.clientes_historico, name='clientes_historico'),
    path('clientes/<int:cliente_id>/ordens/', views.ordens_por_cliente, name='ordens_por_cliente'),

    # ESTOQUE
    path('estoque/', views.produto_list, name='produto_list'),
]
