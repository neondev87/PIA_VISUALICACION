from data_manager import DataManager

# ================================================
#                  MENÚ PRINCIPAL
# ================================================
def menu():
    while True:
        print("\n=== SISTEMA NIKE ===")
        print("1. Compras")
        print("2. Administración")
        print("3. Salir")

        op = input("\nElige una opción: ").strip()

        if op == "1":
            menu_compras()
        elif op == "2":
            menu_admin()
        elif op == "3":
            print("Saliendo...")
            break
        else:
            print("❌ Opción inválida.")


# ================================================
#                  MENÚ COMPRAS
# ================================================
def menu_compras():
    print("\n--- COMPRAS ---")

    print("\nSucursales disponibles:")
    sucursales = [
        (1, "NIKE Monterrey"),
        (2, "NIKE CDMX"),
        (3, "NIKE Guadalajara"),
        (4, "NIKE Puebla"),
        (5, "NIKE Querétaro"),
    ]

    from tabulate import tabulate
    print(tabulate(sucursales, headers=["ID", "Sucursal"], tablefmt="grid"))

    id_local = input("\nElige el ID de la sucursal: ").strip()
    if not id_local.isdigit() or int(id_local) not in range(1, 6):
        print("❌ Sucursal inválida.")
        return
    id_local = int(id_local)

    # Mostrar catálogo
    print(f"\nEstilos disponibles en catálogo: {data.contar_estilos()}\n")
    print("Catálogo de Estilos:")
    print(data.ver_catalogo_estilos())

    # Carrito
    carrito = []

    while True:
        print("\n--- MENU CARRITO ---")
        print("1. Agregar producto al carrito")
        print("2. Finalizar compra")
        print("3. Cancelar compra")

        op = input("\nElige (1-3): ").strip()

        if op == "1":
            agregar_producto(carrito)
        elif op == "2":
            if not carrito:
                print("El carrito está vacío.")
            else:
                finalizar_compra(id_local, carrito)
                return
        elif op == "3":
            print("Compra cancelada.")
            return
        else:
            print("❌ Solo opciones 1, 2 o 3.")


# ================================================
#      AGREGAR PRODUCTO AL CARRITO
# ================================================
def agregar_producto(carrito):
    print("\nAgregar producto al carrito:")

    estilo = data.elegir_estilo()
    if estilo is None:
        print("❌ Estilo inválido.")
        return

    medida = data.elegir_medida(estilo["id_estilo"], estilo["estilo"])
    if medida is None:
        return

    cantidad = data.elegir_cantidad()
    if cantidad is None:
        print("❌ Cantidad inválida.")
        return

    carrito.append({
        "id_estilo": estilo["id_estilo"],
        "estilo": estilo["estilo"],
        "tipo": estilo["tipo_estilo"],
        "medida": medida,
        "cantidad": cantidad
    })

    print("\nProducto agregado al carrito.")


# ================================================
#       FINALIZAR COMPRA
# ================================================
def finalizar_compra(id_local, carrito):
    print("\n--- RESUMEN DEL CARRITO ---")
    print(data.generar_resumen_carrito(carrito))

    confirmar = input("\n¿Confirmar compra? (s/n): ").strip().lower()
    if confirmar == "s":
        mensaje = data.procesar_carrito(id_local, carrito)
        print("\n" + mensaje)
    else:
        print("Compra cancelada.")


# ================================================
#                MENÚ ADMIN
# ================================================
def menu_admin():
    while True:
        print("\n--- ADMINISTRACIÓN ---")
        print("1. Ver tickets")
        print("2. Ver items")
        print("3. Ver productos (inventario)")
        print("4. Regresar")

        op = input("\nElige: ").strip()

        if op == "1":
            print(data.ver_tickets())
        elif op == "2":
            print(data.ver_items())
        elif op == "3":
            print(data.ver_productos())
        elif op == "4":
            return
        else:
            print("❌ Opción inválida.")


# ================================================
#               INICIO DEL PROGRAMA
# ================================================
if __name__ == "__main__":
    data = DataManager()
    menu()
