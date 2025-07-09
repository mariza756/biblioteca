# Biblioteca - Mariza Valdez
## Versiones de Herramientas utilizadas
```text
Package                       Version
----------------------------- -----------
asgiref                       3.9.1
contourpy                     1.3.2
cycler                        0.12.1
Django                        5.2.4
djangorestframework           3.16.0
djangorestframework_simplejwt 5.5.0
fonttools                     4.58.5
kiwisolver                    1.4.8
matplotlib                    3.10.3
numpy                         2.3.1
packaging                     25.0
pandas                        2.3.1
pillow                        11.3.0
pip                           24.3.1
psycopg2                      2.9.10
PyJWT                         2.9.0
pyparsing                     3.2.3
python-dateutil               2.9.0.post0
pytz                          2025.2
seaborn                       0.13.2
six                           1.17.0
sqlparse                      0.5.3
tzdata                        2025.2
```

## Guía de instalación y configuración
### Instalación de Python
Asegúrate de tener Python 3.8+ instalado. Puedes descargarlo desde python.org.
Para verificar la instalación:

```bash
python --version
```

### Creación de entorno virtual
Se recomienda usar un entorno virtual para aislar las dependencias del proyecto.
En este ejemplo, el entorno se llama ent.
```bash
# Abre una terminal en la carpeta del proyecto
python -m venv ent
```

Para activar el entorno virtual:

En Windows:
```bash
ent\Scripts\activate
```

En Linux/Mac:
```bash
source ent/bin/activate
``` 
### Instalación de Django y psycopg2
Con el entorno activado, instala Django y el conector para PostgreSQL:
```bash
pip install django psycopg2-binary
``` 

### Creación del proyecto Django
Si aún no creaste tu proyecto, hazlo así (ejemplo: se llamará biblioteca):
```bash
django-admin startproject biblioteca 
cd biblioteca
```

### Creación de una aplicación
Ejemplo, crea una app llamada libros:
```bash
python manage.py startapp libros
```

