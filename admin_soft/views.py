import uuid
from collections import defaultdict
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView, PasswordResetConfirmView
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from home.models import UserActivation, Encuesta
from .serializers import UserSerializer  # asegúrate de que tienes este serializador
from .serializers import EncuestaSerializer, EncuestaListSerializer
from admin_soft.forms import RegistrationForm, LoginForm, UserPasswordResetForm, UserSetPasswordForm, \
    UserPasswordChangeForm
from home.models import EncuestaEconomica, PreguntaEconomica, RespuestaUsuario, PreguntaAntropometria, \
    RespuestaNumerica


# Create your views here.

# Pages
def index(request):
    return render(request, 'pages/index.html', {'segment': 'index'})


def billing(request):
    return render(request, 'pages/encuestas.html', {'segment': 'billing'})


def tables(request):
    analisis_estadisticos = ['ANOVA', 'Chi-Cuadrado', 'Correlación', 'Regresión']

    if request.method == 'POST':
        analisis_seleccionado = request.POST.get('analisis_estadistico')
        if analisis_seleccionado == 'ANOVA':
            return redirect('anova')
    return render(request, 'pages/tables.html', {'segment': 'tables', 'analisis_estadisticos': analisis_estadisticos})


# AQUI SE MANEJAN LOS ANALISIS ESTADISTICOS


def anova(request):
    # Diccionario donde almacenaremos las encuestas por cada id_encuesta
    encuestas_por_id_encuesta = defaultdict(list)

    # Obtenemos todas las encuestas
    todas_las_encuestas = Encuesta.objects.all()

    # Agrupamos las encuestas por 'id_encuesta'
    for encuesta in todas_las_encuestas:
        encuestas_por_id_encuesta[encuesta.id_encuesta].append(encuesta)

    # Preparamos los datos para la plantilla
    data = []
    for id_encuesta, encuestas in encuestas_por_id_encuesta.items():
        # Obtenemos los nombres de la encuesta
        nombres_encuesta = [encuesta.name for encuesta in encuestas]

        data.append({
            "id_encuesta": id_encuesta,
            "nombres_encuesta": nombres_encuesta,
        })

    return render(request, "pages/resultadoANOVA.html", {"id_encuestas": data})





def vr(request):
    return render(request, 'pages/virtual-reality.html', {'segment': 'vr'})


def rtl(request):
    return render(request, 'pages/rtl.html', {'segment': 'rtl'})


def profile(request):
    return render(request, 'pages/profile.html', {'segment': 'profile'})


# Authentication
class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = self.request.POST['username']
        user = User.objects.get(username=username)
        if UserActivation.objects.filter(user=user).exists():
            user_activation = UserActivation.objects.get(user=user)
            if user_activation.created_through_api:
                return HttpResponse("Este usuario no tiene permisos para la interfaz web.")
        else:
            return super().form_valid(form)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Account created successfully!')
            return redirect('/accounts/login/')
        else:
            print("Register failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


class UserPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm


def encuestas_view(request):
    encuestas = EncuestaEconomica.objects.all()
    usuarios = User.objects.annotate(num_encuestas=Count('respuestausuario__sesion_encuesta', distinct=True))
    return render(request, 'pages/encuestas.html', {'encuestas': encuestas, 'usuarios': usuarios})


def seleccionar_grupo(request, encuesta_id):
    encuesta = get_object_or_404(EncuestaEconomica, id=encuesta_id)
    grupos = PreguntaAntropometria.objects.filter(encuesta=encuesta).values_list('grupo_poblacional',
                                                                                 flat=True).distinct()
    if request.method == 'POST':
        request.session['grupo_poblacional'] = request.POST['grupo_poblacional']
        return redirect('realizar_encuesta', encuesta_id=encuesta.id)

    return render(request, 'pages/seleccionar_grupo.html', {'grupos': grupos, 'encuesta': encuesta})


def realizar_encuesta(request, encuesta_id):
    encuesta = get_object_or_404(EncuestaEconomica, id=encuesta_id)

    if PreguntaAntropometria.objects.filter(encuesta=encuesta).exists():
        grupo_poblacional = request.session.get('grupo_poblacional')
        if not grupo_poblacional:
            return redirect('seleccionar_grupo', encuesta_id=encuesta.id)

        preguntas = PreguntaAntropometria.objects.filter(encuesta=encuesta, grupo_poblacional=grupo_poblacional)
        ModeloRespuesta = RespuestaNumerica
    else:
        preguntas = PreguntaEconomica.objects.filter(encuesta=encuesta)
        ModeloRespuesta = RespuestaUsuario

    if request.method == 'POST':
        if request.user.is_authenticated:
            sesion_encuesta = uuid.uuid4().hex
            for pregunta in preguntas:
                if isinstance(pregunta, PreguntaAntropometria):
                    respuesta_numerica = request.POST[str(pregunta.id)]
                    RespuestaNumerica.objects.create(
                        usuario=request.user,
                        encuesta=encuesta,
                        pregunta=pregunta,
                        respuesta_numerica=respuesta_numerica,  # Use respuesta_numerica for RespuestaNumerica
                        sesion_encuesta=sesion_encuesta,
                    )
                else:  # PreguntaEconomica
                    respuesta_id = request.POST[str(pregunta.id)]
                    RespuestaUsuario.objects.create(
                        usuario=request.user,
                        encuesta=encuesta,
                        pregunta=pregunta,
                        respuesta_id=int(respuesta_id),
                        sesion_encuesta=sesion_encuesta,
                    )
            del request.session['grupo_poblacional']
            return redirect('pages/encuestas.html')
        else:
            return redirect('../../templates/accounts/login.html')
    else:
        rangos = list(range(251))
        return render(request, 'pages/realizar_encuesta.html',
                      {'encuesta': encuesta, 'preguntas': preguntas, 'rangos': rangos})





class EncuestaView(APIView): #Vista para consumir DATOS DE ENTRADA DE ENCUESTAS
    def post(self, request, format=None):
      #  print(f"Data received in post: {request.data}")
        serializer = EncuestaListSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView): #VISTA PARA REGISTRO DESDE APLICACION
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)

            UserActivation.objects.create(user=user, created_through_api=True)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateView(APIView): #VISTA PARA ACTIVACION DE CUENTA api
    def post(self, request, username):
        activation = UserActivation.objects.get(user__username=username)
        if not activation.is_activated:
            activation.is_activated = True
            activation.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

def inactive_users(request): #VISTA ACTIVACION USUARIOS DESDE PANELL
    if request.user.is_authenticated:
        inactive_users = User.objects.filter(useractivation__is_activated=False)
        return render(request, 'pages/inactive_users.html', {"users": inactive_users})
    else:
        return HttpResponse("Inicie sesión para poder visualizar esta página.")

def activate_user(request, username): #VISTA PARA PODER ACTIVAR EL USUARIO
    if request.user.is_authenticated:
        user_activation = UserActivation.objects.get(user__username=username)
        user_activation.is_activated = True
        user_activation.save()
        return HttpResponse("El usuario ha sido activado correctamente.")
    else:
        return HttpResponse("No tiene permisos suficientes.")


def encuestadores(request):
    if request.user.is_authenticated:
        user_activations = UserActivation.objects.filter(created_through_api=True)
        encuestadores = User.objects.filter(useractivation__in=user_activations).annotate(num_encuestas=Count('encuesta'))
        return render(request, 'pages/encuestadores.html',{"encuestadores":encuestadores})
    else:
        return HttpResponse("Inicie sesión para poder visualizar esta página.")