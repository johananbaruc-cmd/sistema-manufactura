# Documentación Técnica — Sistema de Manufactura de Plásticos

---

## ¿Qué es este sistema?

Es una aplicación web para gestionar y analizar las operaciones de una **empresa de manufactura de plásticos**. Permite llevar el control de máquinas, producción, calidad, mantenimiento y paros de planta, todo desde un navegador web.

El sistema incluye un panel de análisis avanzado con gráficas, predicción de fallas y exportación de reportes en PDF y Excel.

---

## Tecnologías utilizadas

| Componente | Tecnología | Para qué sirve |
|---|---|---|
| Backend (servidor) | Python + Flask | Procesa las peticiones del navegador y se comunica con la base de datos |
| Base de datos | MongoDB | Guarda toda la información (documentos flexibles, sin tablas fijas) |
| Frontend (interfaz) | HTML + Bootstrap 5 + JavaScript | Lo que el usuario ve y usa en el navegador |
| Gráficas | Chart.js | Visualización de datos en tiempo real |
| Exportación PDF | jsPDF + jsPDF-AutoTable | Generación de reportes en formato PDF |
| Exportación Excel | SheetJS (xlsx) | Generación de archivos Excel con los datos del análisis |
| Datos de prueba | Faker + NumPy | Generación de datos ficticios realistas para desarrollo |

---

## Cómo está organizado el proyecto

```
sistema-manufactura/
│
├── app.py                  ← Corazón del sistema: rutas web y API REST
├── .env                    ← Variables de entorno (conexión a BD, clave secreta)
├── requirements.txt        ← Librerías de Python necesarias
│
├── config/
│   └── database.py         ← Conexión a MongoDB (patrón singleton)
│
├── templates/              ← Páginas HTML que el usuario ve
│   ├── base.html           ← Plantilla base: barra lateral y navegación
│   ├── dashboard.html      ← Página principal con resumen general
│   ├── productos.html      ← Gestión de productos plásticos
│   ├── materia_prima.html  ← Gestión de materias primas
│   ├── maquinas.html       ← Gestión de maquinaria
│   ├── produccion.html     ← Registros de producción
│   ├── calidad.html        ← Control de calidad y defectos
│   ├── mantenimiento.html  ← Registros de mantenimiento
│   ├── paros.html          ← Registro de paros de planta
│   ├── analisis.html       ← Centro de análisis con 10+ gráficas
│   └── crud_base.html      ← Plantilla reutilizable para formularios CRUD
│
├── static/
│   ├── css/style.css       ← Estilos personalizados
│   └── js/dashboard.js     ← Lógica JavaScript del dashboard principal
│
└── scripts/
    └── generar_datos_random.py  ← Script para poblar la BD con datos ficticios
```

---

## Base de datos

El sistema usa **MongoDB** (base de datos NoSQL). Los datos se guardan en colecciones (equivalente a tablas en bases de datos relacionales). No hay un archivo de modelo separado — los campos se definen directamente al insertar datos.

### Colecciones y sus campos principales

#### `productos`
Catálogo de productos plásticos fabricados.

| Campo | Tipo | Descripción |
|---|---|---|
| nombre | texto | Nombre del producto (ej: "Tubería PVC 32") |
| categoria | texto | Categoría (Envasado, Automotriz, Construcción…) |
| codigo | texto | Código único del producto |
| costo | número | Costo de fabricación |
| precio | número | Precio de venta |
| stock_actual | número | Unidades disponibles en inventario |
| stock_minimo | número | Mínimo de stock permitido (alerta si baja) |
| demanda_promedio_mensual | número | Demanda estimada por mes |
| tiempo_fabricacion_minutos | número | Tiempo para fabricar una unidad |
| material_principal | texto | Materia prima principal (PET, PVC, HDPE…) |
| activo | booleano | Si el producto está activo o no |

---

#### `materia_prima`
Insumos usados en la fabricación.

| Campo | Tipo | Descripción |
|---|---|---|
| nombre | texto | Nombre del material (ej: "Resina PET Grado Alimenticio") |
| proveedor | texto | Empresa proveedora (BASF, Dow Chemical…) |
| costo_unitario | número | Costo por unidad |
| unidad_medida | texto | kg, toneladas, litros, sacos |
| stock_actual | número | Cantidad disponible |
| tiempo_entrega_dias | número | Días que tarda en llegar al pedirse |
| fecha_ultima_compra | fecha | Cuándo se compró por última vez |

---

#### `maquinas`
Maquinaria de la planta (inyectoras, extrusoras, termoformadoras, etc.).

| Campo | Tipo | Descripción |
|---|---|---|
| nombre | texto | Nombre de la máquina |
| tipo | texto | Tipo (Máquina de Inyección, Extrusora…) |
| marca | texto | Fabricante (Arburg, Engel, KraussMaffei…) |
| estado | texto | operando / mantenimiento / parada |
| ubicacion | texto | Planta y línea donde está |
| horas_operacion | número | Total de horas acumuladas de uso |
| temperatura_operativa | número | Temperatura normal de trabajo (°C) |
| presion_operativa | número | Presión normal de trabajo (Bar) |
| lecturas_sensores | lista | Historial de lecturas de sensores (ver abajo) |

