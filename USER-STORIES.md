# Historias de Usuario - Sistema RoboChef

**Proyecto**: RoboChef
**Version**: 1.0.0
**Fecha**: Noviembre 2025
**Metodologia**: User Story Mapping

---

## Indice

1. [Epic 1: Gestión de Pedidos](#epic-1-gestión-de-pedidos)
2. [Epic 2: Gestión de Cocina](#epic-2-gestión-de-cocina)
3. [Epic 3: Gestión de Flota y Entregas](#epic-3-gestión-de-flota-y-entregas)
4. [Historias Técnicas (Patrones de Diseño)](#historias-técnicas-patrones-de-diseño)

---

## Epic 1: Gestión de Pedidos

### US-001: Recibir un nuevo pedido

**Como** Jefe de Cocina,
**Quiero** recibir nuevos pedidos de los clientes en el sistema,
**Para** poder ponerlos en la cola de preparación.

#### Criterios de Aceptación

- [x] Un `Pedido` debe crearse con un número de mesa y una lista de `Platos`.
- [x] Al crearse, el `Pedido` debe tener el estado `RECIBIDO`.
- [x] El `Pedido` debe registrarse en el `JefeDeCocinaService` para ser procesado.

#### Detalles Tecnicos

**Clase**: `Pedido` (`robochef/entidades/cocina/pedido.py`)
**Servicio**: `JefeCocinaService.recibir_pedido()`

---

### US-002: Ser notificado de cambios de estado del pedido

**Como** Jefe de Cocina,
**Quiero** ser notificado automáticamente cuando un `Pedido` cambia de estado,
**Para** poder asignar la siguiente tarea (cocinar o entregar) sin tener que revisar manualmente.

#### Criterios de Aceptación

- [x] La clase `Pedido` debe ser un `Observable`.
- [x] La clase `JefeCocinaService` debe ser un `Observer`.
- [x] Cuando se llama a `pedido.set_estado()`, se debe notificar a todos los observadores suscritos.
- [x] El `JefeDeCocina` debe suscribirse a cada nuevo pedido que recibe.

#### Detalles Tecnicos

**Patrón**: Observer
**Observable**: `Pedido` (`robochef/entidades/cocina/pedido.py`)
**Observer**: `JefeCocinaService` (`robochef/servicios/robots/jefe_cocina_service.py`)

---

## Epic 2: Gestión de Cocina

### US-003: Verificar y descontar ingredientes del inventario

**Como** Jefe de Cocina,
**Quiero** que el sistema verifique y descuente los ingredientes del inventario centralizado *antes* de asignar una tarea,
**Para** asegurar que no intentemos cocinar platos para los que no tenemos stock.

#### Criterios de Aceptación

- [x] Debe existir un **único** `InventarioService` para todo el restaurante.
- [x] Antes de pasar a `EN_PREPARACION`, el sistema debe comprobar el stock de *todos* los ingredientes del pedido.
- [x] Si hay stock, se descuentan las cantidades.
- [x] Si no hay stock, se lanza una `IngredientesInsuficientesException` y el pedido se marca como `CANCELADO`.

#### Detalles Tecnicos

**Patrón**: Singleton
**Clase**: `InventarioService` (`robochef/servicios/cocina/inventario_service.py`)

---

### US-004: Asignar un Robot Cocinero a un pedido

**Como** Jefe de Cocina,
**Quiero** asignar un robot cocinero disponible a un pedido validado,
**Para** que comience la preparación.

#### Criterios de Aceptación

- [x] El sistema debe poder crear diferentes tipos de robots (`COCINERO_PARRILLERO`, `COCINERO_REPOSTERO`).
- [x] Esta creación debe estar centralizada en una `RobotFactory`.
- [x] El `JefeDeCocina` debe buscar un robot del tipo adecuado que esté `operativo` y no `ocupado`.
- [x] Si no hay robots disponibles, el pedido queda en espera (`RECIBIDO`).

#### Detalles Tecnicos

**Patrón**: Factory Method
**Clase**: `RobotFactory` (`robochef/patrones/factory/robot_factory.py`)

---

### US-005: Cocinar un pedido con diferentes estilos

**Como** Robot Cocinero,
**Quiero** tener diferentes algoritmos de cocina (rápido o gourmet),
**Para** poder adaptarme a la demanda del restaurante (ej. hora punta vs. hora valle).

#### Criterios de Aceptación

- [x] Debe existir una interfaz `EstrategiaCocina`.
- [x] Deben existir al menos dos implementaciones: `EstrategiaRapida` (consume menos batería) y `EstrategiaGourmet` (consume más batería y es más lenta).
- [x] El `RobotCocinero` debe tener una estrategia asignada y delegar la ejecución del trabajo (`trabajar()`) a ella.

#### Detalles Tecnicos

**Patrón**: Strategy
**Interfaz**: `EstrategiaCocina` (`robochef/patrones/strategy/estrategia_cocina.py`)
**Implementaciones**: `EstrategiaRapida`, `EstrategiaGourmet`

---

## Epic 3: Gestión de Flota y Entregas

### US-006: Asignar un Robot Camarero para entrega

**Como** Jefe de Cocina,
**Quiero** que, cuando un pedido esté `LISTO_PARA_SERVIR`, el sistema asigne automáticamente un robot camarero,
**Para** que el plato no se enfríe.

#### Criterios de Aceptación

- [x] El `JefeDeCocina` debe ser notificado (vía Observer) del estado `LISTO_PARA_SERVIR`.
- [x] El `JefeDeCocina` debe buscar un `RobotCamarero` que esté `operativo` y no `ocupado`.
- [x] Si no hay camareros disponibles, el pedido queda en espera de entrega.
- [x] El `main.py` debe tener un bucle que reintente asignar pedidos en espera.

#### Detalles Tecnicos

**Servicio**: `JefeCocinaService._asignar_entrega_camarero()`
**Clase**: `RobotCamarero` (`robochef/entidades/robots/robot_camarero.py`)

---

### US-007: Manejar Batería y Concurrencia de Robots

**Como** Sistema de Gestión de Flota,
**Quiero** que los robots consuman batería al trabajar y se pongan fuera de servicio si se agota,
**Para** simular un ciclo de operación realista.

#### Criterios de Aceptación

- [x] Cada robot debe tener un nivel de `_bateria_actual`.
- [x] Al `trabajar()`, el robot debe consumir batería (cantidad definida por la `Strategy` en cocineros).
- [x] Si la batería llega a 0, el robot debe marcarse como no `operativo`.
- [x] Las tareas de los robots (cocinar, entregar) deben ejecutarse en hilos (`threading`) separados para no bloquear al `JefeDeCocina`.

#### Detalles Tecnicos

**Clase**: `Robot` (`robochef/entidades/robots/robot.py`)
**Servicio**: `JefeCocinaService` (maneja los `threading.Thread`)

---

## Historias Técnicas (Patrones de Diseño)

### US-TECH-001: Implementar Singleton para Inventario

**Como** arquitecto de software,
**Quiero** garantizar una única instancia del `InventarioService`,
**Para** evitar inconsistencias de stock y asegurar que todos los robots compartan el mismo recurso.

#### Criterios de Aceptación
- [x] Implementar patrón Singleton thread-safe (con `threading.Lock`).
- [x] Usar inicialización perezosa (lazy initialization).
- [x] Proveer un método `get_instance()` para el acceso global.

---

### US-TECH-002: Implementar Factory Method para Robots

**Como** arquitecto de software,
**Quiero** desacoplar al `JefeDeCocina` de la construcción de robots,
**Para** poder añadir nuevos tipos de robots sin modificar el servicio principal.

#### Criterios de Aceptación
- [x] Crear una `RobotFactory` con un método estático `crear_robot(tipo)`.
- [x] Usar un diccionario de métodos de creación (no `if/elif`).
- [x] La fábrica debe asignar la `EstrategiaCocina` por defecto a los robots cocineros.

---

### US-TECH-003: Implementar Observer para Pedidos

**Como** arquitecto de software,
**Quiero** que el `JefeDeCocina` reaccione a los cambios de estado de los pedidos,
**Para** crear un sistema reactivo y evitar bucles de sondeo (polling) ineficientes.

#### Criterios de Aceptación
- [x] `Pedido` debe heredar de `Observable[Pedido]`.
- [x] `JefeCocinaService` debe heredar de `Observer[Pedido]`.
- [x] `pedido.set_estado()` debe llamar a `notificar_observadores(self)`.
- [x] `jefe_cocina.actualizar()` debe contener la lógica de qué hacer con cada estado.
- [x] Usar `RLock` en el `JefeDeCocina` para prevenir *deadlocks* durante la notificación.

---

### US-TECH-004: Implementar Strategy para Cocina

**Como** arquitecto de software,
**Quiero** que los algoritmos de cocina sean intercambiables,
**Para** permitir al sistema (o a un robot) cambiar su comportamiento dinámicamente.

#### Criterios de Aceptación
- [x] Crear una interfaz abstracta `EstrategiaCocina`.
- [x] Crear implementaciones concretas (`EstrategiaRapida`, `EstrategiaGourmet`).
- [x] `RobotCocinero` debe tener una estrategia y delegar la ejecución a ella.
- [x] La entidad `RobotCocinero` no debe importar los patrones (romper dependencias circulares).

---