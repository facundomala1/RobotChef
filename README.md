# 🤖 Sistema de Simulación de Restaurante Robótico - RoboChef

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/)

`RoboChef` es un sistema de simulación en **Python** que modela la gestión de una cocina futurista y automatizada. Demuestra la aplicación de principios de diseño de software (S.O.L.I.D.) y 4 patrones de diseño clave para manejar un entorno concurrente basado en eventos.

---

## 📋 Características Principales

- **Gestión de Inventario (Singleton)**: Un único inventario centralizado (`InventarioService`) gestiona el stock de ingredientes, asegurando que todos los robots compartan la misma fuente de datos.
- **Creación de Flota (Factory)**: Una `RobotFactory` permite crear diferentes tipos de robots (`COCINERO_PARRILLERO`, `CAMARERO`, etc.) sin que el sistema principal conozca los detalles de su construcción.
- **Gestión de Pedidos (Observer)**: Un sistema reactivo donde los `Pedidos` (Observables) notifican automáticamente al `JefeDeCocina` (Observer) sobre cambios de estado (ej. `RECIBIDO`, `LISTO_PARA_SERVIR`).
- **Comportamiento Dinámico (Strategy)**: Los robots cocineros pueden cambiar su algoritmo de cocina (`EstrategiaRapida` vs. `EstrategiaGourmet`) en tiempo de ejecución.
- **Simulación Concurrente**: Utiliza `threading` para simular operaciones en paralelo (múltiples robots cocinando y entregando al mismo tiempo).
- **Manejo de Excepciones**: Incluye excepciones personalizadas como `IngredientesInsuficientesException` para un control de errores robusto.

## 🧩 Estructura del Proyecto

El repositorio está organizado en un paquete principal (`robochef`) que separa claramente las responsabilidades:

- **main.py**: Punto de entrada que configura y ejecuta la simulación.
- **robochef/entidades/**: Contiene las clases de datos puras (`Robot`, `Pedido`, `Plato`, `Ingrediente`).
- **robochef/patrones/**: Implementaciones genéricas de los patrones de diseño (`Factory`, `Observer`, `Strategy`).
- **robochef/servicios/**: Contiene toda la lógica de negocio y orquestación (`JefeDeCocinaService`, `InventarioService`).
- **robochef/excepciones/**: Excepciones personalizadas para el dominio del restaurante.
- **robochef/constantes.py**: Archivo centralizado para todos los valores de configuración (tiempos, costos de batería, etc.).
- **README.md**: Este archivo.
- **USER_STORIES.md**: Las historias de usuario que definen los requisitos del sistema.

## 🛠️ Instalación

1.  **Clona este repositorio** (debes reemplazar la URL por la de tu propio repositorio)

    ```bash
    git clone [https://github.com/facundomala1/RoboChef.git](https://github.com/facundomala1/RoboChef.git)
    cd RoboChef
    ```

2.  **Crea y activa un entorno virtual**

    ```bash
    # Crear el entorno
    python3 -m venv .venv

    # Activar en macOS/Linux
    source .venv/bin/activate

    # Activar en Windows (CMD)
    # .venv\Scripts\activate
    ```

3.  **Ejecuta el proyecto**

    Este proyecto no requiere dependencias externas (`requirements.txt`) ya que solo usa la biblioteca estándar de Python.

## 🚀 Modo de uso

El script `main.py` es el punto de entrada y ejecuta una simulación completa que demuestra todos los casos de uso principales.

```bash
python3 main.py