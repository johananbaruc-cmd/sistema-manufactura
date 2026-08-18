#!/usr/bin/env python3
"""
Script para poblar la base de datos con datos ficticios para una empresa de MANUFACTURA DE PLÁSTICOS.
Genera datos con patrones no uniformes para análisis y predicción.
"""

import os
import sys
import random
from datetime import datetime, timedelta
from collections import defaultdict

# Agregar el directorio raíz al path para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from faker import Faker
import numpy as np
from config.database import get_db, close_db

# Inicializar Faker
fake = Faker('es_ES')

# ==================== CONFIGURACIÓN ====================
FECHA_INICIO = datetime.now() - timedelta(days=90)
FECHA_FIN = datetime.now()

# ==================== CATEGORÍAS Y PRODUCTOS DE PLÁSTICO ====================
CATEGORIAS_PLASTICO = [
    'Envasado y Embalaje',
    'Construcción',
    'Automotriz',
    'Electrodomésticos',
    'Juguetes',
    'Médico y Farmacéutico',
    'Agrícola',
    'Mobiliario'
]

PRODUCTOS_PLASTICO = [
    'Tubería PVC', 'Lámina Polietileno', 'Copa PET', 'Botella PET', 
    'Película Polipropileno', 'Contenedor Polietileno', 'Perfil PVC',
    'Pieza Automotriz', 'Juguete Inyectado', 'Embalaje Espumado',
    'Tapa Polipropileno', 'Envasado Alimenticio', 'Manguera PVC',
    'Caja Polietileno', 'Pallet Plástico', 'Aislante Térmico'
]

MATERIAS_PLASTICO = [
    'Resina PET Grado Alimenticio',
    'Resina PVC Grado Construcción',
    'Polietileno Alta Densidad (HDPE)',
    'Polietileno Baja Densidad (LDPE)',
    'Polipropileno (PP)',
    'Poliestireno (PS)',
    'Masterbatch Color Blanco',
    'Masterbatch Color Negro',
    'Aditivo Antioxidante',
    'Agente Anti-estático',
    'Estabilizador UV',
    'Carga de Carbonato de Calcio',
    'Pigmento Azul',
    'Pigmento Rojo',
    'Agente Espumante'
]

TIPOS_DEFECTO_PLASTICO = [
    'Marca de flujo',
    'Burbujas superficiales',
    'Deformación por contracción',
    'Rayón o arañazo',
    'Mancha de aceite',
    'Mal llenado de molde',
    'Sopladura irregular',
    'Espesor no uniforme',
    'Fisura por estrés',
    'Color fuera de especificación',
    'Rebaba excesiva',
    'Perforación o agujero',
    'Textura irregular'
]

# ==================== GENERADORES DE DATOS ====================

def generar_productos(db, cantidad=15):
    """Genera productos de plástico con diferentes categorías y precios."""
    productos = []
    
    for i in range(cantidad):
        nombre = random.choice(PRODUCTOS_PLASTICO) + f" {fake.random_number(digits=2)}"
        categoria = random.choice(CATEGORIAS_PLASTICO)
        
        costo = round(random.uniform(10, 5000), 2)
        precio = round(costo * random.uniform(1.3, 2.5), 2)
        
        # Demanda no uniforme
        demanda_base = np.random.poisson(100)
        if i % 3 == 0:
            demanda = int(demanda_base * random.uniform(1.5, 3.0))
        elif i % 5 == 0:
            demanda = int(demanda_base * random.uniform(0.3, 0.6))
        else:
            demanda = int(demanda_base * random.uniform(0.8, 1.2))
        
        # Peso en gramos por unidad
        peso_gramos = round(random.uniform(5, 500), 1)
        
        producto = {
            "nombre": nombre,
            "descripcion": f"Producto de plástico {categoria.lower()} - {fake.sentence(nb_words=8)}",
            "categoria": categoria,
            "codigo": f"PLA-{fake.random_number(digits=6)}",
            "costo": costo,
            "precio": precio,
            "stock_minimo": random.randint(50, 500),
            "stock_actual": random.randint(100, 2000),
            "demanda_promedio_mensual": demanda,
            "tiempo_fabricacion_minutos": random.randint(10, 120),
            "peso_gramos": peso_gramos,
            "material_principal": random.choice(MATERIAS_PLASTICO[:6]),
            "fecha_creacion": fake.date_time_between(start_date="-2y", end_date="now"),
            "activo": random.choice([True, True, True, False])
        }
        productos.append(producto)
    
    return productos

