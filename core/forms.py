import re
from django import forms
from django.forms import TextInput, Select, EmailInput, FileInput
from django.contrib.auth.hashers import make_password

from .models import (
    Usuario, Rol, TipoDocumento,
    NivelEducativo, Grado, Area, Asignatura, Tema, Logro,
    Aula, Grupo, AsignacionDocente, Ciudad,
    PerfilDeUsuario, HojaDeVidaDocente, EducacionDocente, CapacitacionDocente, IdiomaDocente, ExperienciaDocente
)




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
        fields = ['correo', 'rol', 'tipo_documento', 'numero_documento', 'password']
        widgets = {
            'tipo_documento': forms.Select(attrs={'class': 'w-full p-2 border rounded'}),
            'numero_documento': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
        }

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
        usuario.is_active = False  # Por si se te olvida en algún punto
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
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2 mt-1',
            'placeholder': 'Tu usuario'
        })
    )
    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2 mt-1',
            'placeholder': 'Tu contraseña'
        })
    )

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

# Hoja de Vida Docentes
class DatosBasicosDocenteForm(forms.ModelForm):
    class Meta:
        model = HojaDeVidaDocente
        exclude = ['usuario']  # Usuario se asigna en la vista

        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'genero': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'estado_civil': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'pais_residencia': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'departamento_residencia': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'municipio_residencia': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'direccion_linea1': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'direccion_linea2': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'estrato': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'telefono_celular': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'telefono_celular_alterno': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'telefono_fijo': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'telefono_fijo_ext': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'correo_alterno': forms.EmailInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'resumen': forms.Textarea(attrs={
                'rows': 4,
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
        }

# Identificaci♀n Formulario
class IdentificacionForm(forms.ModelForm):
    municipio_identificacion = forms.ModelChoiceField(
        queryset=Ciudad.objects.all(),
        label="Municipio de Identificación",
        required=False,  # MUY IMPORTANTE
        widget=forms.Select(attrs={
            'class': 'w-full border border-gray-300 rounded px-3 py-2'
        })
    )


    class Meta:
        model = Usuario
        fields = ['tipo_documento', 'numero_documento']  # 👈 Solo campos del modelo
        widgets = {
            'tipo_documento': forms.Select(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'numero_documento': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
        }

        
# Identidad Form
class IdentidadForm(forms.ModelForm):
    class Meta:
        model = PerfilDeUsuario
        fields = ['primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido']
        widgets = {
            'primer_nombre': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'segundo_nombre': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'primer_apellido': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'segundo_apellido': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
        }

class EducacionDocenteForm(forms.ModelForm):
    class Meta:
        model = EducacionDocente
        fields = '__all__'

class CapacitacionDocenteForm(forms.ModelForm):
    class Meta:
        model = CapacitacionDocente
        fields = '__all__'

class IdiomaDocenteForm(forms.ModelForm):
    class Meta:
        model = IdiomaDocente
        fields = '__all__'

class ExperienciaDocenteForm(forms.ModelForm):
    class Meta:
        model = ExperienciaDocente
        fields = '__all__' 
        
