# Sistema Manufactura de Plásticos

## 1. Introducción

### Sistema Manufactura de Plásticos — Manual de Usuario

Este manual explica, de forma sencilla y sin necesidad de conocimientos técnicos avanzados, cómo instalar y utilizar el **Sistema Manufactura**, una aplicación web para administrar las operaciones de una planta de producción.

Con esta herramienta se puede llevar el control de:

- Productos que se fabrican.
- Materia prima disponible en almacén.
- Máquinas y su estado de operación.
- Registros de producción diaria.
- Control de calidad y defectos.
- Mantenimiento preventivo y correctivo.
- Paros de máquina y sus causas.
- Análisis y reportes con gráficas.

El sistema está desarrollado en **Python** y utiliza **MongoDB** como base de datos.

El sistema funciona como una aplicación web, por lo que puede utilizarse desde un navegador como Google Chrome, Microsoft Edge o Mozilla Firefox.

---

# 2. Requisitos previos

Antes de instalar el sistema, es necesario contar con lo siguiente en la computadora donde se instalará:

- Python 3.10 o superior.
- MongoDB instalado y funcionando de forma local, o una cuenta de MongoDB Atlas.
- Gestor de paquetes `pip`.
- Navegador web actualizado.
- Acceso a una terminal, CMD, PowerShell o Terminal de Linux.

### Verificar Python

Para comprobar que Python está instalado correctamente, abra una terminal y ejecute:

```bash
python --version


En algunos sistemas Linux o macOS puede ser necesario utilizar:

python3 --version

Debe aparecer la versión instalada de Python.

3. Instalación
3.1 Descargar el proyecto

El proyecto se encuentra disponible en GitHub:

Repositorio:

https://github.com/johananbaruc-cmd/sistema-manufactura

Existen dos formas de obtener el proyecto.

Opción A: Descargar como ZIP
Ingrese al repositorio de GitHub.
Presione el botón Code.
Seleccione Download ZIP.
Espere a que termine la descarga.
Descomprima el archivo ZIP.
Abra una terminal dentro de la carpeta del proyecto.

La carpeta tendrá una estructura similar a:

sistema-manufactura/
Opción B: Clonar utilizando Git

Si tiene Git instalado, puede descargar el proyecto mediante:

git clone https://github.com/johananbaruc-cmd/sistema-manufactura.git

Después ingrese a la carpeta:

cd sistema-manufactura
4. Instalar Python

Si Python todavía no está instalado, descárguelo desde el sitio oficial:

https://www.python.org/

Durante la instalación en Windows, se recomienda activar la opción:

Add Python to PATH

Después de instalarlo, compruebe la instalación:

python --version
5. Instalar MongoDB

El sistema utiliza MongoDB para almacenar la información.

Puede utilizar MongoDB de dos formas:

MongoDB local

Instale MongoDB Community Server en la computadora donde ejecutará el sistema.

MongoDB Atlas

También puede utilizar MongoDB Atlas para almacenar la base de datos en la nube.

Si utiliza MongoDB Atlas, necesitará una cadena de conexión proporcionada por el servicio.

6. Crear el entorno virtual

El entorno virtual permite mantener separadas las librerías utilizadas por este proyecto de las demás instalaciones de Python.

Debe realizar este paso dentro de la carpeta del proyecto.

Windows

Ejecute:

python -m venv venv

Después active el entorno virtual:

venv\Scripts\activate
Linux / macOS

Ejecute:

python3 -m venv venv

Después active el entorno virtual:

source venv/bin/activate

Cuando el entorno virtual esté activo, aparecerá algo similar a:

(venv)

al inicio de la línea de comandos.

7. Instalar las dependencias

El proyecto contiene un archivo llamado:

requirements.txt

Este archivo contiene las librerías necesarias para ejecutar el sistema.

Con el entorno virtual activado, ejecute:

pip install -r requirements.txt

Espere a que termine la instalación.

Si está utilizando Linux y pip no funciona, puede intentar:

pip3 install -r requirements.txt
8. Configurar MongoDB

El sistema necesita conocer la ubicación de la base de datos.

La configuración normalmente se realiza mediante un archivo:

.env

Dentro del archivo se pueden establecer las siguientes variables:

MONGO_URI=mongodb://localhost:27017
DB_NAME=sistema_manufactura

Si MongoDB está instalado localmente, normalmente se puede utilizar:

MONGO_URI=mongodb://localhost:27017

Si utiliza MongoDB Atlas, deberá colocar la cadena de conexión proporcionada por MongoDB Atlas.

Por ejemplo:

MONGO_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/
DB_NAME=sistema_manufactura

Importante: No publique contraseñas, claves privadas ni credenciales de MongoDB en GitHub.

9. Generar datos de prueba

El proyecto cuenta con un script que permite generar datos aleatorios para realizar pruebas.

Este paso es opcional.

Su función es llenar la base de datos con información de prueba para poder comprobar el funcionamiento de:

Dashboard.
Gráficas.
Reportes.
Producción.
Calidad.
Mantenimiento.
Máquinas.
Paros.
Materia prima.

Para ejecutar el script:

python scripts/generar_datos_random.py

En Linux o macOS también puede utilizar:

python3 scripts/generar_datos_random.py

Este proceso permite probar el sistema sin tener que introducir manualmente todos los registros.

10. Ejecutar la aplicación

Después de instalar las dependencias y configurar MongoDB, se puede iniciar el sistema.

Primero asegúrese de que el entorno virtual esté activo:

(venv)

Después ejecute el archivo principal de la aplicación.

Si el proyecto utiliza app.py:

python app.py

En Linux o macOS:

python3 app.py

Si el proyecto utiliza otro archivo principal, deberá ejecutar el archivo correspondiente.

Cuando la aplicación se inicie correctamente, la terminal mostrará una dirección similar a:

http://127.0.0.1:5000

o:

http://localhost:5000
11. Abrir el sistema

Abra un navegador web como:

Google Chrome.
Mozilla Firefox.
Microsoft Edge.

Introduzca en la barra de direcciones la dirección que apareció en la terminal.

Por ejemplo:

http://localhost:5000

Después de ingresar correctamente, aparecerá el Dashboard principal del Sistema Manufactura de Plásticos.

12. Detener la aplicación

Mientras la aplicación esté ejecutándose, la terminal debe permanecer abierta.

Para detener el servidor presione:

Ctrl + C

La aplicación dejará de estar disponible hasta que se vuelva a iniciar.
