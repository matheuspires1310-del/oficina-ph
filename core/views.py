from django.shortcuts import render, redirect, get_object_or_404
from decimal import Decimal
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404, redirect
from .models import ServicoOS
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Sum
from django.utils.timezone import now
from datetime import datetime
from .models import MovimentoFinanceiro
from django.shortcuts import render, get_object_or_404, redirect
from .models import OrdemServico
from clientes.models import Cliente, Veiculo
from .forms import ServicoOSForm
from .models import (
    OrdemServico,
    MovimentoFinanceiro,
    ServicoOS,
    PecaOS,
    Peca
)
from estoque.models import Produto
from .forms import PecaInlineForm
from .forms import ServicoOSForm, PecaInlineForm
from django.views.decorators.http import require_POST




# =========================
# DASHBOARD
# =========================
def dashboard(request):
    entradas = MovimentoFinanceiro.objects.filter(tipo="entrada")
    saidas = MovimentoFinanceiro.objects.filter(tipo="saida")

    total_entrada = sum(e.valor for e in entradas)
    total_saida = sum(s.valor for s in saidas)
    saldo = total_entrada - total_saida

    ordens = OrdemServico.objects.order_by('-id')

    return render(request, "dashboard.html", {
        "total_entrada": total_entrada,
        "total_saida": total_saida,
        "saldo": saldo,
        "os_abertas": OrdemServico.objects.filter(status="aberta").count(),
        "os_andamento": OrdemServico.objects.filter(status="andamento").count(),
        "os_finalizadas": OrdemServico.objects.filter(status="finalizada").count(),
        "ordens": ordens[:10],
    })


# =========================
# ORDENS DE SERVIÇO
# =========================
def ordem_list(request):
    ordens = OrdemServico.objects.all().order_by('-id')
    return render(request, 'ordens/list.html', {
        'ordens': ordens
    })

def ordem_edit(request, pk):
    ordem = get_object_or_404(OrdemServico, pk=pk)

    servico_form = ServicoOSForm()
    peca_form = PecaInlineForm()   

    if request.method == 'POST':

        # =========================
        # ADICIONAR SERVIÇO
        # =========================
        if 'add_servico' in request.POST:
            servico_form = ServicoOSForm(request.POST)

            if servico_form.is_valid():
                servico = servico_form.save(commit=False)
                servico.ordem_servico = ordem
                servico.save()
                return redirect('ordem_edit', pk=ordem.id)


        # =========================
        # ADICIONAR PEÇA (SEM FORM)
        # =========================
        if 'add_peca' in request.POST:
            peca_form = PecaInlineForm(request.POST)

            if peca_form.is_valid():
                PecaOS.objects.create(
                    ordem_servico=ordem,
                    nome=peca_form.cleaned_data['nome'],
                    quantidade=peca_form.cleaned_data['quantidade'],
                    valor_unitario=peca_form.cleaned_data['valor_unitario'],
                )

                return redirect('ordem_edit', pk=ordem.id)


    # =========================
    # TOTAIS
    # =========================
    total_servicos = sum(
        (s.valor or Decimal('0.00')) for s in ordem.servicos.all()
    )

    total_pecas = sum(
        (p.total or Decimal('0.00')) for p in ordem.pecas.all()
    )

    total_ordem = total_servicos + total_pecas

    return render(request, 'ordens/edit.html', {
        'ordem': ordem,
        'servico_form': servico_form,
        'peca_form': peca_form,
        'total_ordem': total_ordem,
    })



def servico_create(request, os_id):
    os = get_object_or_404(OrdemServico, id=os_id)

    if request.method == 'POST':
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')

        if descricao and valor:
            ServicoOS.objects.create(
                ordem_servico=os,
                descricao=descricao,
                valor=valor
            )

        return redirect('ordem_edit', os_id=os.id)

    return render(request, 'ordens/servico_create.html', {
        'os': os
    })

def peca_create(request, os_id):
    os = get_object_or_404(OrdemServico, id=os_id)
    pecas = Peca.objects.all()

    if request.method == 'POST':
        peca_id = request.POST.get('peca')
        quantidade = request.POST.get('quantidade')
        valor_unitario = request.POST.get('valor_unitario')

        if peca_id and quantidade and valor_unitario:
            PecaOS.objects.create(
                ordem_servico=os,
                peca_id=peca_id,
                quantidade=quantidade,
                valor_unitario=valor_unitario
            )

        return redirect('ordem_edit', os.id)

    return render(request, 'ordens/peca_create.html', {
        'os': os,
        'pecas': pecas
    })