def generar_materia_prima(db, cantidad=12):
    """Genera materia prima para manufactura de plásticos."""
    materias = []
    proveedores = ['BASF', 'Dow Chemical', 'SABIC', 'LyondellBasell', 
                   'ExxonMobil', 'Braskem', 'INEOS', 'Borealis']
    
    for i in range(cantidad):
        nombre = random.choice(MATERIAS_PLASTICO)
        costo_unitario = round(random.uniform(1, 50), 2)
        
        # Algunas materias primas son más críticas (stock más alto)
        if 'Masterbatch' in nombre or 'Resina' in nombre:
            stock_actual = random.randint(500, 5000)
            stock_minimo = random.randint(100, 500)
        else:
            stock_actual = random.randint(100, 1000)
            stock_minimo = random.randint(20, 200)
        
        materia = {
            "nombre": nombre,
            "descripcion": f"Insumo para fabricación de plásticos - {fake.sentence(nb_words=6)}",
            "codigo": f"MP-{fake.random_number(digits=6)}",
            "proveedor": random.choice(proveedores),
            "costo_unitario": costo_unitario,
            "unidad_medida": random.choice(['kg', 'toneladas', 'litros', 'sacos']),
            "stock_minimo": stock_minimo,
            "stock_actual": stock_actual,
            "tiempo_entrega_dias": random.randint(2, 20),
            "fecha_ultima_compra": fake.date_time_between(start_date="-3m", end_date="now"),
            "activo": random.choice([True, True, True, False])
        }
        materias.append(materia)
    
    return materias

def generar_maquinas(db, cantidad=8):
    """Genera máquinas para procesamiento de plásticos con lecturas de sensores."""
    maquinas = []
    
    tipos_maquinas = [
        'Máquina de Inyección', 'Extrusora', 'Máquina de Soplado', 
        'Termoformadora', 'Inyectora de Preformas', 'Línea de Película',
        'Máquina de Moldeo por Compresión', 'Recicladora'
    ]
    marcas = ['Arburg', 'Demag', 'Battenfeld', 'Engel', 'KraussMaffei', 
              'Bekum', 'Kiefel', 'Cincinnati']
    
    for i in range(cantidad):
        tiene_anomalia = i < 3
        
        lecturas = []
        dias = (FECHA_FIN - FECHA_INICIO).days
        
        for dia in range(dias):
            fecha = FECHA_INICIO + timedelta(days=dia)
            num_lecturas = random.randint(1, 3)
            
            for _ in range(num_lecturas):
                timestamp = fecha + timedelta(hours=random.randint(0, 23), 
                                             minutes=random.randint(0, 59))
                
                # Parámetros específicos para plásticos
                temperatura_base = random.uniform(170, 230)  # °C (plásticos)
                presion_base = random.uniform(500, 1500)     # Bar (inyección)
                vibracion_base = random.uniform(0.3, 1.2)
                flujo_base = random.uniform(5, 20)           # Índice de flujo
                
                # Simular anomalías antes de falla
                if tiene_anomalia and dia > dias * 0.7:
                    factor = 1 + (dia - dias * 0.7) / (dias * 0.3) * 0.4
                    temperatura = temperatura_base * factor + random.gauss(0, 5)
                    presion = presion_base * factor + random.gauss(0, 50)
                    vibracion = vibracion_base * factor * 1.5 + random.gauss(0, 0.1)
                    flujo = flujo_base * (0.8 + 0.4 * (1 - factor)) + random.gauss(0, 0.5)
                else:
                    temperatura = temperatura_base + random.gauss(0, 5)
                    presion = presion_base + random.gauss(0, 30)
                    vibracion = vibracion_base + random.gauss(0, 0.05)
                    flujo = flujo_base + random.gauss(0, 0.5)
                
                # Picos aleatorios
                if random.random() < 0.03:
                    temperatura += random.uniform(15, 30)
                    vibracion += random.uniform(0.2, 0.5)
                    presion += random.uniform(100, 300)
                
                lectura = {
                    "timestamp": timestamp,
                    "temperatura": round(max(150, temperatura), 1),
                    "presion": round(max(300, presion), 1),
                    "vibracion": round(max(0, vibracion), 3),
                    "indice_flujo": round(max(1, flujo), 2),
                    "estado": random.choices(
                        ["operando", "operando", "operando", "mantenimiento", "parada"],
                        weights=[0.85, 0.85, 0.85, 0.10, 0.05]
                    )[0]
                }
                lecturas.append(lectura)
        
        maquina = {
            "nombre": f"{random.choice(tipos_maquinas)} {fake.random_number(digits=2)}",
            "tipo": random.choice(tipos_maquinas),
            "marca": random.choice(marcas),
            "modelo": f"{fake.random_letter().upper()}{random.randint(100, 999)}",
            "capacidad_toneladas": round(random.uniform(50, 500), 1),
            "fecha_instalacion": fake.date_time_between(start_date="-8y", end_date="-1m"),
            "ubicacion": f"Planta {random.randint(1,3)} - Línea {random.randint(1,6)}",
            "estado": random.choices(
                ["operando", "operando", "operando", "mantenimiento", "parada"],
                weights=[0.70, 0.70, 0.70, 0.15, 0.05]
            )[0],
            "horas_operacion": random.randint(2000, 80000),
            "ciclos_totales": random.randint(10000, 1000000),
            "lecturas_sensores": lecturas,
            "temperatura_operativa": round(random.uniform(175, 225), 1),
            "presion_operativa": round(random.uniform(600, 1400), 1),
            "vibracion_operativa": round(random.uniform(0.4, 1.0), 2),
            "tiene_historial_anomalias": tiene_anomalia,
            "falla_reciente": tiene_anomalia and random.random() < 0.4,
            "ultimo_mantenimiento": fake.date_time_between(start_date="-3m", end_date="now"),
            "horas_ultimo_mantenimiento": random.randint(100, 1000)
        }
        maquinas.append(maquina)
    
    return maquinas

