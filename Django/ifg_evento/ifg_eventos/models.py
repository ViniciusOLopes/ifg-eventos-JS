from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    """
    Cria os eventos
    """
    name = models.CharField(max_length=60)
    description = models.TextField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    date_added = models.DateTimeField(auto_now_add=True)
    max_registration = models.IntegerField(default=1)
    """
    Informações necessarias para o mapa.
    """
    local = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True) 

    def __str__(self):
        return self.name


class Student(models.Model):
    """
    Cria a identidade dos alunos.
    """
    user = models.OneToOneField(
         User,
         on_delete=models.CASCADE,
         related_name='student'

    )
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, verbose_name="E-mail")
    cpf = models.CharField(max_length=14, verbose_name="CPF", null=True)
    cellphone = models.CharField(max_length=15, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f"(Nome: {self.name}, Matricula: {self.id})"


class Registration(models.Model):
    """
    Cria as inscrições dos alunos nos eventos.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    class Meta:
            constraints = [
            models.UniqueConstraint(
                fields=['student', 'event'],
                name='unique_student_event'
            )
        ]

    def __str__(self):
        return f"(Nome: {self.student.name}, Matricula: {self.student.id})"