def ordem_create(request):
    if request.method == 'POST':

        cliente_id = request.POST.get('cliente')
        if cliente_id:
            cliente = Cliente.objects.get(id=cliente_id)
        else:
            cliente = Cliente.objects.create(
                nome=request.POST.get('cliente_nome'),
                telefone=request.POST.get('cliente_telefone')
            )

        veiculo_id = request.POST.get('veiculo')
        if veiculo_id:
            veiculo = Veiculo.objects.get(id=veiculo_id)
        else:
            veiculo = Veiculo.objects.create(
                cliente=cliente,
                modelo=request.POST.get('veiculo_modelo'),
                placa=request.POST.get('veiculo_placa')
            )

        os = OrdemServico.objects.create(
            cliente=cliente,
            veiculo=veiculo,
            km=int(request.POST.get('km') or 0),
            observacao=request.POST.get('observacao', '')
        )

        return redirect('ordem_detail', pk=os.id)

    return render(request, 'ordens/create.html', {
        'clientes': Cliente.objects.all(),
        'veiculos': Veiculo.objects.all()
    })


def ordem_detail(request, pk):
    print(request.POST) 
    os = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':

        # ADD SERVIÇO
        if request.POST.get('acao') == 'add_servico':
            ServicoOS.objects.create(
                ordem_servico=os,
                descricao=request.POST.get('servico_descricao'),
                valor=Decimal(request.POST.get('servico_valor'))
            )

        # EDIT SERVIÇO
        if request.POST.get('acao') == 'edit_servico':
            servico = ServicoOS.objects.get(id=request.POST.get('servico_id'))
            servico.descricao = request.POST.get('servico_descricao')
            servico.valor = Decimal(request.POST.get('servico_valor'))
            servico.save()

        # DELETE SERVIÇO
        if request.POST.get('acao') == 'del_servico':
            ServicoOS.objects.filter(id=request.POST.get('servico_id')).delete()

        # ADD PEÇA
        if request.POST.get('acao') == 'add_peca':
            nome = request.POST.get('peca_nome')
            quantidade = int(request.POST.get('quantidade'))
            valor_unitario = Decimal(request.POST.get('valor_unitario'))

            # 🔥 cria a peça da OS direto, sem depender de cadastro
            PecaOS.objects.create(
                ordem_servico=os,
                nome=nome,
                quantidade=quantidade,
                valor_unitario=valor_unitario
            )

            return redirect('ordem_detail', os.id)


        # EDIT PEÇA
        if request.POST.get('acao') == 'edit_peca':
            item = PecaOS.objects.get(id=request.POST.get('peca_os_id'))
            item.quantidade = int(request.POST.get('quantidade'))
            item.valor_unitario = Decimal(request.POST.get('valor_unitario'))
            item.save()

        # DELETE PEÇA
        if request.POST.get('acao') == 'del_peca':
            PecaOS.objects.filter(id=request.POST.get('peca_os_id')).delete()

        return redirect('ordem_detail', pk=pk)

    return render(request, 'ordens/detail.html', {
        'os': os,
        'pecas': Peca.objects.all()
    })


def ordem_finalizar(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)
    os.status = 'finalizada'
    os.data_fechamento = now().date()
    os.save()

    total = os.total
    if total > 0:
        MovimentoFinanceiro.objects.create(
            tipo='entrada',
            valor=total,
            descricao=f'OS #{os.id} - {os.cliente}'
        )

    return redirect('ordem_detail', pk=pk)


