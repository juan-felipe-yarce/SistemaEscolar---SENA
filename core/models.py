from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.utils import timezone

# ────────────────────────────────
# TABLAS PARAMÉTRICAS
# ────────────────────────────────

class Rol(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Rol"
        verbose_name_plural = "Roles"

    def __str__(self):
        return self.nombre

class TipoDocumento(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        verbose_name = "Tipo de Documento"
        verbose_name_plural = "Tipos de Documento"

    def __str__(self):
        return self.nombre
    
class Pais(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    codigo_iso = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return self.nombre

class Departamento(models.Model):
    pais = models.ForeignKey(Pais, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Departamento"
        verbose_name_plural = "Departamentos"

    def __str__(self):
        return self.nombre


class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ciudad"
        verbose_name_plural = "Ciudades"

    def __str__(self):
        return f"{self.nombre} ({self.departamento.nombre})"

# ────────────────────────────────
# CLASE BASE PERSONA
# ────────────────────────────────

class Persona(models.Model):
    primer_nombre = models.CharField(max_length=50)
    segundo_nombre = models.CharField(max_length=50, blank=True, null=True)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    direccion_linea1 = models.CharField(max_length=100)
    direccion_linea2 = models.CharField(max_length=100, blank=True, null=True)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.PROTECT)

    class Meta:
        abstract = True

# ────────────────────────────────
# USUARIO PERSONALIZADO
# ────────────────────────────────

class UsuarioManager(BaseUserManager):
    def create_user(self, correo, password=None, **extra_fields):
        if not correo:
            raise ValueError('El correo electrónico es obligatorio')
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(correo, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    correo = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)

    tipo_documento = models.ForeignKey(TipoDocumento, on_delete=models.PROTECT, null=True)
    numero_documento = models.CharField(max_length=20, unique=True, null=True)

    fecha_creacion = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=False)  # La cuenta queda inactiva hasta validación
    is_staff = models.BooleanField(default=False)

    groups = models.ManyToManyField(Group, blank=True, related_name='usuario_set')
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name='usuario_set')

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = []

    objects = UsuarioManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.correo


# ────────────────────────────────
# PERFIL DE USUARIO
# ────────────────────────────────

class PerfilDeUsuario(Persona):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil")
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    grupo = models.ForeignKey('Grupo', on_delete=models.SET_NULL, null=True, blank=True)
    acudidos = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='acudientes',
        through='RelacionAcudienteEstudiante',
        through_fields=('acudiente', 'estudiante'),
        blank=True
    )
    foto = models.ImageField(upload_to='avatares/', blank=True, null=True)  # 👈 Nuevo campo

    class Meta:
        verbose_name = "Perfil de Usuario"
        verbose_name_plural = "Perfiles de Usuario"


class RelacionAcudienteEstudiante(models.Model):
    acudiente = models.ForeignKey('PerfilDeUsuario', on_delete=models.CASCADE, related_name='acudidos_asociados')
    estudiante = models.ForeignKey('PerfilDeUsuario', on_delete=models.CASCADE, related_name='acudientes_asociados')

    class Meta:
        unique_together = ('acudiente', 'estudiante')

# ────────────────────────────────
# ESTRUCTURA ACADÉMICA
# ────────────────────────────────

class NivelEducativo(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

class Grado(models.Model):
    nivel = models.ForeignKey(NivelEducativo, on_delete=models.CASCADE, related_name="grados")
    nombre = models.CharField(max_length=10)

    class Meta:
        unique_together = ('nivel', 'nombre')

    def __str__(self):
        return f"{self.nivel.nombre} - {self.nombre}"

class Area(models.Model):
    nombre = models.CharField(max_length=100)
    obligatoria = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Asignatura(models.Model):
    nombre = models.CharField(max_length=100)
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="asignaturas")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="asignaturas")

    class Meta:
        unique_together = ('nombre', 'grado', 'area')

    def __str__(self):
        return self.nombre

class Tema(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name="temas")
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.asignatura.nombre})"

class Logro(models.Model):
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name="logros")
    descripcion = models.TextField(unique=True)

    def __str__(self):
        return f"Logro: {self.descripcion[:30]}..."

class Aula(models.Model):
    ESTADOS = [
        ('Disponible', 'Disponible'),
        ('Ocupada', 'Ocupada'),
        ('Mantenimiento', 'Mantenimiento')
    ]
    nombre = models.CharField(max_length=50)
    capacidad = models.PositiveIntegerField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Disponible')

    def __str__(self):
        return self.nombre

class Grupo(models.Model):
    grado = models.ForeignKey(Grado, on_delete=models.CASCADE, related_name="grupos")
    nombre = models.CharField(max_length=10)
    aula = models.ForeignKey(Aula, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nombre} ({self.grado})"

class AsignacionDocente(models.Model):
    docente = models.ForeignKey(
        Usuario,
        limit_choices_to={'rol__nombre': 'Docente'},
        on_delete=models.CASCADE
    )
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('docente', 'grupo', 'asignatura')

class Actividad(models.Model):
    asignacion = models.ForeignKey(AsignacionDocente, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    es_calificable = models.BooleanField(default=True)
    fecha_publicacion = models.DateField(auto_now_add=True)

class Calificacion(models.Model):
    actividad = models.ForeignKey(Actividad, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(
        Usuario,
        limit_choices_to={'rol__nombre': 'Estudiante'},
        on_delete=models.CASCADE
    )
    nota = models.DecimalField(max_digits=3, decimal_places=1)
    fecha_registro = models.DateField(auto_now_add=True)
