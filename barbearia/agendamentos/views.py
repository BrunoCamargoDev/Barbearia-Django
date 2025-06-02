from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from .models import Cliente, Servico, agendamento
from django.contrib import messages

# Função para os clientes agendarem seu horário
def agendar(request):
    servicos = Servico.objects.all()

    if request.method == 'POST':
        nome = request.POST['nome']
        telefone = request.POST['telefone']
        servico_id = request.POST['servico']
        data = request.POST['data']
        hora = request.POST['hora']

        # Verificar se hora termina em :00
        hora_minuto = hora.split(':')[1]
        if hora_minuto != '00':
            messages.error(request, 'Os agendamentos só podem ser feitos de hora em hora (ex: 13:00, 14:00).')
            return render(request, 'agendamentos/agendar.html', {'servicos': servicos})

        cliente = Cliente.objects.create(nome=nome, telefone=telefone)
        servico = Servico.objects.get(id=servico_id)

        agendamento.objects.create(cliente=cliente, servico=servico, data=data, hora=hora)

        messages.success(request, 'Agendamento realizado com sucesso!')
        return redirect('agendar')

    return render(request, 'agendamentos/agendar.html', {'servicos': servicos})


# Função para o dono verificar os agendamentos
@login_required(login_url='login')
def listar_agendamentos(request):
    agendamentos = agendamento.objects.all().order_by('-data', '-hora')
    return render(request, 'agendamentos/listar_agendamentos.html', {'agendamentos': agendamentos})


# Função de login (Somente o dono acessar)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        senha = request.POST['senha']
        user = authenticate(request, username=username, password=senha)
        if user:
            login(request, user)
            return redirect('listar_agendamentos')
        else:
            return render(request, 'agendamentos/login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'agendamentos/login.html')


# Função logout
def logout_view(request):
    logout(request)
    return redirect('login')
