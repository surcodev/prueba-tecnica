from django.db import models
from django.contrib.auth.models import AbstractUser

# Roles de usuario
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('agente', 'Agente'),
        ('cliente', 'Cliente'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='cliente')
    
    # Usar el email como campo de autenticación
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # El campo email será usado como el nombre de usuario
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'Usuario'

    def __str__(self):
        return self.email

# Modelo de Proyecto
class Proyecto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    class Meta:
        db_table = 'Proyecto'

    def __str__(self):
        return self.nombre

# Modelo de Cita
class Cita(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('completado', 'Completado'),
        ('reabierto', 'Reabierto'),
    ]

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_asignacion = models.DateTimeField(null=True, blank=True)
    fecha_cerrado = models.DateTimeField(null=True, blank=True)
    consulta = models.TextField()
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='citas_cliente')
    agente = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='citas_agente')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')

    class Meta:
        db_table = 'Cita'

    def __str__(self):
        return f"Cita de {self.cliente.username} sobre {self.proyecto.nombre}"
