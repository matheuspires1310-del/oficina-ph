from django import forms
from .models import OrdemServico, ServicoOS, PecaOS
from django import forms
from .models import ServicoOS


# =========================
# ORDEM DE SERVIÇO
# =========================
class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = [
            'cliente',
            'veiculo',
            'km',
            'observacao',
            'status',
            'orcamento',
        ]
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'veiculo': forms.Select(attrs={'class': 'form-select'}),
            'km': forms.NumberInput(attrs={'class': 'form-control'}),
            'observacao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'orcamento': forms.Select(attrs={'class': 'form-select'}),
        }

from django import forms

class PecaInlineForm(forms.Form):
    nome = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome da peça (ex: Óleo 5W30)'
        })
    )

    quantidade = forms.IntegerField(
        label='',
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Qtd'
        })
    )

    valor_unitario = forms.DecimalField(
        label='',
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Valor'
        })
    )



from django import forms
from .models import ServicoOS


class ServicoOSForm(forms.ModelForm):
    class Meta:
        model = ServicoOS
        fields = ['descricao', 'valor']
        widgets = {
            'descricao': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descrição do serviço'
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Valor'
            }),
        }
