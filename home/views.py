from django.shortcuts import render
from django.views.generic import View
from django.db.models import Sum
from veiculos.models import Veiculo
from postos.models import Abastecimento
from django.utils import timezone

class home_view(View):
    template_name = 'home.html'
    
    def get(self, request):
        context = {}
        abastecimentos = Abastecimento.objects.filter(data_abastecimento__month=timezone.now().month)
        context["cards"] = {
            'num_veiculos': Veiculo.objects.filter(ativo=True).count(),
            'valor_gasto': abastecimentos.aggregate(Sum('valor_total'))['valor_total__sum'],
            'litros': abastecimentos.aggregate(Sum('litros'))['litros__sum']
        }
        return render(request, self.template_name, context)