def generar_produccion(db, productos, maquinas, cantidad=200):
    """Genera registros de producción de piezas plásticas."""
    producciones = []
    turnos = ['Matutino', 'Vespertino', 'Nocturno']
    operadores = [fake.name() for _ in range(25)]
    estados = ['completado', 'completado', 'completado', 'en_proceso', 'cancelado']
    
    for _ in range(cantidad):
        producto = random.choice(productos)
        maquina = random.choice(maquinas)
        
        # Cantidad producida según demanda
        demanda = producto.get('demanda_promedio_mensual', 100)
        cantidad_producida = max(1, int(np.random.poisson(demanda / 25)))
        
        # Tiempo de producción
        tiempo_base = producto.get('tiempo_fabricacion_minutos', 30)
        tiempo_real = tiempo_base * random.uniform(0.8, 1.5)
        
        fecha = fake.date_time_between(start_date=FECHA_INICIO, end_date=FECHA_FIN)
        
        # Tasa de defectos (relacionada con el producto)
        if 'PET' in producto.get('nombre', '') or 'BOTELLA' in producto.get('nombre', '').upper():
            tasa_defectos = random.uniform(0.02, 0.06)  # Más difíciles
        elif 'TUBERÍA' in producto.get('nombre', '').upper():
            tasa_defectos = random.uniform(0.01, 0.04)
        else:
            tasa_defectos = random.uniform(0.005, 0.04)
        
        produccion = {
            "producto_id": producto.get('_id'),
            "maquina_id": maquina.get('_id'),
            "fecha": fecha,
            "turno": random.choice(turnos),
            "operador": random.choice(operadores),
            "cantidad_producida": int(cantidad_producida),
            "tiempo_produccion_minutos": round(tiempo_real, 1),
            "temperatura_promedio": round(random.uniform(170, 235), 1),
            "presion_promedio": round(random.uniform(500, 1600), 1),
            "estado": random.choices(estados, weights=[0.7, 0.7, 0.7, 0.15, 0.05])[0],
            "defectos_encontrados": int(cantidad_producida * tasa_defectos * random.uniform(0.5, 1.5)),
            "peso_promedio": round(random.uniform(5, 500), 1),
            "observaciones": fake.sentence() if random.random() < 0.25 else ""
        }
        producciones.append(produccion)
    
    return producciones