**Lecturas de sensores** (guardadas dentro de cada máquina):

| Campo | Descripción |
|---|---|
| timestamp | Fecha y hora de la lectura |
| temperatura | Temperatura del proceso (°C) |
| presion | Presión del proceso (Bar) |
| vibracion | Nivel de vibración (mm/s) |
| indice_flujo | Fluidez del material |
| estado | Estado de la máquina en ese momento |

---

#### `produccion`
Registros de cada corrida de producción.

| Campo | Tipo | Descripción |
|---|---|---|
| producto_id | ID | Producto que se fabricó |
| maquina_id | ID | Máquina que lo fabricó |
| fecha | fecha | Cuándo se realizó |
| turno | texto | Matutino / Vespertino / Nocturno |
| operador | texto | Nombre del operador responsable |
| cantidad_producida | número | Unidades fabricadas |
| defectos_encontrados | número | Unidades con defecto |
| tiempo_produccion_minutos | número | Duración de la corrida |
| temperatura_promedio | número | Temperatura promedio durante la producción |
| estado | texto | completado / en_proceso / cancelado |

---

#### `calidad`
Registros de defectos detectados durante inspección.

| Campo | Tipo | Descripción |
|---|---|---|
| produccion_id | ID | Corrida de producción afectada |
| producto_id | ID | Producto defectuoso |
| tipo_defecto | texto | Marca de flujo, burbujas, fisura, rebaba… |
| severidad | texto | Bajo / Medio / Alto / Crítico |
| inspector | texto | Quien detectó el defecto |
| accion_tomada | texto | Reprocesar / Rechazar / Reparar… |
| costo_reparacion | número | Costo de corregir el defecto ($) |
| ubicacion_defecto | texto | Dónde está el defecto en la pieza |

---

#### `mantenimiento`
Historial de trabajos de mantenimiento en las máquinas.

| Campo | Tipo | Descripción |
|---|---|---|
| maquina_id | ID | Máquina que recibió mantenimiento |
| tipo | texto | Preventivo / Correctivo / Predictivo |
| fecha | fecha | Cuándo se realizó |
| tecnico | texto | Técnico responsable |
| descripcion | texto | Qué se hizo (cambio de boquilla, limpieza…) |
| duracion_horas | número | Cuánto tiempo tomó |
| costo | número | Costo total del mantenimiento |
| piezas_reemplazadas | número | Cuántas piezas se cambiaron |
| efectividad | texto | Alta / Media / Baja |

---

#### `paros`
Registro de interrupciones no programadas en la producción.

| Campo | Tipo | Descripción |
|---|---|---|
| maquina_id | ID | Máquina que se paró |
| fecha | fecha | Cuándo ocurrió el paro |
| duracion_minutos | número | Cuánto tiempo duró |
| causa | texto | Por qué se detuvo (falla eléctrica, material…) |
| operador_responsable | texto | Quien reportó el paro |
| accion_tomada | texto | Cómo se resolvió |
| costo_estimado | número | Costo estimado por el tiempo perdido |

---

## Pantallas del sistema

### Dashboard (Inicio)
La pantalla principal muestra un resumen ejecutivo:
- Total de productos, máquinas, producciones y defectos registrados
- Gráfica de producción vs defectos de los últimos 30 días
- Estado actual de las máquinas (operando / mantenimiento / parada)
- Los 5 productos más producidos
- Últimas 10 actividades de producción

### Módulos de gestión (Productos, Materia Prima, Máquinas, Producción, Calidad, Mantenimiento, Paros)
Cada módulo permite:
- **Ver** todos los registros en una tabla
- **Crear** nuevos registros con un formulario
- **Editar** registros existentes
- **Eliminar** registros

### Análisis avanzado
La pantalla más completa del sistema. Incluye:

1. **Filtros** — por rango de fechas, máquina y producto
2. **KPIs** — Eficiencia global, total de fallas, tiempo muerto y tasa de calidad
3. **10 gráficas analíticas:**
   - Eficiencia por línea de producción
   - Máquinas con más fallas (mantenimientos correctivos)
   - Productos con más defectos
   - Productividad por operador (unidades/hora)
   - Distribución de causas de paro
   - Correlación temperatura vs vibración
   - Tendencias de sensores (temperatura, vibración, presión en el tiempo)
   - Agrupación de máquinas por comportamiento (algoritmo k-means)
   - Mantenimiento predictivo: máquinas en riesgo de falla próxima
   - Gráfica personalizable por el usuario
4. **Recomendaciones automáticas** basadas en los datos
5. **Exportar a PDF** — Reporte completo con gráficas y estadísticas
6. **Exportar a Excel** — Datos tabulados en múltiples hojas

---

## API REST

El sistema expone una API que el navegador usa para obtener y guardar datos. Todos los endpoints comienzan con `/api/`.

### Estado del sistema
| Método | URL | Qué hace |
|---|---|---|
| GET | `/api/health` | Verifica si el servidor y la base de datos están activos |

