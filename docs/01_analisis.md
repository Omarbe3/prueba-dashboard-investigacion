# 01. Análisis y comprensión de los datos

## Objetivo

Analizar la estructura, contenido y calidad de los datos
del archivo reporte_quito.xlsx.

## 1. Comprensión de los datos

El archivo `reporte_quito.xlsx` contiene cinco hojas con información
relacionada con publicaciones científicas, proyectos de investigación,
investigadores y grupos de investigación.

| Hoja | Filas | Columnas | Descripción |
|---|---:|---:|---|
| authors_publications | 8.970 | 20 | Publicaciones científicas y sus autores. |
| projects_publications | 735 | 8 | Relación entre publicaciones y proyectos. |
| researchers_projects | 4.079 | 16 | Investigadores vinculados a proyectos. |
| projects_metadata | 223 | 9 | Información general de los proyectos. |
| researchers_groups | 790 | 14 | Grupos de investigación y sus integrantes. |

En total se identificaron 14.797 filas distribuidas en cinco hojas.

## a. Granularidad y claves candidatas

| Hoja | ¿Qué representa cada fila? | Clave candidata |
|---|---|---|
| `authors_publications` | Participación de un autor en una publicación. | Código de publicación + autor |
| `projects_publications` | Asociación entre una publicación y un proyecto. | Código de publicación + código de proyecto |
| `researchers_projects` | Participación de un investigador en un proyecto y grupo. | Código de proyecto + cédula del investigador + código de grupo |
| `projects_metadata` | Registro descriptivo de un proyecto. | Código |
| `researchers_groups` | Vinculación de un investigador con un grupo. | Código de grupo + cédula del investigador |

Las claves identificadas son candidatas y requieren
validación de unicidad antes de considerarse claves primarias.

## b. Relaciones entre hojas

| Hoja de origen | Columna | Hoja relacionada | Columna |
|---|---|---|---|
| `authors_publications` | `Codigo` | `projects_publications` | `Codigo` |
| `projects_publications` | `Codigo del proyecto` | `projects_metadata` | `Codigo` |
| `projects_metadata` | `Codigo` | `researchers_projects` | `Codigo del proyecto` |
| `researchers_projects` | `Codigo del grupo` | `researchers_groups` | `Codigo del grupo` |

Las relaciones se identificaron mediante códigos comunes
entre las hojas.

Sin embargo, se detectaron diferencias en las coincidencias
de códigos, especialmente entre `projects_publications`
y `projects_metadata`.

Por tanto, las relaciones y sus cardinalidades deberán
validarse antes de implementar las uniones definitivas.

## 2. Calidad de datos

Se analizaron las cinco hojas mediante Python y Pandas
para identificar valores nulos y registros duplicados.

### 2.1. Hallazgos identificados

| Hoja | Columna | Registros afectados | Tratamiento propuesto |
|---|---|---:|---|
| `authors_publications` | `Cuartil JCR` | 7.098 | Verificar si la clasificación aplica; conservar los nulos cuando corresponda. |
| `authors_publications` | `Cuartil SJR` | 5.543 | Revisar la indexación antes de asignar categorías. |
| `authors_publications` | `Carrera` | 7.443 | Mostrar «Sin información» sin modificar el dato original. |
| `researchers_projects` | `Carrera del docente` | 4.034 | Verificar si el campo aplica al tipo de investigador. |
| `projects_metadata` | `ODS vinculado al Proyecto` | 142 | Mantener como «Sin ODS registrado» para visualización. |
| `researchers_groups` | `Fecha de fin del grupo` | 392 | Verificar si corresponde a una participación vigente. |
| `researchers_groups` | `Sede del investigador` | 156 | Mostrar «Sin información» sin inferir una sede. |

### 2.2. Registros duplicados

No se identificaron filas completamente duplicadas
en las cinco hojas analizadas.

Sin embargo, existen códigos repetidos que requieren
validación para distinguir participaciones legítimas
de posibles duplicaciones.

