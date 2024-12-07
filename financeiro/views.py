# from django.shortcuts import render, get_object_or_404
# from django.contrib import messages
# from postos.models import Abastecimento, Posto
# from veiculos.models import Veiculo
# from django.db.models import Avg, Sum, Count
# import json
# from django.utils import timezone
# from .forms import RelatorioVeiculoForm, RelatorioGeralForm
# from utils.utils import get_perfil_logado
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic import ListView, CreateView, UpdateView, DetailView
# from rolepermissions.mixins import HasRoleMixin


# def get_dict_diario(queryset, value, value_soma):
#     """
#     Função que retorna um dicionario do mês com dados de cada dia
#     Parametros:
#         value: nome da coluna da tabela que desejar agrupar
#         value_soma: valor que será somado de cada grupo
#     """
#     mes = {x: 0 for x in range(1, 31)}
#     queryset_ordenada = queryset.values(value).annotate(total=Sum(value_soma)).order_by(f'-{value}')
#     for x in queryset_ordenada: mes[x[value]] = x['total']
#     return mes

# class Geral_mensal_view(LoginRequiredMixin, HasRoleMixin, DetailView):
#     ...


# def geral_mensal_view(request):
#     """
#     Exibe um relatório mensal do mês desejado
#     """
#     dados = {}
#     if request.method == 'POST':
#         form = RelatorioGeralForm(request.POST)
#         if form.is_valid():
#             abastecimentos = Abastecimento.objects.filter(data_abastecimento__month=form.cleaned_data['mes'])
#             if abastecimentos.exists():
#                 dados = {
#                     'mais_abastecidos': {
#                         'Veiculo': get_object_or_404(Veiculo, pk=abastecimentos.values('veiculo').annotate(total=Sum('valor_total')).order_by('-total').first()['veiculo']).placa,
#                         'Posto': get_object_or_404(Posto, pk=abastecimentos.values('posto').annotate(total=Sum('valor_total')).order_by('-total').first()['posto'])
#                     },
#                     'medias': {
#                         'Valor médio L': abastecimentos.aggregate(Avg('valor_total'))['valor_total__avg']/abastecimentos.aggregate(Sum('litros'))['litros__sum'],
#                         'Valor médio/Veículo': abastecimentos.aggregate(Avg('valor_total'))['valor_total__avg']/abastecimentos.values('veiculo').distinct().aggregate(Count('veiculo'))['veiculo__count'],
#                         'Litros/Real': abastecimentos.aggregate(Sum('litros'))['litros__sum']/abastecimentos.aggregate(Sum('valor_total'))['valor_total__sum'],
#                     },
#                     'total': {
#                         'Número de abastecimentos': abastecimentos.count(),
#                         'Gasto total': abastecimentos.aggregate(Sum('valor_total'))['valor_total__sum'],
#                     },
#                     'grafico_dias': {
#                         'labels': list(get_dict_diario(abastecimentos, 'data_abastecimento__day', 'litros').keys()),
#                         'data_litros': list(get_dict_diario(abastecimentos, 'data_abastecimento__day', 'litros').values()),
#                         'data_valor': list(get_dict_diario(abastecimentos, 'data_abastecimento__day', 'valor_total').values())
#                     }
#                 }
#         else:
#             messages.error(request, form.errors)
#     else:
#         form = RelatorioGeralForm()
#     return render(request, 'relatorios.html', {'perfil_logado':get_perfil_logado(request),'form':form,'dados':dados})

# def relatorio_veiculo_view(request):
#     """
#     Exibi um relatório sobre um veiculo cadastrado
#     """
#     dados = {}
#     if request.method == 'POST':
#         form = RelatorioVeiculoForm(request.POST)
#         if form.is_valid():
#             veiculo = get_object_or_404(Veiculo, placa=form.cleaned_data['placa'])
#             abastecimentos = veiculo.abastecimentos.all().filter(data_abastecimento__month=form.cleaned_data['mes']).order_by('-data_abastecimento')
#             dados['veiculo'] = veiculo

#             if abastecimentos.exists():
#                 dados['cards'] = {
#                     'Abastecimentos': abastecimentos.count(),
#                     'KM/L': (abastecimentos.first().quilometragem - abastecimentos.last().quilometragem) / abastecimentos.aggregate(Sum('litros'))['litros__sum'],
#                     'Gastos R$': abastecimentos.aggregate(Sum('valor_total'))['valor_total__sum']
#                 }
                
#                 tipo_combus_total = abastecimentos.values('tipo_combustivel').annotate(total=Count('tipo_combustivel')).order_by('-total')
#                 abast_mes_litros = get_dict_diario(abastecimentos, 'data_abastecimento__day', 'litros')
#                 abast_mes_valor = get_dict_diario(abastecimentos, 'data_abastecimento__day', 'valor_total')

#                 dados['graficos'] = {
#                     'combustivel_usado': {
#                         'labels': json.dumps(list(tipo_combus_total.values_list('tipo_combustivel__tipo', flat=True))),
#                         'data': list(tipo_combus_total.values_list('total', flat=True))
#                     },
#                     'abastecimentos_mes': {
#                         'labels': list(abast_mes_litros.keys()),
#                         'data_litros': list(abast_mes_litros.values()),
#                         'data_valor': list(abast_mes_valor.values())
#                     },
#                 }
#         else:   
#             messages.error(request, form.errors)
#     else:
#         form = RelatorioVeiculoForm()
#     return render(request, 'relatorio_veiculo.html', {'perfil_logado':get_perfil_logado(request),'form':form,'dados':dados})