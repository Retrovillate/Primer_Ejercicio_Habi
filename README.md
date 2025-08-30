# Primer ejercicio Habi

## Descripción del proyecto
Este proyecto forma parte de la prueba técnica para Habi. La prueba se compone de dos puntos principales:

1. **Microservicio de Consulta de Inmuebles**:
   Permite que los usuarios externos puedan consultar inmuebles disponibles para la venta o pre-venta, así como inmuebles ya vendidos. Se pueden aplicar filtros por ciudad, año de construcción y estado del inmueble.  
   Se retorna la información esencial del inmueble: Dirección, Ciudad, Estado, Precio de venta y Descripción.

2. **Microservicio conceptual de “Me gusta”**:
   Permite conceptualizar cómo los usuarios pueden dar “Me gusta” a los inmuebles, generando un ranking interno de los más atractivos. Solo se entrega el modelo de base de datos y el SQL de creación, sin implementación del microservicio.

---

## Estructura del proyecto
```
Primer_Ejercicio_Habi/
│
├── microservicio_consulta/
│   ├── servicio_consulta.py         # Código Python del microservicio de consulta
│   ├── test_servicio_consulta.py    # Pruebas unitarias TDD
│   └── filtros_entrada.json         # Ejemplo de JSON con filtros de front-end
│
├── microservicio_me_gusta/
│   ├── modelo_me_gusta.sql          # SQL de creación de tabla y relaciones
│   └── diagrama_ERD.png             # Diagrama de Entidad-Relación conceptual
│
└── README.md
```

---

## Tecnologías utilizadas
- **Python 3.10+**: Para la lógica de negocio y consultas SQL.
- **MySQL**: Base de datos relacional.
- **SQL puro**: Sin ORM, para demostrar manejo directo de consultas.
- **Pruebas unitarias con `unittest`**: Implementación de TDD.
- **JSON**: Para simular la entrada de filtros del front-end.
- **Buenas prácticas**: Código limpio, modular y autodocumentado siguiendo PEP8.

---

## Microservicio de Consulta

### Funcionalidades
- Consultar inmuebles con estados válidos: `pre_venta`, `en_venta` y `vendido`.
- Aplicar filtros combinables:
  - Ciudad
  - Año de construcción
  - Estado (puede ser uno o varios estados a la vez)
- Manejar inconsistencias en la base de datos (registros incompletos o duplicados)
- Retornar información del inmueble:
  - Dirección
  - Ciudad
  - Estado
  - Precio de venta
  - Descripción

### Ejemplo de entrada JSON
Archivo: `filtros_entrada.json`
```json
{
    "ciudad": "Bogotá",
    "ano_construccion": 2018,
    "estado": ["pre_venta", "en_venta"]
}
```

### Uso
1. Modificar los datos de conexión en `servicio_consulta.py` (`DB_CONFIG`).
2. Ejecutar directamente el script para probar consultas:
```bash
python microservicio_consulta/servicio_consulta.py
```
3. Para pruebas unitarias:
```bash
python -m unittest microservicio_consulta/test_servicio_consulta.py
```

---

## Microservicio de “Me gusta”

### Modelo de base de datos
- Tabla `usuarios`: Información básica de los usuarios.
- Tabla `inmuebles`: Información básica de los inmuebles.
- Tabla `me_gusta`: Relación entre usuarios e inmuebles con fecha de registro y restricción de unicidad (`UNIQUE(usuario_id, inmueble_id)`).

### SQL de creación
Archivo: `modelo_me_gusta.sql`  
Se encuentra listo para ejecutar, pero no se implementó en la base de datos de prueba.

### Diagrama ERD
Archivo: `diagrama_ERD.png`  
Muestra la relación entre las tablas `usuarios`, `inmuebles` y `me_gusta`.

### Consideraciones
- Se puede extender el modelo con campos adicionales para analítica (ej. ranking por popularidad).
- Mantener integridad referencial entre usuarios e inmuebles.

---

## Pruebas Unitarias

- Ubicadas en `test_servicio_consulta.py`.
- Cobertura:
  - Filtro por ciudad
  - Filtro por año de construcción
  - Filtro por uno o varios estados
  - Combinación de filtros
- Permite validar que la lógica de consulta funcione correctamente ante distintos escenarios.

---

## Buenas prácticas implementadas

1. **Código modular**: Separación de funciones por responsabilidad.
2. **Validaciones de entrada**: Se verifica que los filtros existan y sean del tipo esperado.
3. **Manejo de errores**: Conexiones a base de datos envueltas en try/except/finally.
4. **TDD**: Se construyeron pruebas unitarias antes de ejecutar la lógica.
5. **Documentación**: Cada función incluye docstrings explicativos.

---

## Cómo abordar la prueba

1. Clonar el repositorio.
2. Configurar la base de datos con los datos de prueba provistos.
3. Ejecutar el microservicio de consulta y probar con distintos filtros JSON.
4. Revisar que los resultados cumplan con:
   - Estados válidos (`pre_venta`, `en_venta`, `vendido`)
   - Campos requeridos de cada inmueble
   - Manejo de inconsistencias
5. Revisar la propuesta conceptual del microservicio de “Me gusta” en SQL y diagrama ERD.
6. Ejecutar pruebas unitarias para asegurar la correcta funcionalidad.

---

## Notas finales
- No se utilizó ningún framework ni ORM, para demostrar estándares de código Python y SQL puro.
- Código limpio, fácil de mantener y legible.
- Manejo de errores y excepciones para garantizar que la aplicación no falle ante inconsistencias.
- Se cumplen todos los requerimientos funcionales y no funcionales especificados en la prueba técnica.

## Autor
**Msc. Inteligencia Artificial Cristian David Villate Martínez**