### 2.3. Criterios de tratamiento

Los valores nulos no se eliminarán automáticamente.
Primero se verificará si representan información faltante
o campos que no aplican.

Las transformaciones conservarán el archivo original
y evitarán generar información no verificada.

## 3. Datos sensibles

El archivo contiene información personal de investigadores
y autores, por lo que es necesario aplicar medidas de
protección en el dashboard y los reportes.

| Hoja | Columnas sensibles | Medidas de protección |
|---|---|---|
| `authors_publications` | `Autor`, `Género` | Evitar mostrar datos individuales en indicadores públicos. |
| `researchers_projects` | `Cédula del investigador`, `Investigador`, `Género del investigador` | Ocultar números de identificación y restringir el acceso a información personal. |
| `researchers_groups` | `Cédula del investigador`, `Nombre completo`, `Género del investigador` | Excluir identificadores personales de los reportes generales. |

### 3.1. Medidas de seguridad

- Restringir el acceso al dashboard a usuarios autorizados.
- Presentar información agregada siempre que sea posible.
- No incluir cédulas en las tablas o reportes PDF generales.
- Evitar publicar información personal en GitHub.
- Mantener el archivo Excel original fuera del repositorio público.
- Aplicar las mismas restricciones de acceso a los archivos PDF exportados.

## 4. Requerimientos

### 4.1. Requerimientos funcionales

| Código | Requerimiento |
|---|---|
| RF01 | Consultar publicaciones, proyectos, investigadores y grupos de investigación de la sede Quito. |
| RF02 | Visualizar indicadores KPI sobre la producción científica y los proyectos. |
| RF03 | Filtrar la información por año y grupo de investigación. |
| RF04 | Actualizar indicadores, gráficos y tablas al aplicar filtros. |
| RF05 | Visualizar dos gráficos y una tabla de detalle. |
| RF06 | Exportar un PDF con fecha, filtros, indicadores y gráficos de la selección actual. |

### 4.2. Requerimientos no funcionales

| Código | Requerimiento |
|---|---|
| RNF01 | Seguridad: proteger los datos personales y restringir el acceso a usuarios autorizados. |
| RNF02 | Usabilidad: disponer de una interfaz clara y accesible desde un navegador web. |
| RNF03 | Rendimiento: responder eficientemente a consultas y cambios de filtros. |

## 5. Indicadores (KPI)

Se proponen cuatro indicadores para facilitar el seguimiento de
la producción científica, los proyectos y los investigadores
de la sede Quito.

### 5.1. Indicadores propuestos

| Código | Indicador | Fórmula de cálculo | Hoja de origen |
|---|---|---|---|
| KPI01 | Total de publicaciones científicas | Conteo de valores únicos no nulos de `Codigo`. | `authors_publications` |
| KPI02 | Total de proyectos de investigación | Conteo de valores únicos no nulos de `Codigo`. | `projects_metadata` |
| KPI03 | Total de grupos de investigación | Conteo de valores únicos no nulos de `Codigo del grupo`. | `researchers_groups` |
| KPI04 | Total de investigadores vinculados a proyectos | Conteo de valores únicos no nulos de `Cédula del investigador`. | `researchers_projects` |

### 5.2. Consideraciones para el cálculo

- Se utilizarán identificadores únicos para evitar conteos duplicados.
- Los indicadores se actualizarán según los filtros seleccionados.
- Los registros con identificadores nulos no se incluirán en los conteos únicos.
- Se verificará la sede correspondiente antes de presentar resultados específicos de Quito.
- Los investigadores se contabilizarán una sola vez, aunque participen en varios proyectos.

### 5.3. Utilidad de los indicadores

Los indicadores permitirán al Coordinador de Investigación
consultar la producción científica, conocer la cantidad
de proyectos registrados, identificar los grupos de investigación
y analizar la participación de investigadores.

Esta información facilitará el seguimiento institucional,
la elaboración de reportes y los procesos de evaluación
y acreditación.