def ordem_update(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':
        os.cliente_id = request.POST.get('cliente')
        os.veiculo = request.POST.get('veiculo')
        os.status = request.POST.get('status')
        os.descricao = request.POST.get('descricao')
        os.save()

        return redirect('ordem_detail', os.id)

    return render(request, 'ordens/update.html', {
        'os': os,
        'clientes': Cliente.objects.all()
    })

def ordem_delete(request, pk):
    os = get_object_or_404(OrdemServico, pk=pk)

    if request.method == 'POST':
        os.delete()
        return redirect('dashboard')

    return render(request, 'ordens/delete.html', {'os': os})

# =========================
# FINANCEIRO
# =========================
def financeiro_list(request):
    return render(request, 'financeiro/list.html', {
        'movimentos': MovimentoFinanceiro.objects.all().order_by('-id')
    })


def financeiro_create(request):
    ordens = OrdemServico.objects.all().order_by('-id')

    if request.method == 'POST':
        tipo = request.POST.get('tipo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor_raw = request.POST.get('valor')
        ordem_id = request.POST.get('ordem_servico') or None

        if not valor_raw or not descricao or not tipo:
            return render(request, 'financeiro/create.html', {
                'ordens': ordens,
                'erro': 'Preencha todos os campos obrigatórios.'
            })

        valor = Decimal(request.POST.get('valor').replace(',', '.'))

        MovimentoFinanceiro.objects.create(
            tipo=tipo,
            categoria=categoria,
            descricao=descricao,
            valor=valor,
            ordem_servico_id=ordem_id if ordem_id else None
        )

        return redirect('financeiro_dashboard')

    return render(request, 'financeiro/create.html', {
        'ordens': ordens
    })

def financeiro_dashboard(request):
    total_entradas = (
        MovimentoFinanceiro.objects
        .filter(tipo='entrada')
        .aggregate(total=Sum('valor'))
        .get('total') or 0
    )

    total_saidas = (
        MovimentoFinanceiro.objects
        .filter(tipo='saida')
        .aggregate(total=Sum('valor'))
        .get('total') or 0
    )

    saldo = total_entradas - total_saidas

    movimentos = MovimentoFinanceiro.objects.all().order_by('-criado_em')

    return render(request, 'financeiro/list.html', {
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo': saldo,
        'movimentos': movimentos,
    })

@require_POST
def excluir_lancamento(request, pk):
    try:
        movimento = MovimentoFinanceiro.objects.get(pk=pk)
        movimento.delete()
    except MovimentoFinanceiro.DoesNotExist:
        pass  # já foi excluído ou não existe

    return redirect("financeiro_dashboard")

# =========================
# CLIENTES / VEÍCULOS
# =========================
def cliente_list(request):
    return render(request, 'clientes/list.html', {
        'clientes': Cliente.objects.all()
    })
    


def veiculo_list(request):
    return render(request, 'veiculos/list.html', {
        'veiculos': Veiculo.objects.select_related('cliente')
    })

def buscar_clientes(request):
    q = request.GET.get("q", "")
    clientes = Cliente.objects.filter(nome__icontains=q)[:5]
    return JsonResponse([
        {"id": c.id, "nome": c.nome, "telefone": c.telefone}
        for c in clientes
    ], safe=False)


def clientes_historico(request):
    q = request.GET.get('q')

    clientes = Cliente.objects.filter(
        ordemservico__isnull=False
    ).distinct()

    if q:
        clientes = clientes.filter(
            Q(nome__icontains=q) |
            Q(telefone__icontains=q)
        )

    return render(request, 'clientes/historico.html', {
        'clientes': clientes
    })


def ordens_por_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    ordens = OrdemServico.objects.filter(cliente=cliente)

    return render(request, 'ordens/por_cliente.html', {
        'cliente': cliente,
        'ordens': ordens
    })

# =========================
# ESTOQUE
# =========================
def produto_list(request):
    return render(request, 'estoque/list.html', {
        'produtos': Produto.objects.all()
    })


def peca_edit(request, pk):
    item = get_object_or_404(PecaOS, pk=pk)

    if request.method == "POST":
        item.quantidade = int(request.POST.get("quantidade"))
        item.valor_unitario = Decimal(request.POST.get("valor_unitario"))
        item.save()
        return redirect('ordem_detail', pk=item.ordem_servico.id)

    return render(request, "ordens/peca_edit.html", {
        "item": item
    })

def peca_delete(request, pk):
    item = get_object_or_404(PecaOS, pk=pk)
    os_id = item.ordem_servico.id
    item.delete()
    return redirect('ordem_detail', pk=os_id)

def servico_delete(request, pk):
    servico = get_object_or_404(ServicoOS, pk=pk)
    os_id = servico.ordem_servico.id
    servico.delete()
    return redirect('ordem_detail', pk=os_id)

def servico_edit(request, pk):
    servico = get_object_or_404(ServicoOS, pk=pk)

    if request.method == "POST":
        servico.descricao = request.POST.get("descricao")
        servico.valor = Decimal(request.POST.get("valor"))
        servico.save()
        return redirect('ordem_detail', pk=servico.ordem_servico.id)

    return render(request, "ordens/servico_edit.html", {
        "servico": servico
    })
