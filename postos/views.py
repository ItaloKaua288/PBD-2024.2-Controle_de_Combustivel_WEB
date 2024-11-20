from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from usuarios.models import Usuarios
from veiculos.models import TipoCombustivel, Veiculo
from .models import Posto, Abastecimento
from .forms import PostoForm, AbastecimentoForm

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def postosView(request):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        context['postos'] = Posto.objects.filter(nome__icontains=request.POST.get('busca-input'))
        return render(request, 'postos.html', context)
    if request.method == 'GET':
        context['postos'] = Posto.objects.all()
        return render(request, 'postos.html', context)
    
@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def postosCadastrarView(request):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        form = PostoForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                posto = Posto(
                    nome=form.cleaned_data['nome'],
                    cnpj=form.cleaned_data['cnpj'],
                )
                posto.full_clean()
                posto.save()
                for tipo in form.cleaned_data['tipos_combustivel']:
                    posto.tipos_combustivel.add(get_object_or_404(TipoCombustivel, tipo=tipo))
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
                return render(request, 'cadastrar.html', context)
            messages.add_message(request, messages.SUCCESS, 'Posto adicionado com sucesso!')
        else:
            return render(request, 'cadastrar.html', context)
        return redirect(reverse('postos_cadastrar'))
    if request.method == 'GET':
        context['form'] = PostoForm()
        return render(request, 'cadastrar.html', context)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def postosEditarView(request, pk):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        form = PostoForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                posto = get_object_or_404(Posto, pk=pk)
                posto.nome=form.cleaned_data['nome']
                posto.cnpj=form.cleaned_data['cnpj']
                posto.full_clean()
                veiculo_combustiveis = posto.tipos_combustivel.all()
                for tipo in form.cleaned_data['tipos_combustivel']:
                    if not veiculo_combustiveis.filter(tipo=tipo).exists():
                        posto.tipos_combustivel.add(get_object_or_404(TipoCombustivel, tipo=tipo))
                for veiculo_combustivel in veiculo_combustiveis:
                    if veiculo_combustivel.tipo not in form.cleaned_data['tipos_combustivel']:
                        posto.tipos_combustivel.remove(veiculo_combustivel)
                posto.save()
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
                return render(request, 'editar.html', context)
            messages.add_message(request, messages.SUCCESS, 'Posto atualizado com sucesso!')
        else:
            return render(request, 'editar.html', context)
        return redirect(reverse('postos_editar', kwargs={'pk': pk}))
    if request.method == 'GET':
        posto = get_object_or_404(Posto, pk=pk)
        form = PostoForm(initial={
            'nome': posto.nome,
            'cnpj': posto.cnpj,
            'tipos_combustivel': [x.tipo for x in posto.tipos_combustivel.all()]
        })
        context['form'] = form
        return render(request, 'editar.html', context)
    
@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def postosDesativarView(request, pk):
    posto = get_object_or_404(Posto, pk=pk)
    try:
        if posto.ativo:
            posto.ativo = False
        else:
            posto.ativo = True
        posto.save()
    except Exception as e:
        messages.add_message(request, messages.ERROR, 'Não foi possivel alterar o status!')
    else:
        messages.add_message(request, messages.SUCCESS, 'Status alterado com sucesso!')
    return redirect(reverse('postos'))

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def abastecimentosView(request):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        data_inicio = request.POST.get('data-inicio') if request.POST.get('data-inicio') else timezone.now()
        data_fim = request.POST.get('data-fim') if request.POST.get('data-fim') else timezone.now()
        if request.POST.get('data-inicio') == '' and request.POST.get('data-fim') == '':
            context['abastecimentos'] = Abastecimento.objects.all()
        else:
            context['abastecimentos'] = Abastecimento.objects.filter(data_abastecimento__range=[data_inicio, data_fim])
        return render(request, 'abastecimentos.html', context)
    if request.method == 'GET':
        context['abastecimentos'] = Abastecimento.objects.all()
        return render(request, 'abastecimentos.html', context)
    
@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def abastecimentosCadastrarView(request):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        form = AbastecimentoForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                abastecimento = Abastecimento(
                    posto=get_object_or_404(Posto, pk=form.cleaned_data['posto']),
                    veiculo=get_object_or_404(Veiculo, pk=form.cleaned_data['veiculo']),
                    tipo_combustivel=get_object_or_404(TipoCombustivel, tipo=form.cleaned_data['tipo_combustivel']),
                    litros=form.cleaned_data['litros'],
                    valor_litro=form.cleaned_data['valor_litro'],
                    valor_total=form.cleaned_data['litros']*form.cleaned_data['valor_litro'],
                    data_abastecimento=form.cleaned_data['data_abastecimento'].strftime('%Y-%m-%d %H:%M:%S')
                )
                abastecimento.full_clean()
                abastecimento.save()
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
                return render(request, 'cadastrar.html', context)
            messages.add_message(request, messages.SUCCESS, 'Abastecimento adicionado com sucesso!')
        else:
            return render(request, 'cadastrar.html', context)
        return redirect(reverse('abastecimentos_cadastrar'))
    if request.method == 'GET':
        context['form'] = AbastecimentoForm()
        return render(request, 'cadastrar.html', context)
    
@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def abastecimentosEditarView(request, pk):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        form = AbastecimentoForm(request.POST)
        context['form'] = form
        if form.is_valid():
            try:
                abastecimento = get_object_or_404(Abastecimento, pk=pk)
                abastecimento.posto=get_object_or_404(Posto, pk=form.cleaned_data['posto'])
                abastecimento.veiculo=get_object_or_404(Veiculo, pk=form.cleaned_data['veiculo'])
                abastecimento.tipo_combustivel=get_object_or_404(TipoCombustivel, tipo=form.cleaned_data['tipo_combustivel'])
                abastecimento.litros=form.cleaned_data['litros']
                abastecimento.valor_litro=form.cleaned_data['valor_litro']
                abastecimento.valor_total=form.cleaned_data['litros']*form.cleaned_data['valor_litro']
                abastecimento.data_abastecimento=form.cleaned_data['data_abastecimento'].strftime('%Y-%m-%d %H:%M:%S')
                abastecimento.full_clean()
                abastecimento.save()
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
                return render(request, 'editar.html', context)
            messages.add_message(request, messages.SUCCESS, 'Abastecimento atualizado com sucesso!')
        else:
            return render(request, 'editar.html', context)
        return redirect(reverse('abastecimentos_editar', kwargs={'pk': pk}))
    if request.method == 'GET':
        abastecimento = get_object_or_404(Abastecimento, pk=pk)
        form = AbastecimentoForm(initial={
            'posto': abastecimento.posto.pk,
            'veiculo': abastecimento.veiculo.pk,
            'tipo_combustivel': abastecimento.tipo_combustivel,
            'litros': abastecimento.litros,
            'valor_litro': abastecimento.valor_litro,
            'data_abastecimento': abastecimento.data_abastecimento.strftime('%Y-%m-%dT%H:%M:%S')
        })
        context['form'] = form
        return render(request, 'editar.html', context)