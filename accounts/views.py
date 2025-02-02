from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # Перенаправление после успешной регистрации
    template_name = 'registration/signup.html'  # Путь к шаблону