### Dashboard
| Método | URL | Qué hace |
|---|---|---|
| GET | `/api/dashboard/stats` | Totales de todos los módulos |
| GET | `/api/dashboard/produccion-ultimos-dias` | Producción diaria (acepta `?dias=30`) |
| GET | `/api/dashboard/defectos-por-producto` | Top 10 productos con más defectos |
| GET | `/api/dashboard/estado-maquinas` | Conteo de máquinas por estado |
| GET | `/api/dashboard/top-productos` | Top 5 productos más producidos |

### CRUD por módulo
Cada módulo soporta las 4 operaciones básicas:

| Método | URL | Qué hace |
|---|---|---|
| GET | `/api/{modulo}` | Lista todos los registros |
| POST | `/api/{modulo}` | Crea un registro nuevo |
| PUT | `/api/{modulo}/{id}` | Actualiza un registro existente |
| DELETE | `/api/{modulo}/{id}` | Elimina un registro |

Los módulos disponibles son: `productos`, `materia_prima`, `maquinas`, `produccion`, `calidad`, `mantenimiento`, `paros`.

**Ejemplo:** `GET /api/productos` devuelve la lista de todos los productos.

### Análisis
| Método | URL | Qué hace |
|---|---|---|
| GET | `/api/reportes/analisis` | Devuelve todos los datos para las gráficas del módulo de análisis. Acepta parámetros: `fechaInicio`, `fechaFin`, `maquina`, `producto` |

---

## Cómo ejecutar el proyecto

### Requisitos previos
- Python 3.8 o superior
- MongoDB corriendo localmente en el puerto 27017
- pip (gestor de paquetes de Python)

### Pasos

**1. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**2. Configurar variables de entorno**

El archivo `.env` ya viene configurado para desarrollo local:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=sistema_manufactura
FLASK_ENV=development
SECRET_KEY=algo-seguro-aqui
```

**3. Poblar la base de datos con datos de prueba**
```bash
python scripts/generar_datos_random.py
```
Este script genera automáticamente datos ficticios de 90 días de operación:
- 15 productos plásticos
- 12 materias primas
- 8 máquinas con lecturas de sensores
- 200 registros de producción
- 80 registros de calidad
- 40 registros de mantenimiento
- ~60 paros de planta

**4. Iniciar el servidor**
```bash
python app.py
```

**5. Abrir en el navegador**
```
http://localhost:5001
```

---

## Algoritmos de análisis

### K-means (agrupación de máquinas)
El sistema implementa el algoritmo k-means directamente en el navegador (JavaScript) para agrupar las máquinas en 3 niveles de riesgo: **Alto**, **Medio** y **Bajo**.

Cómo funciona:
1. Calcula el promedio de temperatura y vibración de cada máquina
2. Normaliza los valores para que ambas variables pesen igual (z-score)
3. Agrupa las máquinas en 3 clusters según similitud
4. El cluster con mayor temperatura y vibración promedio = Alto Riesgo

### Mantenimiento predictivo
Una máquina se marca en riesgo si sus últimas 3 lecturas superan simultáneamente el umbral de "media + 1 desviación estándar" de toda la planta en temperatura Y vibración.

### Interpretaciones automáticas
Cada gráfica genera texto explicativo automático que identifica el mejor y peor valor, calcula el promedio y brinda una recomendación contextualizada para el sector de plásticos.

---

## Dependencias del proyecto

```
Flask==2.3.3          ← Framework web para Python
pymongo==4.5.0        ← Conector de MongoDB para Python
python-dotenv==1.0.0  ← Carga variables de entorno desde .env
flask-cors==4.0.0     ← Permite peticiones desde otros dominios
faker==19.10.0        ← Generación de datos ficticios (solo para pruebas)
numpy==1.24.3         ← Cálculos numéricos (solo para el script de pruebas)
```

---

## Flujo de datos

```
Usuario (navegador)
      │
      │ Petición HTTP (GET, POST, PUT, DELETE)
      ▼
   app.py (Flask)
      │
      │ Consulta / Escritura
      ▼
   MongoDB
   (sistema_manufactura)
      │
      │ Respuesta JSON
      ▼
   app.py
      │
      │ JSON o HTML renderizado
      ▼
Usuario (navegador)
      │
      │ JavaScript procesa el JSON
      ▼
   Gráficas y tablas actualizadas
```

---

## Notas importantes

- **Sin autenticación de usuarios**: El sistema no tiene login. Cualquiera con acceso a la URL puede usar todas las funciones. Para producción sería necesario agregar un sistema de autenticación.
- **Datos de prueba**: El script `generar_datos_random.py` **borra todos los datos existentes** antes de insertar los nuevos. Úsalo solo en desarrollo.
- **Límite de registros**: Los endpoints de producción, calidad, mantenimiento y paros devuelven máximo 100 registros por consulta (los más recientes). Esto evita que la página se vuelva lenta con grandes volúmenes de datos.
- **Conexión MongoDB**: El sistema usa un patrón singleton para la conexión (una sola conexión compartida por todas las peticiones), lo que es eficiente para aplicaciones de tamaño mediano.
- **Puerto por defecto**: El servidor corre en el puerto `5001`. Se puede cambiar con la variable de entorno `PORT`.
