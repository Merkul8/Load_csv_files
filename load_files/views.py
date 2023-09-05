from typing import Any, Dict
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from . models import CSVFile, FileColumn
from . forms import LoadFile, UserLoginForm, UserRegisterForm
from django.views.generic import ListView, FormView
import csv
import chardet
from django.contrib.auth import logout, login
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'load_files/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Успешная регистрация')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'load_files/register.html', {'form': form})


class LoadFileView(FormView):
    template_name = 'load_files/load_file.html'  
    form_class = LoadFile  
    success_url = reverse_lazy('home')

    def detect_file_encoding(self, file):
        # Определяем кодировку файла
        detector = chardet.universaldetector.UniversalDetector()
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']

    def form_valid(self, form):
        csv_file = CSVFile.objects.create(**form.cleaned_data)

        file_encoding = self.detect_file_encoding(csv_file.csv_file)
        csv_file.csv_file.seek(0)  
        csv_data = csv_file.csv_file.read().decode(file_encoding)
        csvreader = csv.reader(csv_data.splitlines())

        headers = next(csvreader)
        headers_res = headers[0].split(';')

        # Создаем объекты FileColumn на основе заголовков
        for head in headers_res:
            if head:
                FileColumn.objects.create(uploaded_file=csv_file, column_name=head)
            
        return super().form_valid(form)
    

class Home(ListView):
    model = CSVFile
    template_name = 'load_files/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['headers'] = FileColumn.objects.all()
        return context