def generar_calidad(db, productos, producciones, cantidad=80):
    """Genera registros de calidad con defectos típicos de plásticos."""
    calidades = []
    
    prod_por_producto = defaultdict(list)
    for p in producciones:
        prod_por_producto[p['producto_id']].append(p)
    
    for _ in range(cantidad):
        producto_ids = list(prod_por_producto.keys())
        if producto_ids:
            if random.random() < 0.6:
                producto_id = random.choice(producto_ids[:len(producto_ids)//3])
            else:
                producto_id = random.choice(producto_ids)
            
            producciones_del_producto = prod_por_producto[producto_id]
            if producciones_del_producto:
                produccion = random.choice(producciones_del_producto)
            else:
                produccion = random.choice(producciones)
        else:
            produccion = random.choice(producciones)
        
        # Defectos específicos de plásticos
        defecto = {
            "produccion_id": produccion.get('_id'),
            "producto_id": produccion.get('producto_id'),
            "fecha": fake.date_time_between(start_date=FECHA_INICIO, end_date=FECHA_FIN),
            "tipo_defecto": random.choices(TIPOS_DEFECTO_PLASTICO, weights=[
                0.15, 0.12, 0.13, 0.10, 0.08, 0.10, 0.05, 0.08, 0.06, 0.06, 0.04, 0.02, 0.01
            ])[0],
            "severidad": random.choices(['Bajo', 'Medio', 'Alto', 'Crítico'], weights=[0.3, 0.35, 0.25, 0.1])[0],
            "descripcion": f"Defecto en pieza plástica: {fake.sentence(nb_words=6)}",
            "inspector": fake.name(),
            "accion_tomada": random.choice(['Reprocesar', 'Rechazar', 'Reparar', 'Aceptar con condición', 'Ninguna']),
            "costo_reparacion": round(random.uniform(0.5, 500), 2),
            "ubicacion_defecto": random.choice(['Borde', 'Centro', 'Superficie', 'Interior', 'Cara superior', 'Cara inferior'])
        }
        calidades.append(defecto)
    
    return calidades

def generar_mantenimiento(db, maquinas, cantidad=40):
    """Genera registros de mantenimiento para maquinaria de plásticos."""
    mantenimientos = []
    tipos = ['Preventivo', 'Correctivo', 'Predictivo']
    tecnicos = [fake.name() for _ in range(10)]
    
    descripciones_mantenimiento = [
        'Cambio de boquilla', 'Limpieza de cilindro', 'Cambio de filtro',
        'Calibración de temperatura', 'Reemplazo de termopares', 'Ajuste de presión',
        'Cambio de aceite hidráulico', 'Revisión de sistema de enfriamiento',
        'Cambio de tornillo', 'Limpieza de molde', 'Reemplazo de resistencias',
        'Calibración de servo', 'Cambio de sellos', 'Revisión de bombas'
    ]
    
    maquinas_con_problemas = random.sample(maquinas, min(3, len(maquinas)))
    
    for _ in range(cantidad):
        maquina = random.choice(maquinas)
        
        if maquina in maquinas_con_problemas:
            tipo = random.choices(tipos, weights=[0.15, 0.65, 0.20])[0]
        else:
            tipo = random.choices(tipos, weights=[0.55, 0.15, 0.30])[0]
        
        if tipo == 'Preventivo':
            fecha = fake.date_time_between(start_date="-4m", end_date="now")
            duracion_horas = random.uniform(1, 6)
        else:
            fecha = fake.date_time_between(start_date="-2m", end_date="now")
            duracion_horas = random.uniform(2, 12)
        
        mantenimiento = {
            "maquina_id": maquina.get('_id'),
            "tipo": tipo,
            "fecha": fecha,
            "tecnico": random.choice(tecnicos),
            "descripcion": random.choice(descripciones_mantenimiento),
            "duracion_horas": round(duracion_horas, 1),
            "costo": round(duracion_horas * random.uniform(80, 250), 2),
            "piezas_reemplazadas": random.randint(0, 6),
            "observaciones": fake.sentence() if random.random() < 0.4 else "",
            "efectividad": random.choices(
                ['Alta', 'Media', 'Baja'], 
                weights=[0.6, 0.3, 0.1]
            )[0] if tipo != 'Correctivo' else random.choice(['Alta', 'Media', 'Baja'])
        }
        mantenimientos.append(mantenimiento)
    
    return mantenimientos

def generar_paros(db, maquinas, cantidad=60):
    """Genera registros de paros en planta de plásticos."""
    paros = []
    causas = [
        'Falla eléctrica', 'Falla hidráulica', 'Atasco de material',
        'Sobrecalentamiento', 'Falta de materia prima', 'Error de operador',
        'Mantenimiento no programado', 'Problema de calidad', 'Falla de molde',
        'Problema de enfriamiento', 'Falla de sensor', 'Cambio de producción'
    ]
    operadores = [fake.name() for _ in range(15)]
    
    for _ in range(cantidad):
        maquina = random.choice(maquinas)
        
        duracion_minutos = int(np.random.exponential(scale=25) + 5)
        duracion_minutos = min(duracion_minutos, 480)
        
        # Máquinas de inyección tienen más paros
        if maquina in maquinas[:3]:
            frecuencia_paro = 0.35
        else:
            frecuencia_paro = 0.12
        
        if random.random() > frecuencia_paro:
            continue
        
        fecha = fake.date_time_between(start_date=FECHA_INICIO, end_date=FECHA_FIN)
        
        paro = {
            "maquina_id": maquina.get('_id'),
            "fecha": fecha,
            "hora_inicio": fecha,
            "duracion_minutos": duracion_minutos,
            "causa": random.choices(causas, weights=[0.12, 0.10, 0.08, 0.10, 0.15, 0.10, 0.10, 0.05, 0.08, 0.06, 0.04, 0.02])[0],
            "operador_responsable": random.choice(operadores),
            "accion_tomada": random.choice([
                'Reinicio', 'Llamar a mantenimiento', 'Reemplazar pieza', 
                'Ajustar parámetros', 'Esperar material', 'Cambiar molde'
            ]),
            "costo_estimado": round(duracion_minutos / 60 * random.uniform(80, 350), 2),
            "tiempo_resolucion_minutos": int(duracion_minutos * random.uniform(0.5, 1.5)),
            "observaciones": fake.sentence() if random.random() < 0.3 else ""
        }
        paros.append(paro)
    
    return paros

# ==================== FUNCIÓN PRINCIPAL ====================

def main():
    """Función principal que ejecuta la generación de todos los datos."""
    print("=" * 70)
    print("🏭 GENERANDO DATOS PARA EMPRESA DE MANUFACTURA DE PLÁSTICOS")
    print("=" * 70)
    print("")
    
    db = get_db()
    
    print("🗑️  Limpiando colecciones existentes...")
    colecciones = ['productos', 'materia_prima', 'maquinas', 'produccion', 
                   'calidad', 'mantenimiento', 'paros']
    for coleccion in colecciones:
        db[coleccion].drop()
    print("✅ Colecciones limpiadas\n")
    
    print("📦 Generando productos de plástico...")
    productos = generar_productos(db)
    db.productos.insert_many(productos)
    print(f"   ✅ {len(productos)} productos insertados")
    
    print("🧪 Generando materia prima para plásticos...")
    materias = generar_materia_prima(db)
    db.materia_prima.insert_many(materias)
    print(f"   ✅ {len(materias)} materias primas insertadas")
    
    print("🔧 Generando máquinas de procesamiento...")
    maquinas = generar_maquinas(db)
    db.maquinas.insert_many(maquinas)
    total_lecturas = sum(len(m.get('lecturas_sensores', [])) for m in maquinas)
    print(f"   ✅ {len(maquinas)} máquinas insertadas con {total_lecturas} lecturas de sensores")
    
    print("🔄 Estableciendo relaciones...")
    productos_db = list(db.productos.find())
    maquinas_db = list(db.maquinas.find())
    
    print("🏭 Generando producción...")
    producciones = generar_produccion(db, productos_db, maquinas_db)
    db.produccion.insert_many(producciones)
    print(f"   ✅ {len(producciones)} registros de producción insertados")
    
    print("📊 Generando control de calidad...")
    calidades = generar_calidad(db, productos_db, producciones)
    db.calidad.insert_many(calidades)
    print(f"   ✅ {len(calidades)} registros de calidad insertados")
    
    print("🔩 Generando mantenimiento...")
    mantenimientos = generar_mantenimiento(db, maquinas_db)
    db.mantenimiento.insert_many(mantenimientos)
    print(f"   ✅ {len(mantenimientos)} registros de mantenimiento insertados")
    
    print("⏸️  Generando paros...")
    paros = generar_paros(db, maquinas_db)
    db.paros.insert_many(paros)
    print(f"   ✅ {len(paros)} registros de paros insertados")
    
    print("\n" + "=" * 70)
    print("📊 RESUMEN FINAL - EMPRESA DE PLÁSTICOS")
    print("=" * 70)
    print(f"   🧊 Productos: {db.productos.count_documents({})}")
    print(f"   🧪 Materia Prima: {db.materia_prima.count_documents({})}")
    print(f"   🔧 Máquinas: {db.maquinas.count_documents({})}")
    print(f"   🏭 Producción: {db.produccion.count_documents({})}")
    print(f"   📊 Calidad: {db.calidad.count_documents({})}")
    print(f"   🔩 Mantenimiento: {db.mantenimiento.count_documents({})}")
    print(f"   ⏸️  Paros: {db.paros.count_documents({})}")
    print("=" * 70)
    print("✅ ¡Datos generados exitosamente!")
    print("🏭 Contexto: Empresa de Manufactura de Plásticos")
    print("=" * 70)
    
    close_db()

if __name__ == "__main__":
    main()