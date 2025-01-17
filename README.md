# Orbea Monegros 2024 - Análisis de Datos

Este proyecto analiza los datos de la carrera Orbea Monegros 2024, una prueba de ciclismo de montaña (BTT) no competitiva realizada en Sariñena (Huesca).

## Funcionalidades

El proyecto incluye cinco módulos principales de análisis:

1. **Importación y EDA** (ex1.py)
   - Carga y validación del dataset
   - Análisis exploratorio inicial

2. **Anonimización** (ex2.py)
   - Anonimización de datos de ciclistas
   - Limpieza de registros no participantes

3. **Análisis Temporal** (ex3.py)
   - Agrupamiento de tiempos en intervalos de 20 minutos
   - Generación de histogramas de distribución

4. **Análisis de Clubs** (ex4.py)
   - Normalización de nombres de clubs
   - Análisis de participación por club

5. **Análisis UCSC** (ex5.py)
   - Análisis específico del club UCSC
   - Estadísticas de rendimiento

## Requisitos

- Python 3.11+
- Anaconda o Miniconda

### Dependencias principales
- pandas >= 2.0.3
- numpy >= 1.24.3
- matplotlib >= 3.7.1
- Faker >= 19.3.0

## Instalación

1. Clonar el repositorio:
```bash
git clone [url-repositorio]
cd orbea-monegros
```

2. Crear y activar el entorno Anaconda:
```bash
conda create -n orbea-env python=3.11
conda activate orbea-env
```

3. Instalar el paquete en modo desarrollo:
```bash
pip install -e .
```

4. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Dataset

El proyecto espera encontrar el archivo de datos en:
```
data/dataset.csv
```

El dataset debe contener las siguientes columnas:
- biker: Nombre del ciclista
- dorsal: Número de dorsal
- time: Tiempo de carrera (formato HH:MM:SS)
- club: Club al que pertenece

## Ejecución

### Modos de Ejecución

#### Ejecutar todos los ejercicios (por defecto)
```bash
python main.py
```

#### Ejecutar un ejercicio específico
```bash
python main.py --exercise 2
```

#### Modo Interactivo
```bash
python main.py --interactive
```

### Salidas generadas

- **Visualizaciones**: Se guardan en la carpeta `img/`
  - Histograma de tiempos (histograma.png)
  
- **Resultados**: Se muestran en consola con formato tabular
  - Datos anonimizados
  - Análisis de clubs
  - Estadísticas UCSC

## Tests y Calidad de Código

### Ejecución de tests
```bash
pytest tests/
```

### Cobertura de tests
```bash
# Reporte en consola
pytest --cov=src tests/

# Reporte HTML detallado
pytest --cov=src --cov-report=html tests/
```

### Verificación de estilo
```bash
# Análisis completo
pylint src/

# Análisis por módulo
pylint src/ex1.py
```

## Estructura del Proyecto

```
orbea_monegros/
│
├── data/                    # Datasets
│   └── dataset.csv         
├── img/                    # Visualizaciones generadas
│   └── histograma.png     
├── src/                    # Código fuente
│   ├── __init__.py
│   ├── ex1.py             # Importación y EDA
│   ├── ex2.py             # Anonimización
│   ├── ex3.py             # Análisis temporal
│   ├── ex4.py             # Análisis de clubs
│   └── ex5.py             # Análisis UCSC
├── tests/                  # Tests unitarios
│   ├── __init__.py
│   ├── test_ex1.py
│   ├── test_ex2.py
│   ├── test_ex3.py
│   ├── test_ex4.py
│   └── test_ex5.py
├── main.py                 # Script principal
├── setup.py               # Configuración del paquete
├── requirements.txt       # Dependencias
├── README.md             # Documentación
└── LICENSE               # Licencia Apache 2.0
```

## Licencia

Este proyecto está bajo la licencia Apache 2.0. Ver el archivo `LICENSE` para más detalles.
