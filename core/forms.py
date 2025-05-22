import re
from django import forms
from django.forms import TextInput, Select, EmailInput
from django.contrib.auth.hashers import make_password

from .models import (
    Usuario, Rol, NivelEducativo, Grado, Area, Asignatura, Tema, Logro,
    Aula, Grupo, AsignacionDocente, PerfilDeUsuario
)
from django.forms import FileInput

# Formulario de Registro de Usuario
class RegistroUsuarioForm(forms.ModelForm):
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="Debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un símbolo (#$%!)."
    )
    confirmar_password = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput
    )

    class Meta:
        model = Usuario
        fields = ['correo', 'rol', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirmar = cleaned_data.get("confirmar_password")

        if password != confirmar:
            raise forms.ValidationError("⚠️ Las contraseñas no coinciden.")
        if len(password) < 8:
            raise forms.ValidationError("🔒 La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("🔒 La contraseña debe incluir al menos una letra mayúscula.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("🔒 La contraseña debe incluir al menos una letra minúscula.")
        if not re.search(r'\d', password):
            raise forms.ValidationError("🔒 La contraseña debe incluir al menos un número.")
        if not re.search(r'[#\$%!_]', password):
            raise forms.ValidationError("🔒 La contraseña debe incluir al menos un símbolo especial: # $ % ! _")

        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["password"])
        if commit:
            usuario.save()
        return usuario
    
# Formulario para Perfil de Usuario
class PerfilUsuarioForm(forms.ModelForm):
    correo = forms.EmailField(label="Correo electrónico", required=True, disabled=True)
    
    class Meta:
        model = PerfilDeUsuario
        fields = [
            'foto',
            'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'tipo_documento', 'numero_documento',
            'direccion_linea1', 'direccion_linea2', 'ciudad',
            'especialidad', 'grupo', 'acudidos'  # Estos serán filtrados
        ]
        widgets = {
            'foto': FileInput(),
            'primer_nombre': TextInput(),
            'segundo_nombre': TextInput(),
            'primer_apellido': TextInput(),
            'segundo_apellido': TextInput(),
            'tipo_documento': Select(),
            'numero_documento': TextInput(),
            'direccion_linea1': TextInput(),
            'direccion_linea2': TextInput(),
            'ciudad': Select(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Inicializar correo si está presente
        if self.user:
            self.fields['correo'].initial = self.user.correo

        # ---- Filtrar campos por rol ----
        campos_visibles = [
            'foto', 'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido',
            'tipo_documento', 'numero_documento',
            'direccion_linea1', 'direccion_linea2', 'ciudad'
        ]

        if self.user:
            rol = self.user.rol.nombre.strip().lower()
            if rol == 'docente':
                campos_visibles.append('especialidad')
                self.fields['especialidad'].required = True
            elif rol == 'estudiante':
                campos_visibles.append('grupo')
                self.fields['grupo'].required = True
            elif rol in ['acudiente', 'padre de familia o acudiente']:
                campos_visibles.append('acudidos')
                self.fields['acudidos'].required = False
                self.fields['acudidos'].queryset = PerfilDeUsuario.objects.filter(
                    usuario__rol__nombre__iexact='estudiante'
                )

        # Eliminar campos que no deben mostrarse
        for field in list(self.fields):
            if field not in campos_visibles and field != 'correo':
                del self.fields[field]

    def save(self, commit=True):
        perfil = super().save(commit=False)
        if self.user:
            # No se actualiza self.user.correo porque es solo lectura
            if commit:
                self.user.save()
        if commit:
            perfil.save()
            self.save_m2m()
        return perfil



# Formulario de Login de Usuario
class LoginForm(forms.Form):
    correo = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(label="Contraseña", widget=forms.PasswordInput)

# Formulario para Nivel Educativo
class NivelEducativoForm(forms.ModelForm):
    class Meta:
        model = NivelEducativo
        fields = ['nombre']

# Formulario para Grado
class GradoForm(forms.ModelForm):
    class Meta:
        model = Grado
        fields = ['nivel', 'nombre']
        
# Formulario para Aula
class AulaForm(forms.ModelForm):
    class Meta:
        model = Aula
        fields = ['nombre', 'capacidad', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'
            }),
            'estado': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded focus:outline-none focus:ring focus:border-blue-500'
            }),
        }



# Formulario para Grupo
class GrupoForm(forms.ModelForm):
    class Meta:
        model = Grupo
        fields = ['nombre', 'grado', 'aula']

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        grado = cleaned_data.get('grado')
        if Grupo.objects.filter(nombre=nombre, grado=grado).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe un grupo con ese nombre en el mismo grado.")
        return cleaned_data


# Formulario para Asignación de Docente
class AsignacionDocenteForm(forms.ModelForm):
    class Meta:
        model = AsignacionDocente
        fields = ['docente', 'asignatura', 'grupo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar solo usuarios con rol "Docente"
        self.fields['docente'].queryset = Usuario.objects.filter(rol__nombre__iexact='Docente')


# Formulario para Área
class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre', 'obligatoria']

# Formulario para Asignatura
class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ['nombre', 'grado', 'area']

# Formulario para Tema
class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nombre', 'asignatura']

# Formulario para Logro
class LogroForm(forms.ModelForm):
    class Meta:
        model = Logro
        fields = ['descripcion', 'asignatura']
