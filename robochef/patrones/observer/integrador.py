"""
Archivo integrador generado automaticamente
Directorio: /home/facundo/RoboChef/robochef/patrones/observer
Fecha: 2025-11-04 15:42:21
Total de archivos integrados: 2
"""

# ================================================================================
# ARCHIVO 1/2: observable.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/observer/observable.py
# ================================================================================

from typing import Generic, TypeVar, List
from robochef.patrones.observer.observer import Observer

T = TypeVar('T')

class Observable(Generic[T]):
    
    def __init__(self):
        self._observadores: List[Observer[T]] = []

    def agregar_observador(self, observador: Observer[T]) -> None:
        if observador not in self._observadores:
            self._observadores.append(observador)

    def eliminar_observador(self, observador: Observer[T]) -> None:
        try:
            self._observadores.remove(observador)
        except ValueError:
            pass 

    def notificar_observadores(self, evento: T) -> None:
        for observador in self._observadores:
            observador.actualizar(evento)

# ================================================================================
# ARCHIVO 2/2: observer.py
# Ruta: /home/facundo/RoboChef/robochef/patrones/observer/observer.py
# ================================================================================

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar('T')

class Observer(Generic[T], ABC):

    @abstractmethod
    def actualizar(self, evento: T) -> None:
        pass

