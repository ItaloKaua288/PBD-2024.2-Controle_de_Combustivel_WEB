from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rolepermissions.decorators import has_role_decorator
from usuarios.models import Usuarios
from .models import Veiculo, Modelo, TipoCombustivel
from .forms import VeiculoForm

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def veiculosView(request):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        context['veiculos'] = Veiculo.objects.filter(placa__icontains=request.POST.get('busca-input'))
        return render(request, 'veiculos.html', context)
    if request.method == 'GET':
        context['veiculos'] = Veiculo.objects.all()
        return render(request, 'veiculos.html', context)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def veiculosCadastrarView(request):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            try:
                veiculo = Veiculo(
                    placa=form.cleaned_data['placa'].strip().upper(),
                    capacidade_tanque=form.cleaned_data['capacidade_tanque'],
                    modelo=get_object_or_404(Modelo, pk=form.cleaned_data['modelo'])
                )
                veiculo.full_clean()
                veiculo.save()
                for tipo in form.cleaned_data['combustivel']:
                    veiculo.tipo_combustivel.add(get_object_or_404(TipoCombustivel, tipo=tipo))
                messages.add_message(request, messages.SUCCESS, 'Veiculo adicionado com sucesso!')
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
        return redirect(reverse('veiculos_cadastrar'))
    if request.method == 'GET':
        context['form'] = VeiculoForm()
        return render(request, 'veiculos_cadastrar.html', context)

@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def veiculosEditarView(request, pk):
    context = {'perfil_logado': Usuarios.objects.get(username=request.user)}
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            try:
                veiculo = get_object_or_404(Veiculo, pk=pk)
                if veiculo.placa != form.cleaned_data['placa'].strip().upper():
                    veiculo.placa=form.cleaned_data['placa'].strip().upper()
                veiculo.capacidade_tanque=form.cleaned_data['capacidade_tanque']
                veiculo.modelo=get_object_or_404(Modelo, pk=form.cleaned_data['modelo'])
                veiculo.full_clean()
                veiculo.save()

                veiculo_combustiveis = veiculo.tipo_combustivel.all()
                for tipo in form.cleaned_data['combustivel']:
                    if not veiculo_combustiveis.filter(tipo=tipo).exists():
                        veiculo.tipo_combustivel.add(get_object_or_404(TipoCombustivel, tipo=tipo))
                for veiculo_combustivel in veiculo_combustiveis:
                    if veiculo_combustivel.tipo not in form.cleaned_data['combustivel']:
                        veiculo.tipo_combustivel.remove(veiculo_combustivel)
                messages.add_message(request, messages.SUCCESS, 'Veiculo adicionado com sucesso!')
            except Exception as e:
                messages.add_message(request, messages.ERROR, e)
        else:
            messages.add_message(request, messages.ERROR, form.errors)
        return redirect(reverse('veiculos'))
    if request.method == 'GET':
        veiculo = get_object_or_404(Veiculo, pk=pk)
        form = VeiculoForm(initial={
            'placa': veiculo.placa,
            'modelo': veiculo.modelo.pk,
            'capacidade_tanque': veiculo.capacidade_tanque,
            'combustivel': list(veiculo.tipo_combustivel.all().values_list('tipo', flat=True)),
        })
        context['form'] = form
        return render(request, 'veiculos_editar.html', context)
    
@login_required(login_url='login')
@has_role_decorator('Administrador', redirect_url=reverse_lazy('login'))
def veiculosDesativarView(request, pk):
    if request.method == 'GET':
        try:
            veiculo = get_object_or_404(Veiculo, pk=pk)
            if veiculo.ativo:
                veiculo.ativo = False
            else:
                veiculo.ativo = True
            veiculo.save()
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)
        else:
            messages.add_message(request, messages.SUCCESS, 'Status alterado com sucesso!')
        return redirect(reverse('veiculos'))