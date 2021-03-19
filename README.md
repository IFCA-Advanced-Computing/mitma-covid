mitma-covid
===========

Herramienta para procesar los datos del [Estudio de movilidad con Big Data](https://www.mitma.gob.es/ministerio/covid-19/evolucion-movilidad-big-data) elaborado por el Ministerio de Transportes (MITMA) para el estudio de las medidas contra el COVID-19.

Se pueden visualizar los datos en [este mapa](https://flowmap.blue/from-url?flows=https://raw.githubusercontent.com/IFCA/mitma-covid/main/data/processed/flowmap-blue/flows.csv&locations=https://raw.githubusercontent.com/IFCA/mitma-covid/main/data/processed/flowmap-blue/locations.csv&f=13&col=BurgYl&c=0&bo=100).

<a href="https://flowmap.blue/from-url?flows=https://raw.githubusercontent.com/IFCA/mitma-covid/main/data/processed/flowmap-blue/flows.csv&locations=https://raw.githubusercontent.com/IFCA/mitma-covid/main/data/processed/flowmap-blue/locations.csv&f=13&col=BurgYl&c=0&bo=100">
   <img alt="map" src="https://github.com/IFCA/mitma-covid/blob/main/reports/figures/map.png">
</a>

Para generar los datos desde cero usar:
```bash
python src/data.py
```
Esto descargará los datos desde la primera fecha del estudio (21 Febrero 2020) hasta día de hoy y los procesará.
Si ya tiene los datos descargados y procesados de una vez anterior y solo quiere actualizarlos con los datos recientes, puede usar:
```bash
python src/data.py --update
```
Esto mirará cuál es el último día descargado y bajará/procesará todos los días posteriores. 


**Notas metodológicas:**

El estudio tiene un [nota metodológica](https://cdn.mitma.gob.es/portal-web-drupal/covid-19/estudio/MITMA-Estudio_Movilidad_COVID-19_Informe_Metodologico_v012.pdf) con indicaciones generales, pero añadiremos aquí algunos detalles relevantes. Puede ser también útil consultar la [nota metodológica](https://cdn.fomento.gob.es/portal-web-drupal/Docs_OTLE/MFOM-Estudio_Movilidad_Interprovincial_Informe_Metodologico.pdf) del [estudio anterior](https://observatoriotransporte.mitma.gob.es/estudio-experimental) en el que se basa el estudio actual.

Los archivos de `maestria1` tienen las siguientes columnas:
* `fecha`: día considerado
* `origen` / `destino`: códigos de los municipios para el estudio. Si el código viene sucedido por un `_AM` quieres decir que pertenece a una agrupación de municipios realizada por el MITMA para aumentar el tamaño de la muestra. Los municipios que componen estas agrupaciones son municipios que pertenecen siempre a la misma provincia. El mapeo de municipios del INE a agrupaciones del MITMA se puede realizar usando el archivo `relaciones_municipio_mitma.csv`.
* `periodo`: periodo horario `{0-23}`
* `distancia`: distancia de los viajes en rangos con límites 500m, 2km, 5km, 10km, 50km, 100km
  `{'0005-002', '002-005', '005-010', '010-050', '050-100', '100+'}`
* `viajes`: numero de viajes realizados
* `viajes_km`: numero de km realizados

**Errores en los datos:**
* los datos originales no contienen el archivo correspondiente al domingo 12 de Julio para `maestra1` y `municipio`. En los archivos originales se pone el link erróneo al fichero de `maestra1` y `distrito`. Como apaño hemos duplicado a mano el archivo del 05 de Julio (domingo anterior) y reemplazado las fechas por el 12 de Julio (ver `misc.py`). También se puede elegir procesar el dataset obviando esa fecha. 
