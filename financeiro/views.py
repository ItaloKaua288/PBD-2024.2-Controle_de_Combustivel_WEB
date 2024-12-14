from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.db.models import Count, Sum, Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView, View
from django.contrib import messages
from django.utils import timezone
from .models import Financeiro
from .forms import FinanceiroAbastForm, RelatorioVeiculoForm
from utils.forms import BuscaForm, get_data_form
from utils.utils import get_list_placa, get_list_combustivel, get_combustivel_tipo, HasRoleMixinCustom
from veiculos.models import Veiculo, TipoCombustivel

class Financeiro_abast_listar_view(LoginRequiredMixin, HasRoleMixinCustom, ListView):
    """
    Exibe a lista de financeiros de abastecimento gerados
    """
    model = Financeiro
    template_name = 'financeiro_abastecimento.html'
    login_url = reverse_lazy('login')
    required_permission = 'Administrador'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['busca_form'] = BuscaForm()
        context['cadastro_form'] = FinanceiroAbastForm()
        return context

    def get_queryset(self):
        datas = get_data_form(self.request)
        queryset = super().get_queryset()
        if None not in datas:
            return Financeiro.objects.filter(Q(data_inicial__range=datas) | Q(data_final__range=datas))
        return queryset

class Financeiro_abast_cadastrar_view(LoginRequiredMixin, HasRoleMixinCustom, CreateView):
    """
    Gera novos financeiros de abastecimento.
    """
    model = Financeiro
    form_class = FinanceiroAbastForm
    template_name = 'base_CRUD.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('financeiro_abast')
    allowed_roles = ['administrador']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_titulo"] = 'Cadastrar'
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Financeiro de abastecimentos gerado com sucesso!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)
        
class Financeiro_abast_view(LoginRequiredMixin, HasRoleMixinCustom, DetailView):
    """
    Exibe as informações de um financeiro de abastecimento existente.
    """
    model = Financeiro
    template_name = 'financeiro_vizualizar.html'
    login_url = reverse_lazy('login')
    allowed_roles = ['administrador']
    
    def _processar_dados(self, dados_str:str):
        """
        Converte uma string de dados no formato de dicionário em um dicionário Python.
        """
        dados = {}
        for item in dados_str.replace('{','').replace('}','').replace('"','').split(', '):
            k, v = item.split(': ')
            dados[get_combustivel_tipo(k)] = float(v)
        return dados
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        financeiro = self.get_object()
        abastecimentos = financeiro.abastecimentos
        litros = self._processar_dados(financeiro.litros)
        totais = self._processar_dados(financeiro.totais)

        veiculos = {
            veiculo: {
                'litros': abastecimentos.filter(veiculo__placa=veiculo).aggregate(Sum('litros'))['litros__sum'],
                'gasto': self.get_object().abastecimentos.filter(veiculo__placa=veiculo).aggregate(Sum('valor_total'))['valor_total__sum'],
                'num_abast': self.get_object().abastecimentos.filter(veiculo__placa=veiculo).count()
            }
            for veiculo in get_list_placa(abastecimentos.values('veiculo').annotate(count=Count('veiculo')))
        }

        context['cards'] = {
            'num_abast': {'label': 'Número de abastecimentos', 'data': abastecimentos.count()},
            'litros': {'label': 'Litros', 'data': litros},
            'totais': {'label': 'Totais R$', 'data': totais},
            'veiculos': {'label': 'Veiculos', 'data': veiculos}
        }

        combustiveis_usados = get_list_combustivel(abastecimentos.values('tipo_combustivel').annotate(litros=Sum('litros')))
        context['graficos'] = {
            'combustiveis': {'labels': list(combustiveis_usados.keys()), 'data': list(combustiveis_usados.values())}
        }

        return context  

class Financeiro_abast_deletar_view(LoginRequiredMixin, HasRoleMixinCustom, DeleteView):
    """
    Deleta um financeiro existente
    """
    model = Financeiro
    template_name = 'financeiro_vizualizar.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('financeiro_abast')
    allowed_roles = ['administrador']

    def dispatch(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        if 'abast_pk' in request.GET:
            return redirect('financeiro_abast_lista', pk=request.GET.get('abast_pk'))
        return redirect('financeiro_abast')

class Relatorio_veiculo_view(LoginRequiredMixin, HasRoleMixinCustom, View):
    template_name = 'relatorio_veiculo.html'
    
    def _processar_combustiveis(self, dados):
        return [get_combustivel_tipo(get_object_or_404(TipoCombustivel, pk=x).tipo) for x in dados]
    
    def _processar_abast_mes(self, abast):
        dias = [x for x in range(1, 31)]
        gastos = [0 for x in range(30)]
        litros = [0 for x in range(30)]
        valores = list(abast.values('data_abastecimento__day').annotate(valor=Sum('valor_total'), litros=Sum('litros')))
        for item in valores:
            gastos[int(item['data_abastecimento__day'])-1] = item['valor']
            litros[int(item['data_abastecimento__day'])-1] = item['litros']
        return dias, gastos, litros

    def get(self, request, *args, **kwargs):
        form_mes = RelatorioVeiculoForm(data=request.GET)
        mes = timezone.now().month

        if form_mes.is_valid():
            mes = form_mes.cleaned_data['mes']
        
        object = get_object_or_404(Veiculo, pk=kwargs.get('pk'))
        context = {'form': RelatorioVeiculoForm(), 'dados': {'veiculo': object}}
        abastecimentos = object.abastecimentos.filter(data_abastecimento__month=mes)
        
        if abastecimentos.exists():
            valor_gasto = abastecimentos.aggregate(Sum('valor_total'))['valor_total__sum']
            litros = abastecimentos.aggregate(Sum('litros'))['litros__sum']
            count_combustivel = abastecimentos.values('tipo_combustivel').annotate(count=Count('tipo_combustivel'))
            abast_mes = self._processar_abast_mes(abastecimentos)
            km_rodado = abastecimentos.order_by('quilometragem').last().quilometragem - abastecimentos.order_by('quilometragem').first().quilometragem
            
            context['dados'].update(
                {
                    'cards': {
                        'int': {'Vezes abastecido': abastecimentos.count()},
                        'float': {'Valor gasto': valor_gasto, 'Litros': litros, 'Gasto/litro': valor_gasto/litros,'KM rodado':km_rodado}
                    },
                    'graficos': {
                        'combustivel_usado': {
                            'labels': self._processar_combustiveis(list(count_combustivel.values_list('tipo_combustivel', flat=True))),
                            'data': list(count_combustivel.values_list('count', flat=True))
                        },
                        'abastecimentos_mes': {'labels': abast_mes[0], 'data_valor': abast_mes[1], 'data_litros': abast_mes[2]}
                    }
                }
            )
        return render(request, self.template_name, context)