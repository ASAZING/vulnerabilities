# Vulnerability Management API

Este proyecto es una API REST para gestionar vulnerabilidades, combinando datos obtenidos de la National Vulnerability Database (NVD) con vulnerabilidades almacenadas localmente. La API permite obtener, marcar como fixeadas, y excluir vulnerabilidades, así como obtener información sumarizada por severidad.

## Requisitos

- Python 3.8+
- Django 4.0+
- Django REST Framework
- PostgreSQL (opcional, pero recomendado para producción)
- Docker

## Instalación

1. **Clonar el Repositorio**

```bash
   https://github.com/ASAZING/vulnerabilities.git
   cd vulnerabilities
```
2. **Crear Migraciones**
```bash
   python manage.py makemigrations vulnerabilities && python manage.py migrate
```
3. **Ejecutar docker**
```bash
   docker compose up -d --build
```

Listo consumir de manera local en http://localhost:8000/