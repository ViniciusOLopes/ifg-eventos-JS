from django.db import models

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
    TO DO: Incluir informações do maps.
    """

    def __str__(self):
        return super().__str__()


class Student(models.Model):
    """
    Cria a identidade dos alunos.
    """
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

    def __str__(self):
        return f"(Nome: {self.student.name}, Matricula: {self.student.id})"


