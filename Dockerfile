FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar todo el código de la aplicación al contenedor
COPY . /app/

# Añadir un usuario para ejecutar el contenedor de forma segura
RUN adduser --disabled-password django-user

# Establecer las variables de entorno necesarias
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalar dependencias necesarias para PostgreSQL y Django REST Framework
RUN apt-get update && \
    apt-get install -y libpq-dev gcc && \
    pip install psycopg2 psycopg2-binary requests Django djangorestframework 

# Cambiar el propietario de los archivos al usuario no root
RUN chown -R django-user /app

# Cambiar a ese usuario no root
USER django-user

# Exponer el puerto en el que correrá la aplicación
EXPOSE 8000

# Correr las migraciones y el servidor de desarrollo de Django
CMD ["sh", "-c", "python manage.py && python manage.py makemigrations vulnerabilities && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
