from django.shortcuts import render
from AppCoder.models import Curso, Profesor, Estudiante, Entregable,Avatar
from django.http import HttpResponse, HttpResponseRedirect
from AppCoder.forms import CursoFormulario, ProfesorFormulario, EstudiantesFormulario, EntregableFormulario, UserRegisterForm,AvatarFormulario
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, login
from AppCoder.forms import User, UserRegisterForm, UserEditForm, CursoFormulario, ProfesorFormulario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
# Create your views here.

url = ''
@login_required
def inicio(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    return render(request, 'inicio.html', {'url': avatares[0].imagen.url})

@login_required
def cursos(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    
    if request.method == 'POST':
        miFormulario = CursoFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid:
            
            informacion = miFormulario.cleaned_data

            curso=Curso(nombre=informacion['nombre'], camada=informacion['camada'])
            curso.save()

            return render(request, 'inicio.html',)

    else: 
        miFormulario = CursoFormulario()

    return render(request, "cursos.html", {'miFormulario':miFormulario})

@login_required
def profesores(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    
    if request.method == 'POST':
        miFormulario = ProfesorFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid:
            
            informacion = miFormulario.cleaned_data

            profesor=Profesor(nombre=informacion['nombre'], 
                              apellido=informacion['apellido'], 
                              email=informacion['email'], 
                              profesion=informacion['profesion'])
            profesor.save()

            return render(request, 'inicio.html')

    else: 
        miFormulario = ProfesorFormulario()

    return render(request, "Profesores.html", {'miFormulario':miFormulario})
def busquedaCamada(request):
    return render(request, 'inicio.html')
def buscar(request):
    if request.GET['camada']:
        camada = request.GET['camada']
        curso = Curso.objects.filter(camada__icontains=camada)

        return render(request, 'inicio.html', {"cursos":curso, "camada":camada})
    
    else:
        respuesta = 'No enviaste Datos'

    #return HttpResponse(respuesta)
    return render(request, 'inicio.html', {"respuesta":respuesta}) 

@login_required
def estudiantes(request):
    avatares = Avatar.objects.filter(user=request.user.id)
    
    if request.method == 'POST':
        miFormulario = EstudiantesFormulario(request.POST)

        print(miFormulario)

        if miFormulario.is_valid:
            
            informacion = miFormulario.cleaned_data

            estudiante=Estudiante(nombre=informacion['nombre'],
                                  apellido=informacion['apellido'],
                                  email=informacion['email'])
            estudiante.save()

            return render(request, 'inicio.html')

    else: 
        miFormulario = EstudiantesFormulario()

    return render(request, "estudiantes.html", {'miFormulario':miFormulario,})

@login_required
def entregables(request):
    avatares = Avatar.objects.filter(user=request.user.id)

    if request.method == 'POST':
        miFormulario = EntregableFormulario(request.POST, request.FILES)

        print(miFormulario)

        if miFormulario.is_valid:
            
            informacion = miFormulario.cleaned_data

            entregable= Entregable(nombre=informacion['nombre'],
                                  fecha_de_Entrega=informacion['fecha_De_Entrega'],
                                  entregado=informacion['entregado'],
                                  imagen=informacion['imagen'])
            entregable.save()

            return render(request, 'inicio.html')

    else: 
        miFormulario = EntregableFormulario()

    return render(request, "entregables.html", {'miFormulario':miFormulario,})

@login_required
def editarPerfil(request):
    usuario = request.user
    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data
            usuario.email = informacion['email']
            usuario.first_name = informacion['first_name']
            usuario.last_name = informacion['last_name']
            if informacion['password1'] == informacion['password2']:
                usuario.password = make_password(informacion['password1'])
                usuario.save()
            else:
                return render(request, 'inicio.html', {'mensaje':'Contrasena incorrecta'})


            return render(request, 'inicio.html')
    else:
        miFormulario = UserEditForm(initial={'email':usuario.email})


    return render(request, "editarPerfil.html", {"miFormulario":miFormulario, "usuario":usuario})

@login_required
def agregarAvatar(request):
      if request.method == 'POST':

            miFormulario = AvatarFormulario(request.POST, request.FILES) #aquí mellega toda la información del html

            if miFormulario.is_valid():   #Si pasó la validación de Django


                  u = User.objects.get(username=request.user)
                
                  avatar = Avatar (user=u, imagen=miFormulario.cleaned_data['image']) 
      
                  avatar.save()

                  return render(request, "inicio.html") #Vuelvo al inicio o a donde quieran

      else: 

            miFormulario= AvatarFormulario() #Formulario vacio para construir el html

      return render(request, "agregarAvatar.html", {"miFormulario":miFormulario})
'''
def leerEntregables(request):
    entregables = Entregable.objects.all()
    contexto = {'entregables':entregables}
    return render(request, "leerEntregables.html", contexto)

def eliminarEntregable(request, entregable_nombre):
    entregable = Entregable.objects.get(nombre=entregable_nombre)
    entregable.delete()

    entregables = Entregable.objects.all()
    contexto = {"Entregables":entregables}
    return render(request, "leerEntregables.html", contexto)

def editarEntregable(request,entregable_nombre):
    entregable = Entregable.objects.get(nombre=entregable_nombre)
    if request.method == "POST":
        miFormulario = EntregableFormulario(request.POST)
        print(miFormulario)

        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data

            entregable.nombre = informacion['nombre']
            entregable.fecha_de_Entrega = informacion['fecha_de_Entrega']
            entregable.entregado = informacion['entregado']
            entregable.imagen = informacion['imagen']

            entregable.save()
            return render(request, "inicio.html")
    else:
        miFormulario = EntregableFormulario(initial={'nombre':entregable.nombre, 
                                                     'fecha_de_Entrega': entregable.fecha_de_Entrega, 
                                                     'entregado': entregable.entregado, 
                                                     'imagen': entregable.imagen})
        return render(request, "editarEntregable.html", {'miFormulario': miFormulario, "entregable_nombre":entregable_nombre})    
'''
def proximamente(request):
    return render(request, 'proximamente.html')

class CursoList(ListView):
    model = Curso
    template_name = "curso_list.html"

class CursoDetalle(DetailView):
    model = Curso
    template_name = "curso_detalle.html"

class CursoCreacion(CreateView):
    model = Curso
    template_name = "curso_form.html"
    success_url = reverse_lazy("AppCoder:List")
    fields = ['nombre', 'camada']

class CursoUpdate(UpdateView):
    model = Curso
    success_url = "/appcoder1/curso/list"
    template_name = "curso_form.html"
    fields = ['nombre', 'camada']

class CursoDelete(DeleteView):
    model = Curso
    template_name = "curso_confirm_delete.html"
    success_url = "/appcoder1/curso/list"


class EntregableLista(ListView):   
    model = Entregable
    template_name = "entregable_lista.html"

class EntregableDetail(DetailView):
    model = Entregable
    template_name = "entregable_detail.html"

class EntregableCreation(CreateView):
    model = Entregable
    template_name = "entregable_creation.html"
    success_url = reverse_lazy("AppCoder:Lista")
    fields = ['nombre', 'fecha_de_Entrega', 'entregado', 'imagen']

class EntregableUpdate(UpdateView):
    model = Entregable
    success_url = "/appcoder1/entregables/lista"   
    template_name = "entregable_form.html"
    fields = ['nombre', 'fecha_de_Entrega', 'entregado', 'imagen']

class EntregableDelete(DeleteView):
    model = Entregable
    template_name = "entregable_confirm.delete.html"
    success_url = "/appcoder1/entregables/lista"

    
@login_required
def aboutus(request):
    return render(request, 'aboutus.html')