# Little Lemon

Proyecto de un restaurante desarrollado con Django y Django REST Framework. Incluye vistas web y una API REST para gestionar el menú y las reservas, con autenticación por token. Es el proyecto final de la certificación Meta Back-End Developer (Coursera).

## Tecnologías
- Python
- Django y Django REST Framework
- [MySQL / la base de datos que uses]
- Autenticación por token

## Funcionalidades
- Gestión de elementos del menú (crear, listar, ver, actualizar y eliminar)
- Gestión de reservas
- Autenticación por token para la API
- [Roles o permisos, si los implementaste]

## Rutas disponibles

### Vistas web
| Ruta | Descripción |
|---|---|
| `/` | Página de inicio |
| `/about/` | Información del restaurante |
| `/book/` | Formulario de reserva |
| `/menu/` | Listado del menú |
| `/menu/<int:pk>/` | Detalle de un elemento del menú |
| `/reservations/` | Listado de reservas |

### API REST
| Ruta | Descripción |
|---|---|
| `/menu-items/` | Listar y crear elementos del menú |
| `/menu-items/<int:pk>/` | Ver, actualizar o eliminar un elemento |
| `/bookings/` | Gestionar reservas |
| `/api-token-auth/` | Obtener el token de autenticación |

## Cómo ejecutarlo localmente
1. Cloná el repositorio y entrá a la carpeta del proyecto.
2. Instalá las dependencias: `pipenv install`
3. Activá el entorno: `pipenv shell`
4. Configurá la base de datos en `settings.py` (en `DATABASES`, completá `USER` y `PASSWORD` con tus datos).
5. Aplicá las migraciones: `python manage.py migrate`
6. Iniciá el servidor: `python manage.py runserver`