### Configuración de la base de datos PostgreSQL
Edita el archivo biblioteca/settings.py y busca la sección DATABASES.
Cámbiala así (usa tus propios datos de usuario, password, etc):

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'biblioteca',
        'USER': 'postgres',
        'PASSWORD': '123',          # Cambia por tu password real
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```
### Migraciones iniciales
Aplica las migraciones para crear las tablas base:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Descripción y Funcionamiento del Programa
Este proyecto es un sistema de gestión y análisis de libros desarrollado en Django, utilizando PostgreSQL como base de datos. Permite registrar libros, autores, géneros, usuarios y calificaciones, así como generar reportes gráficos y recomendaciones personalizadas.

### ¿Cómo funciona el programa? 
**Modelo de datos:**
El programa utiliza el framework Django para estructurar los datos en modelos relacionales:

- Autor: Almacena nombre y nacionalidad del autor.
- Género: Define el género literario.
- Libro: Incluye título, autor, género, año de lanzamiento, ISBN y enlace.
- Calificación: Relaciona usuarios con libros, almacenando una nota del 1 al 5.

**Usuarios y autenticación:**
Se utiliza el sistema de usuarios de Django, permitiendo el registro, inicio de sesión y asignación de calificaciones por cada usuario, Se utiliza JWT para autenticacion.

**Administración y reportes:**
El programa permite gestionar la información desde la interfaz administrativa de Django. Además, incluye comandos personalizados para la consola que generan reportes automáticos en forma de gráficos (por ejemplo: top autores, libros mejor calificados, etc.) y para recomendaciones de libros.

**Comandos personalizados:**
Los comandos escritos con BaseCommand permiten analizar los datos de la base y producir resultados útiles, por ejemplo:

- Generar gráficos que resumen visualmente la información de la biblioteca (cantidad de libros por género, evolución anual, mejores autores, etc).
- Recomendar libros a partir del género seleccionado, mostrando los títulos con mejores calificaciones.

**Citación del funcionamiento**
```text
"El usuario puede ejecutar comandos desde la consola como python manage.py reportes_libros para generar gráficos estadísticos en la carpeta /graficos, o python manage.py recomienda_libros --genero=Fantasía para obtener sugerencias de lectura personalizadas por género.
Todo el procesamiento se realiza sobre los datos almacenados en la base PostgreSQL, utilizando las capacidades ORM de Django para consultas eficientes y seguras."
```

El programa está diseñado para ser fácil de instalar, configurar y expandir, siguiendo las buenas prácticas de desarrollo con Django y asegurando compatibilidad multiplataforma.

## Prueba de la Aplicacion

### **Registrarse!**
**Url de la api registro:**
```http
POST http://127.0.0.1:8000/api/register/
```
**Cargamos los datos en Json:**
```json
{
  "username": "mariza",
  "email": "marizavaldez.alta@gmail.com",
  "password": "12345678!",
  "password2": "12345678!",
  "first_name": "Mariza",
  "last_name": "Valdez"
}
```
**La respuesta en postman:**
<img width="962" height="532" alt="Image" src="https://github.com/user-attachments/assets/fca6b093-8cb8-4861-be96-88e3d0f5542a" />

**Codigo para el registro:**
```python
#serializers.py
class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, min_length=8)
    password2 = serializers.CharField(write_only=True, required=True, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("El nombre de usuario ya está en uso.")
        if 'email' in data and User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("El email ya está registrado.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
#views.py
class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación
```

## **Inicio de Sesion**
**Url de la api login:**
```http
POST http://127.0.0.1:8000/api/login/
```
**Cargamos los datos en Json:**
```json
{
  "username": "mariza",
  "password": "12345678!"
}
```
**La respuesta en postman:**
<img width="966" height="582" alt="Image" src="https://github.com/user-attachments/assets/3d9e2d58-9aa1-4ad0-96f9-fe789b70fa94" />

El Login genera un access token, que luego va a servir para autenticar las demas aplicaciones.


## **Aplicacion Libros**
**Listar todos libros**
**Url de la api libros:**
```http
GET http://127.0.0.1:8000/api/libros/
```
En auth type se selecciona bearer token y se pone el access token generado en login.

**Respuesta en postman:**
<img width="972" height="828" alt="Image" src="https://github.com/user-attachments/assets/511cb9d2-801a-455f-931b-2431d531a324" />

**Listar libro por ID**
**Url de la api libros:**
```http
GET http://127.0.0.1:8000/api/libros/3/
```
Se pasa en la url el id del libro que se desea.
En auth type se selecciona bearer token y se pone el access token generado en login.
**Respuesta en postman:**
<img width="974" height="718" alt="Image" src="https://github.com/user-attachments/assets/f0dd18e7-36f1-428d-a9d8-7fc496bfdf8a" />

**Insertar nuevo Libro**
**Url de la api libros:**
```http
POST http://127.0.0.1:8000/api/libros/
```
En auth type se selecciona bearer token y se pone el access token generado en login.

**Cargamos los datos en Json:**
```json
{
    "titulo": "Trilogía de la ocupación",
    "autor_id": 2,
    "genero_id": 1,
    "fecha_lanzamiento": "1990-01-01",
    "isbn": "9788433968466",
    "libro_url": "https://www.casadellibro.com/libro-trilogia-de-la-ocupacion/9788433968466/1091870"
}
```
**Respuesta en postman:**
<img width="970" height="714" alt="Image" src="https://github.com/user-attachments/assets/fbcae9a6-b083-43bf-a4f4-11f347254e90" />

**Actualizar Libro**
**Url de la api libros:**
```http
PUT http://127.0.0.1:8000/api/libros/61/
```
Se pasa en la url el id del libro que se desea **actualizar**.
En auth type se selecciona bearer token y se pone el access token generado en login.

**Cargamos los datos en Json:**
```json
{
    "titulo": "Accidente nocturno",
    "autor_id": 2,
    "genero_id": 4,
    "fecha_lanzamiento": "2003-01-01",
    "isbn": "9788433974139",
    "libro_url": "https://www.casadellibro.com/libro-accidente-nocturno/9788433974139/890926"
}
```
**Respuesta en postman:**
<img width="972" height="724" alt="Image" src="https://github.com/user-attachments/assets/0dd6c1b9-19f5-42c0-b2b1-bef97fb6a039" />

**Eliminar Libro**
**Url de la api libros:**
```http
PUT http://127.0.0.1:8000/api/libros/61/
```
Se pasa en la url el id del libro que se desea **eliminar**.
En auth type se selecciona bearer token y se pone el access token generado en login.

**Respuesta en postman:**
<img width="968" height="546" alt="Image" src="https://github.com/user-attachments/assets/cb569149-1506-48b6-b384-8723786b7f1d" />

## Codigo del View en Libros

**Vistas (Views) de la API**
Las vistas principales de la API utilizan la clase ModelViewSet de Django REST Framework, lo que permite implementar de manera sencilla todas las operaciones CRUD (crear, leer, actualizar y eliminar) para cada uno de los modelos: Autor, Género, Libro y Calificación.
Cada ViewSet está protegido para que solo los usuarios autenticados puedan acceder a sus funcionalidades, asegurando la privacidad y seguridad de los datos.

```python
class LibroViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated] 
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
```
**¿Por qué se eligió este enfoque?**
- **Simplicidad y rapidez:** Usar ModelViewSet permite crear de forma automática todos los endpoints REST (GET, POST, PUT, DELETE, etc.) sin necesidad de definir manualmente cada acción, acelerando el desarrollo.
- **Mantenibilidad:** Al centralizar la lógica repetitiva, el código es más limpio y fácil de mantener.
- **Seguridad:** Se utiliza IsAuthenticated para que solo los usuarios logueados accedan a la API, protegiendo la información sensible.
- **Estandarización:** Este enfoque sigue las recomendaciones oficiales de Django REST Framework, asegurando compatibilidad y buenas prácticas.

## Descripción del script de reportes gráficos
El proyecto incluye un comando personalizado (reportes_libros) que genera una serie de gráficos estadísticos basados en la información almacenada en la base de datos.
Cada gráfico se guarda como imagen PNG en la carpeta graficos.

A continuación se describe la utilidad de cada reporte:

**1. Top 5 géneros con más libros**
Archivo: reporte1_top5_libros_por_genero.png

Descripción:
Presenta los cinco géneros literarios con mayor cantidad de libros registrados en el sistema. Permite visualizar las preferencias temáticas predominantes en la biblioteca.

<img width="800" height="600" alt="Image" src="https://github.com/user-attachments/assets/7690de20-86a8-4af3-9162-0ca2557a7664" />

**2. Top 5 autores con más libros**
Archivo: reporte2_top5_autores_mas_libros.png

Descripción:
Muestra los cinco autores con mayor número de libros en la base de datos, ayudando a identificar a los escritores más representados en la colección.

<img width="800" height="600" alt="Image" src="https://github.com/user-attachments/assets/9bd2cf98-2101-4977-af37-d40c569c53fc" />

**3. Top 5 libros mejor calificados**
Archivo: reporte3_top5_libros_mejor_calificados.png

Descripción:
Expone los cinco libros que tienen el promedio de calificación más alto otorgado por los usuarios, indicando las obras más apreciadas o recomendadas.

<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/bbe71154-6d83-45ac-9c32-21650102cd1f" />

**4. Libros publicados por año**
Archivo: reporte4_libros_por_anio.png

Descripción:
Representa la evolución en el tiempo de la cantidad de libros publicados cada año. Este gráfico de líneas permite analizar tendencias y picos de publicación.

<img width="1000" height="600" alt="Image" src="https://github.com/user-attachments/assets/19967b02-1029-4f0d-88ec-10317c070133" />

**5. Top 5 usuarios con más calificaciones**
Archivo: reporte5_top5_usuarios_mas_calificaciones.png

Descripción:
Identifica a los usuarios más activos, es decir, aquellos que han emitido la mayor cantidad de calificaciones dentro del sistema.

<img width="900" height="600" alt="Image" src="https://github.com/user-attachments/assets/089ddfad-3c76-4f70-88b2-29ebacfb04ac" />

**6. Distribución de calificaciones (1 a 5)**
Archivo: reporte6_distribucion_calificaciones.png

Descripción:
Muestra la cantidad de calificaciones asignadas para cada valor posible (del 1 al 5), visualizando si los usuarios tienden a ser estrictos, promedio o generosos en sus evaluaciones.

<img width="640" height="480" alt="Image" src="https://github.com/user-attachments/assets/a707d48c-b360-436d-926f-125f34adc217" />

**7. Libros sin calificaciones**
Archivo: reporte7_libros_sin_calificaciones.png

Descripción:
Enlista todos los libros que todavía no han recibido ninguna calificación por parte de los usuarios, lo que puede ser útil para identificar obras poco valoradas o promocionar su lectura.

<img width="1000" height="459" alt="Image" src="https://github.com/user-attachments/assets/dd6bfc0d-a6c5-4eee-b28c-ed722c0ae71e" />

**8. Top 5 autores mejor calificados**
Archivo: reporte8_top5_autores_mejor_calificados.png

Descripción:
Presenta a los cinco autores cuyo promedio de calificación en sus libros es el más alto, brindando un panorama sobre la calidad percibida de sus obras.

<img width="1000" height="500" alt="Image" src="https://github.com/user-attachments/assets/08e9d13d-af99-4e80-9383-2a6acfeb0614" />

**9. Top 5 géneros más calificados**
Archivo: reporte9_top5_generos_mas_calificados.png

Descripción:
Muestra los géneros que acumulan la mayor cantidad de calificaciones en total, reflejando la interacción y popularidad entre los usuarios.
<img width="900" height="500" alt="Image" src="https://github.com/user-attachments/assets/2fb31760-98cc-4d96-a7f6-a359a616ca54" />

**10. Top 5 libros más calificados**
Archivo: reporte10_top5_libros_mas_calificados.png

Descripción:
Lista los cinco libros que recibieron la mayor cantidad de calificaciones, independientemente de su promedio. Permite identificar los títulos más populares o polémicos.

<img width="1000" height="500" alt="Image" src="https://github.com/user-attachments/assets/1cd7372f-8c92-43e1-93be-f50a29ba16d9" />
## Script de recomendaciones de libros por género

El proyecto incluye un comando personalizado para la consola llamado recomienda_libros, que genera una lista de libros recomendados en base a un género literario seleccionado por el usuario. Este comando facilita obtener rápidamente los títulos mejor valorados según la opinión de los usuarios registrados en el sistema.

**¿Cómo funciona el script?**
**Selección de género:**
El usuario puede indicar el género literario por su nombre o por su identificador numérico (id) utilizando el argumento --genero.
Si no se proporciona este argumento, el programa muestra la lista de géneros disponibles y permite seleccionar uno interactuando en la consola.

**Lógica de recomendación:**
El comando busca los libros del género seleccionado, calcula el promedio de calificaciones de cada libro y presenta los títulos con mejor puntuación, ordenando primero por promedio más alto y luego por cantidad de calificaciones (en caso de empate).
El número de recomendaciones puede ajustarse con el argumento --top (por defecto, 3 libros).

**Salida:**
La recomendación se muestra directamente en la consola, e incluye el título del libro, su promedio de calificación, la cantidad de calificaciones recibidas y el nombre del autor.
Además, la lista de recomendaciones se guarda automáticamente en un archivo de texto llamado recomendaciones_libros.txt para fácil consulta o impresión.

**Ejemplo de uso**
**Recomendación interactiva:**

```bash
python manage.py recomienda_libros
```
(El sistema mostrará los géneros disponibles y solicitará que selecciones uno.)

**Recomendación por id:**

```bash
python manage.py recomienda_libros --genero=4
```
Recomendación por nombre y top personalizado:

```bash
python manage.py recomienda_libros --genero="Ciencia Ficción" --top=5
```
<img width="634" height="92" alt="Image" src="https://github.com/user-attachments/assets/09b94b91-25d9-4e5b-adb5-a942735a587a" />

## Licencia
Este proyecto se distribuye bajo la licencia MIT, lo que significa que eres libre de utilizar, modificar y distribuir el código, incluso para fines comerciales, siempre que conserves el aviso de copyright y la licencia en cualquier copia.

**Licencias de herramientas de terceros**
```text
Name                           Version      License
 Django                         5.2.4        BSD License
 PyJWT                          2.9.0        MIT License
 asgiref                        3.9.1        BSD License
 contourpy                      1.3.2        BSD License
 cycler                         0.12.1       BSD License
 djangorestframework            3.16.0       BSD License
 djangorestframework_simplejwt  5.5.0        MIT License
 fonttools                      4.58.5       MIT
 kiwisolver                     1.4.8        BSD License
 matplotlib                     3.10.3       Python Software Foundation License
 numpy                          2.3.1        BSD License
 packaging                      25.0         Apache Software License; BSD License
 pandas                         2.3.1        BSD License
 pillow                         11.3.0       UNKNOWN
 psycopg2                       2.9.10       GNU Library or Lesser General Public License (LGPL)
 pyparsing                      3.2.3        MIT License
 python-dateutil                2.9.0.post0  Apache Software License; BSD License
 pytz                           2025.2       MIT License
 seaborn                        0.13.2       BSD License
 six                            1.17.0       MIT License
 sqlparse                       0.5.3        BSD License
 tzdata                         2025.2       Apache Software License
```
