import uuid
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.conf import settings
from .forms import InscripcionTallerForm

def login_cliente(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            login(request, user)
            # Verificamos si es administrador o personal autorizado
            if user.is_staff or user.is_superuser:
                return redirect('administrador:index')
            else:
                # Si es un cliente/usuario normal, va al catálogo de clientes
                return redirect('clientes:index')
        else:
            return render(request, 'clientes/login.html', {'error': 'Usuario o contraseña incorrectos'})
            
    return render(request, 'clientes/login.html')

def index_clientes(request):
    # Vista principal del catálogo para clientes
    return render(request, 'clientes/index.html')

def inscribir_taller(request):
    if request.method == 'POST':
        form = InscripcionTallerForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            # Generamos un código de cupón único de 8 caracteres en mayúsculas
            inscripcion.cupon = str(uuid.uuid4())[:8].upper()
            inscripcion.save()
            
            # Preparamos el correo electrónico con los datos personales
            asunto = f"Cupón de acceso para el taller: {inscripcion.taller}"
            mensaje = (
                f"Hola {inscripcion.nombre_completo},\n\n"
                f"Te has inscripto correctamente al taller '{inscripcion.taller}'.\n"
                f"Recuerda que el acceso es gratuito a cambio de tu donación de un alimento no perecedero ({inscripcion.alimento_donado}).\n\n"
                f"Tu número de cupón personal para ingresar es: {inscripcion.cupon}\n\n"
                f"¡Te esperamos en la biblioteca!"
            )
            remitente = settings.EMAIL_HOST_USER
            destinatario = [inscripcion.email]
            
            try:
                send_mail(asunto, mensaje, remitente, destinatario)
            except Exception as e:
                print(f"Error al enviar correo: {e}")
                
            return render(request, 'clientes/exito_inscripcion.html', {'inscripcion': inscripcion})
    else:
        form = InscripcionTallerForm()
        
    return render(request, 'clientes/inscribir_taller.html', {'form': form})