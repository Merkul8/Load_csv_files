from django.db import models


class FileColumn(models.Model):
    uploaded_file = models.ForeignKey('CSVFile', on_delete=models.CASCADE, verbose_name='Название файла')
    column_name = models.CharField(max_length=255, verbose_name='Имя колонки')

    def __str__(self):
        return self.column_name
    
    class Meta:
        verbose_name = 'Колонка файла'
        verbose_name_plural = 'Колонки файлов'


class CSVFile(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название файла')
    csv_file = models.FileField(upload_to='csv_files/', verbose_name='Файл')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
