# 31/10/2020

## 19:00-20:00 - 1h
- Instalar code (extensión ms-python)
- Clonar https://github.com/quijot/django_project_heroku_template.git
- Seguir instrucciones para deployar herokuapp

# 01/11/2020

## 18:00-20:30 - 2.5h
- Crear app **costos**
- Diseñar y armar modelo de datos
    - Empresa, Profesional, Vehículo (Combustible), Instrumento

# 04/11/2020

## 23:00-01:00 - 2h
- Diseñar y armar modelo de datos
    - Gasto (TipoGasto), Gasto Empresa, Gasto Personal, Trabajo
- Armado de admin site

# 05/11/2020

## 15:00-17:00 - 2h
- Investigando cómo asociar modelos User y Profesional

## 23:30-00:30 - 1h
- Decisión de reemplazar User por Profesional(AbstractUser) como explica [acá](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractuser)
- Configuración en settings

# 06/11/2020

## 14:00-16:00 - 2h
- Ultimado v1 del modelo
- Armando interfaz de admin para prototipo

# 07/11/2020

## 16:00-17:00 x 2 - 2h
- Reunión con Fer revisando modelo

# 08/11/2020

## 19:30-21:30 - 2h
- Ultimado v1 del modelo
- Armando interfaz de admin para prototipo

# 09/11/2020

## 16:30-17:30 - 1h
- Modificando modelos ManyToMany "through" entre Trabajos y Profesional,Vehículos e Instrumentos para agregar Horas, KMs y Jornadas respectivamente.

# 14/11/2020

## 4 h
- Adaptando SB Admin 2

# 16/11/2020

## 6 h
- UserAdmin
- Customizando urls, ListViews, DetailView, UpdateView, DeleteView de Profesional (con Formset de Gastos), Instrumento y Vehículo filtrados para user

# 19/11/2020

## 06:00-09:00 - 3h
- Investigar la mejor manera de parametrizar una app, o mejor dicho, de guardar config global / settings:
    - candidato 1: solo global preferences, muy sencillo -> Constance
    - candidato 2: global and per user preferences, un poco menos sencillo -> dynamic preferences

## 15:00-16:00 - 1h
- resolver bug en formset_layout.py
- agregar menú Perfil en topbar para editar datos de usuario

# 20/11/2020

## 08:00-11:00 y 15:00-16:00 y 23:00-04:00 - 9h
- modificar base template para permitir botones de acciones en título (por ej: Agregar objeto)
- puliendo lógica y presentación de Empresas
- puliendo lógica y presentación de Profesionales (profile, add, update, list, etc)
- código de PieChart de Chartjs para Gastos en Empresa y Profesional

# 21/11/2020

## 12:00-17:30 - 5.5h
- poder mostar cotiz dolar en topbar  
- puliendo lógica y presentación de Instrumentos y Vehículos (add, update, delete, list, etc)

# --- Parcial 42.5h ---

###### SEGUIR
- ... para hoy, EMPEZAR lógica y presentación de Trabajos (add, update, delete, list, print, generate report etc)

-----

# ToDo
## app
- pasar a poetry
## Code clean
- Factorizar código de PieChart de Chartjs para GASTOS en Empresa_Detail y Profesional_Detail
## Interfaz
- Factorizar mejor SBAdmin2 para independizarlo de la app
- Revisar si es factible reemplazar SBAdmin2 por AdminLTE o CoreUI (u otro)
## Models
- Mostrarlas en la topbar
- Investigar la mejor manera de separar los Gastos asociados a la Empresa, al Profesional y al Trabajo
- Investigar la mejor manera de TrabajoPlantilla (trabajo preconfigurado tipo Mensura, VEP, CCU, etc) y la mejor manera de guardar el TrabajoTipo de cada usuario, sería una relación Profesional<->Trabajo