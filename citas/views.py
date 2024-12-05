from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Proyecto, Cita
from django.utils import timezone
from django.http import JsonResponse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from django.contrib import messages
import json

def index(request):
    return render(request, 'index.html')

# Vista para el panel de cliente
@login_required
def panel_cliente(request):
    # Filtrar las citas correspondientes al cliente autenticado
    citas = Cita.objects.filter(cliente=request.user).order_by('-fecha_creacion')
    return render(request, 'panel_cliente.html', {'citas': citas})

# Vista para el panel de agente
@login_required
def panel_agente(request):
    # Filtrar las citas asignadas al agente autenticado
    citas = Cita.objects.filter(agente=request.user).order_by('-fecha_creacion')
    return render(request, 'panel_agente.html', {'citas': citas})

# Vista para el panel de agente
@login_required
def panel_admin(request):
    # Obtener todas las citas y agentes
    citas = Cita.objects.all().order_by('-fecha_creacion')
    agentes = CustomUser.objects.filter(role='agente')  # Filtrar usuarios con rol de agente

    # Renderizar la plantilla con las citas y agentes
    return render(request, 'panel_admin.html', {'citas': citas, 'agentes': agentes})

######################################################################################################

# Vista de Cierre de Sesión
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión

def login_view(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'cliente':
                return redirect('panel_cliente')  # Redirigir al panel de cliente
            elif user.role == 'agente':
                return redirect('panel_agente')  # Redirigir al panel de agente
            elif user.role == 'admin':
                return redirect('panel_admin')
            else:
                return redirect('index')  # Redirigir al home si no es ni cliente ni agente
        else:
            return render(request, 'index.html', {'error': 'Credenciales incorrectas'})

    return render(request, 'index.html')

@login_required
def crear_cita(request):
    if request.method == 'POST':
        proyecto_id = request.POST.get('proyecto')
        consulta = request.POST.get('consulta')

        proyecto = Proyecto.objects.get(id=proyecto_id)

        # Crear una nueva cita
        cita = Cita(
            proyecto=proyecto,
            cliente=request.user,  # Usuario autenticado
            consulta=consulta,
            fecha_creacion=timezone.now(),  # Fecha de creación automática
        )
        cita.save()

        # Redirigir al usuario a su panel
        return redirect('panel_cliente')
    
    # Si la solicitud es GET, pasar los proyectos para mostrar el formulario
    proyectos = Proyecto.objects.all()
    return render(request, 'consulta.html', {'proyectos': proyectos})


# Vista para actualizar el estado de la cita
login_required
def actualizar_estado_cita(request):
    if request.method == 'POST':
        cita_id = request.POST.get('cita_id')
        nuevo_estado = request.POST.get('estado')

        try:
            cita = Cita.objects.get(id=cita_id, agente=request.user)
            cita.estado = nuevo_estado

            # Si el estado es "completado", actualizar la fecha_cerrado
            if nuevo_estado == 'completado':
                cita.fecha_cerrado = now()
            else:
                cita.fecha_cerrado = None

            cita.save()
            return JsonResponse({'success': True, 'message': 'Estado actualizado correctamente'})
        except Cita.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cita no encontrada'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})


@csrf_exempt
@login_required
def asignar_agente(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cita_id = data.get('cita_id')
        agente_id = data.get('agente_id')

        try:
            cita = Cita.objects.get(id=cita_id)
            agente = CustomUser.objects.get(id=agente_id, role='agente')

            cita.agente = agente
            cita.fecha_asignacion = now()  # Registrar la fecha de asignación
            cita.save()

            return JsonResponse({'success': True, 'message': 'Agente asignado correctamente.'})
        except (Cita.DoesNotExist, CustomUser.DoesNotExist):
            return JsonResponse({'success': False, 'message': 'Cita o agente no encontrado.'})
    return JsonResponse({'success': False, 'message': 'Método no permitido.'})


def registro_cliente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')

        # Validaciones básicas
        if not all([email, password, first_name, last_name, username]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect('registro_cliente')

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return redirect('registro_cliente')

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "El correo electrónico ya está registrado.")
            return redirect('registro_cliente')

        # Crear usuario con rol de cliente
        usuario = CustomUser.objects.create(
            email=email,
            password=make_password(password),
            first_name=first_name,
            last_name=last_name,
            username=username,
            role='cliente'  # Especificar el rol
        )
        usuario.save()

        messages.success(request, "Cuenta creada exitosamente. Inicia sesión.")
        return redirect('login')

    return render(request, 'registro_cliente.html')


def registro_agente(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')

        # Crear el usuario con el rol de agente
        agente = CustomUser.objects.create(
            email=email,
            password=make_password(password),  # Hashear la contraseña
            first_name=first_name,
            last_name=last_name,
            username=username,
            role='agente'  # Asignar el rol de agente
        )
        agente.save()

        # Redirigir después del registro exitoso
        return redirect('login')

    return render(request, 'registro_agente.html')
