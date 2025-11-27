import pandas as pd
from datetime import datetime
from tabulate import tabulate

class DataManager:

    # ====================================
    # CONSTRUCTOR
    # ====================================
    def __init__(self):

        self.ruta_productos = "datos_csv/productos.csv"
        self.ruta_tickets   = "datos_csv/tickets.csv"
        self.ruta_items     = "datos_csv/items.csv"

        # Cargar CSV
        self.productos = pd.read_csv(self.ruta_productos, dtype=str)
        self.tickets   = pd.read_csv(self.ruta_tickets, dtype=str)
        self.items     = pd.read_csv(self.ruta_items, dtype=str)

        # Convertir a numéricos donde aplica
        self.productos["precio_lista"] = self.productos["precio_lista"].astype(float)
        self.productos["costo_unitario"] = self.productos["costo_unitario"].astype(float)

        # Mapa de estilos
        mapa_estilos = {
            "E001": "DAMA", "E002": "DAMA", "E003": "DAMA", "E004": "DAMA", "E005": "DAMA",
            "E006": "CABALLERO", "E007": "CABALLERO", "E008": "CABALLERO", "E009": "CABALLERO", "E010": "CABALLERO",
            "E011": "UNISEX", "E012": "UNISEX", "E013": "UNISEX", "E014": "UNISEX", "E015": "UNISEX",
            "E016": "RUNNER", "E017": "RUNNER", "E018": "RUNNER", "E019": "RUNNER", "E020": "RUNNER"
        }

        self.productos["tipo_estilo"] = self.productos["id_estilo"].map(mapa_estilos)

        # Inicializar tablas si están vacías
        if self.tickets.empty:
            self.tickets = pd.DataFrame(columns=["ticket","fecha_venta","id_local","venta_ticket"])

        if self.items.empty:
            self.items = pd.DataFrame(columns=[
                "ticket","item","id_estilo","id_medida",
                "cantidad","precio_venta","venta_item",
                "costo_venta","utilidad"
            ])


    # ====================================
    # GUARDAR CSV
    # ====================================
    def guardar(self):
        self.productos.to_csv(self.ruta_productos, index=False)
        self.tickets.to_csv(self.ruta_tickets, index=False)
        self.items.to_csv(self.ruta_items, index=False)


    # ====================================
    # UTILIDADES DE TABLAS
    # ====================================
    def tabla(self, df):
        if df.empty:
            return "No hay datos."
        return tabulate(df, headers="keys", tablefmt="grid", showindex=False)


    # ====================================
    # CONTAR ESTILOS
    # ====================================
    def contar_estilos(self):
        return len(self.productos["id_estilo"].unique())


    # ====================================
    # CATÁLOGO (LIMPIO, SIN ÍNDICES)
    # ====================================
    def ver_catalogo_estilos(self):
        df = self.productos[["id_estilo", "estilo", "tipo_estilo"]].drop_duplicates()

        df = df.reset_index(drop=True)          # eliminar índice
        df.insert(0, "#", df.index + 1)         # agregar número manual

        # SOLO estas columnas
        return tabulate(
            df[["#", "id_estilo", "estilo", "tipo_estilo"]],
            headers="keys",
            tablefmt="grid",
            showindex=False
        )


    # ====================================
    # VER TICKETS / ITEMS / PRODUCTOS
    # ====================================
    def ver_tickets(self):
        return self.tabla(self.tickets)

    def ver_items(self):
        return self.tabla(self.items)

    def ver_productos(self):
        return self.tabla(self.productos)


    # ====================================
    # ELEGIR ESTILO REAL (BASADO EN #)
    # ====================================
    def elegir_estilo(self):
        try:
            n = int(input("\nNúmero de estilo a agregar: ").strip())
        except:
            return None

        estilos = self.productos.drop_duplicates("id_estilo").reset_index(drop=True)

        if n < 1 or n > len(estilos):
            print("❌ Número fuera de rango.")
            return None

        row = estilos.iloc[n - 1]

        return {
            "id_estilo": row["id_estilo"],
            "estilo": row["estilo"],
            "tipo_estilo": row["tipo_estilo"]
        }


    # ====================================
    # SOLO MOSTRAR TALLAS DISPONIBLES
    # ====================================
    def elegir_medida(self, id_estilo, nombre_estilo):

        df = self.productos[self.productos["id_estilo"] == id_estilo]

        tallas = sorted(df["id_medida"].astype(int).tolist())
        tallas_str = ", ".join(str(t) for t in tallas)

        print(f"\nTallas disponibles para {nombre_estilo}: {tallas_str}")

        med = input("Elige la talla: ").strip()

        if not med.isdigit():
            print("❌ Talla inválida.")
            return None

        med = int(med)

        if med not in tallas:
            print("❌ Esa talla NO existe para este estilo.")
            return None

        return str(med).zfill(3)


    # ====================================
    # ELEGIR CANTIDAD
    # ====================================
    def elegir_cantidad(self):
        c = input("\nCantidad: ").strip()

        if not c.isdigit():
            print("❌ Cantidad inválida.")
            return None

        c = int(c)

        if c <= 0:
            print("❌ Cantidad debe ser mayor a 0.")
            return None

        return c


    # ====================================
    # VALIDACIÓN DE DISPONIBILIDAD
    # Inventario global → siempre disponible
    # ====================================
    def validar_disponibilidad_carrito(self, id_local, carrito):
        return []


    # ====================================
    # RESUMEN DEL CARRITO
    # ====================================
    def generar_resumen_carrito(self, carrito):
        tabla_data = []
        total = 0

        for c in carrito:
            prod = self.productos[
                (self.productos["id_estilo"] == c["id_estilo"]) &
                (self.productos["id_medida"] == c["medida"])
            ].iloc[0]

            precio = float(prod["precio_lista"])
            subtotal = precio * c["cantidad"]
            total += subtotal

            tabla_data.append([
                c["estilo"],
                c["tipo"],
                c["medida"],
                c["cantidad"],
                precio,
                subtotal
            ])

        tabla_impresa = tabulate(
            tabla_data,
            headers=["Estilo", "Tipo", "Medida", "Cant.", "Precio", "Subtotal"],
            tablefmt="grid"
        )

        return tabla_impresa + f"\n\nTOTAL A PAGAR: ${total:.2f}"


    # ====================================
    # PROCESAR COMPRA
    # ====================================
    def procesar_carrito(self, id_local, carrito):

        nuevo_ticket = 1001 if self.tickets.empty else int(self.tickets["ticket"].astype(int).max()) + 1
        fecha = str(datetime.now().date())
        total_venta = 0

        for idx, item in enumerate(carrito, start=1):

            prod = self.productos[
                (self.productos["id_estilo"] == item["id_estilo"]) &
                (self.productos["id_medida"] == item["medida"])
            ].iloc[0]

            precio = float(prod["precio_lista"])
            costo  = float(prod["costo_unitario"])

            venta = precio * item["cantidad"]
            total_venta += venta

            costo_total = costo * item["cantidad"]
            utilidad = venta - costo_total

            new_item = {
                "ticket": nuevo_ticket,
                "item": idx,
                "id_estilo": item["id_estilo"],
                "id_medida": item["medida"],
                "cantidad": item["cantidad"],
                "precio_venta": precio,
                "venta_item": venta,
                "costo_venta": costo_total,
                "utilidad": utilidad
            }

            self.items = pd.concat([self.items, pd.DataFrame([new_item])], ignore_index=True)

        ticket_row = {
            "ticket": nuevo_ticket,
            "fecha_venta": fecha,
            "id_local": id_local,
            "venta_ticket": total_venta
        }

        self.tickets = pd.concat([self.tickets, pd.DataFrame([ticket_row])], ignore_index=True)

        self.guardar()

        return f"Compra realizada exitosamente. Ticket #{nuevo_ticket}"
