import json

# Clase base Venta
class Venta:
    def __init__(self, fecha, cliente, productos, idproducto):
        self.fecha = fecha
        self.cliente = cliente
        self.productos = productos
        self.idproducto = idproducto

    def __str__(self):
        return (f"Fecha: {self.fecha}, Cliente: {self.cliente}, "
                f"Productos: {self.productos}, ID Producto: {self.idproducto}")

# Clases derivadas para tipos de ventas
class VentaOnline(Venta):
    def __init__(self, fecha, cliente, productos, idproducto, direccion_envio):
        super().__init__(fecha, cliente, productos, idproducto)
        self.direccion_envio = direccion_envio

    def __str__(self):
        return (super().__str__() + f", Dirección de Envío: {self.direccion_envio}")

class VentaLocal(Venta):
    def __init__(self, fecha, cliente, productos, idproducto, tienda):
        super().__init__(fecha, cliente, productos, idproducto)
        self.tienda = tienda

    def __str__(self):
        return (super().__str__() + f", Tienda: {self.tienda}")

# Gestor de Ventas
class GestorVentas:
    def __init__(self, archivo):
        self.archivo = archivo
        self.ventas = self.cargar_ventas()

    def cargar_ventas(self):
        try:
            with open(self.archivo, 'r') as file:
                data = json.load(file)
                return [self.dict_a_venta(d) for d in data]
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as e:
            print(f"Error al cargar el archivo JSON: {e}")
            return []

    def guardar_ventas(self):
        try:
            with open(self.archivo, 'w') as file:
                json.dump([self.venta_a_dict(v) for v in self.ventas], file, indent=4)
        except IOError as e:
            print(f"Error al guardar el archivo JSON: {e}")

    def dict_a_venta(self, data):
        try:
            if data['tipo'] == 'Online':
                return VentaOnline(data['fecha'], data['cliente'], data['productos'], data['idproducto'], data['direccion_envio'])
            elif data['tipo'] == 'Local':
                return VentaLocal(data['fecha'], data['cliente'], data['productos'], data['idproducto'], data['tienda'])
            else:
                raise ValueError("Tipo de venta desconocido")
        except KeyError as e:
            print(f"Falta una clave en el diccionario: {e}")
            raise

    def venta_a_dict(self, venta):
        data = {
            'fecha': venta.fecha,
            'cliente': venta.cliente,
            'productos': venta.productos,
            'idproducto': venta.idproducto
        }
        if isinstance(venta, VentaOnline):
            data.update({'tipo': 'Online', 'direccion_envio': venta.direccion_envio})
        elif isinstance(venta, VentaLocal):
            data.update({'tipo': 'Local', 'tienda': venta.tienda})
        return data

    def crear_venta(self, venta):
        try:
            self.ventas.append(venta)
            self.guardar_ventas()
            print("Venta creada:", venta)
        except Exception as e:
            print(f"Error al crear la venta: {e}")

    def leer_ventas(self):
        if not self.ventas:
            print("No hay ventas registradas.")
        for venta in self.ventas:
            print(venta)

    def actualizar_venta(self, idproducto, nueva_venta):
        try:
            for i, venta in enumerate(self.ventas):
                if venta.idproducto == idproducto:
                    self.ventas[i] = nueva_venta
                    self.guardar_ventas()
                    print("Venta actualizada:", nueva_venta)
                    return
            print("Venta con ID Producto no encontrada.")
        except Exception as e:
            print(f"Error al actualizar la venta: {e}")

    def eliminar_venta(self, idproducto):
        try:
            for i, venta in enumerate(self.ventas):
                if venta.idproducto == idproducto:
                    del self.ventas[i]
                    self.guardar_ventas()
                    print("Venta eliminada.")
                    return
            print("Venta con ID Producto no encontrada.")
        except Exception as e:
            print(f"Error al eliminar la venta: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    archivo_json = 'ventas.json'
    gestor = GestorVentas(archivo_json)

    try:
        venta1 = VentaOnline("2024-07-24", "Carlos", ["Shampoo", "Jabon"], 101, "Mclean")
        venta2 = VentaLocal("2024-07-24", "Juan", ["Desodorante"], 102, "25mayo")

        gestor.crear_venta(venta1)
        gestor.crear_venta(venta2)

        print("\nListado de ventas:")
        gestor.leer_ventas()

        print("\nActualizando venta...")
        venta_actualizada = VentaOnline("2024-07-24", "Jose", ["bizcochos", "arroz", "jamon"], 111, "45 mayo")
        gestor.actualizar_venta(101, venta_actualizada)

        print("\nListado de ventas después de la actualización:")
        gestor.leer_ventas()

        print("\nEliminando venta...")
        gestor.eliminar_venta(101)

        print("\nListado de ventas después de la eliminación:")
        gestor.leer_ventas()
    except Exception as e:
        print(f"Error general: {e}")
