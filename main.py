import time
from robochef.servicios.cocina.menu_service import MenuService
from robochef.servicios.cocina.inventario_service import InventarioService
from robochef.servicios.robotsservicios.jefe_cocina_service import JefeCocinaService
from robochef.entidades.cocina.pedido import Pedido
from robochef.constantes import STOCK_INICIAL_DEFAULT, TIEMPO_SIMULACION_REINTENTO, TIEMPO_SIMULACION_FINAL

def run_simulation():
    
    print("="*60 + "\n         SIMULACIÓN DE RESTAURANTE ROBOCHEF\n" + "="*60)

    # --- 1. Inicialización del Sistema ---
    print("\n[PASO 1]: Inicializando servicios centrales (Singleton y Menú)...")
    inventario = InventarioService.get_instance()
    menu = MenuService()
    jefe_cocina = JefeCocinaService()

    # --- 2. Abastecimiento de Inventario (Singleton) ---
    print("\n[PASO 2]: Abasteciendo el inventario...")
    for ingrediente in menu.get_ingredientes_base():
        inventario.agregar_stock(ingrediente, STOCK_INICIAL_DEFAULT)

    # --- 3. Inicialización de la Flota de Robots (Factory) ---
    print("\n[PASO 3]: Contratando flota de robots (Factory)...")
    jefe_cocina.inicializar_flota(num_cocineros=2, num_camareros=1)

    # --- 4. Llegada de Pedidos (Observer) ---
    print("\n[PASO 4]: Abriendo puertas... Llegan los pedidos.")
    
    plato_hamburguesa = menu.buscar_plato_por_nombre("Hamburguesa Clásica")
    plato_volcan = menu.buscar_plato_por_nombre("Volcán de Chocolate")

    pedido_1 = Pedido(numero_mesa=1, platos=[plato_hamburguesa])
    jefe_cocina.recibir_pedido(pedido_1)
    
    time.sleep(0.5)
    
    pedido_2 = Pedido(numero_mesa=3, platos=[plato_hamburguesa, plato_volcan])
    jefe_cocina.recibir_pedido(pedido_2)

    # --- 5. Simulación de Operación (Strategy) ---
    print(f"\n[PASO 5]: Cocina en operación. Esperando {TIEMPO_SIMULACION_REINTENTO} segundos...")
    time.sleep(TIEMPO_SIMULACION_REINTENTO)

    # --- 6. Llegada de más pedidos mientras otros están en espera ---
    print("\n[PASO 6]: Llega un pedido grande...")
    pedido_3 = Pedido(numero_mesa=2, platos=[plato_hamburguesa, plato_hamburguesa, plato_volcan])
    jefe_cocina.recibir_pedido(pedido_3)
    
    print(f"\n[PASO 7]: Esperando {TIEMPO_SIMULACION_FINAL} segundos más a que se liberen robots...")
    time.sleep(TIEMPO_SIMULACION_FINAL)
    
    jefe_cocina.reintentar_pedidos_pendientes()

    print("\n" + "="*60 + "\n              SIMULACIÓN COMPLETADA\n" + "="*60)

if __name__ == "__main__":
    run_simulation()