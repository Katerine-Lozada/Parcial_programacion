@@ -0,0 +1,161 @@
from datetime import date, timedelta

# ===================== CLASE MATERIAL BIBLIOGRÁFICO =====================
class MaterialBibliografico:
    def __init__(self, codigo, titulo, autor, disponible=True):
        self.codigo = codigo
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible

    def get_codigo(self):
        return self.codigo

    def get_titulo(self):
        return self.titulo

    def get_autor(self):
        return self.autor

    def esta_disponible(self):
        return self.disponible

    def set_disponible(self, disponible):
        self.disponible = disponible

    def tipo_material(self):
        return "Material bibliográfico general"

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"{self.codigo} - {self.titulo} ({self.autor}) [{estado}]"


# ===================== CLASE LIBRO =====================
class Libro(MaterialBibliografico):
    def __init__(self, codigo, titulo, autor, genero):
        super().__init__(codigo, titulo, autor)
        self.genero = genero

    def tipo_material(self):
        return f"Libro - Género: {self.genero}"


# ===================== CLASE REVISTA =====================
class Revista(MaterialBibliografico):
    def __init__(self, codigo, titulo, autor, edicion):
        super().__init__(codigo, titulo, autor)
        self.edicion = edicion

    def tipo_material(self):
        return f"Revista - Edición Nº {self.edicion}"


# ===================== CLASE BIBLIOTECA =====================
class Biblioteca:
    def __init__(self):
        self.inventario = []
        self.prestamos = {}

    def agregar_material(self, material):
        self.inventario.append(material)

    def mostrar_inventario(self):
        print("\n--- INVENTARIO ---")
        if not self.inventario:
            print("No hay materiales en el inventario.")
        else:
            for m in self.inventario:
                print(f"{m} - {m.tipo_material()}")

    def realizar_prestamo(self, codigo):
        for m in self.inventario:
            if m.get_codigo().lower() == codigo.lower():
                if m.esta_disponible():
                    m.set_disponible(False)
                    self.prestamos[codigo] = date.today()
                    print(f"✅ Préstamo realizado: {m.get_titulo()}")
                    print(f"Fecha del préstamo: {date.today()}")
                    print("Debe devolverlo en 7 días.")
                    return
                else:
                    print("❌ Este material ya está prestado.")
                    return
        print("❌ Código no encontrado en el inventario.")

    def realizar_devolucion(self, codigo):
        if codigo in self.prestamos:
            for m in self.inventario:
                if m.get_codigo().lower() == codigo.lower():
                    m.set_disponible(True)
                    fecha_prestamo = self.prestamos.pop(codigo)
                    hoy = date.today()
                    dias_prestamo = (hoy - fecha_prestamo).days

                    print(f"📘 Material devuelto: {m.get_titulo()}")
                    print(f"Días en préstamo: {dias_prestamo}")

                    if dias_prestamo > 7:
                        multa = (dias_prestamo - 7) * 500
                        print(f"⚠️ Multa por retraso: ${multa}")
                    else:
                        print("✅ Devolución sin multas. ¡Gracias!")
                    return
        else:
            print("❌ No hay registro de préstamo con ese código.")

    def mostrar_multas(self):
        print("\n--- MULTAS ACTIVAS ---")
        hoy = date.today()
        hay_multas = False

        for codigo, fecha_prestamo in self.prestamos.items():
            dias = (hoy - fecha_prestamo).days
            if dias > 7:
                multa = (dias - 7) * 500
                for m in self.inventario:
                    if m.get_codigo().lower() == codigo.lower():
                        print(f"{m.get_titulo()} - Retraso: {dias - 7} días - Multa: ${multa}")
                        hay_multas = True
        if not hay_multas:
            print("No hay multas activas.")


# ===================== FUNCIÓN PRINCIPAL =====================
def main():
    biblioteca = Biblioteca()

    # Agregar materiales de ejemplo
    biblioteca.agregar_material(Libro("L001", "Cien Años de Soledad", "García Márquez", "Realismo Mágico"))
    biblioteca.agregar_material(Libro("L002", "El Principito", "Antoine de Saint-Exupéry", "Infantil"))
    biblioteca.agregar_material(Revista("R001", "National Geographic", "Varios", 220))

    while True:
        print("\n===== MENÚ BIBLIOTECA =====")
        print("1. Inventario")
        print("2. Préstamo")
        print("3. Devolución")
        print("4. Multas")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            biblioteca.mostrar_inventario()
        elif opcion == "2":
            codigo = input("Ingrese el código del material a prestar: ")
            biblioteca.realizar_prestamo(codigo)
        elif opcion == "3":
            codigo = input("Ingrese el código del material a devolver: ")
            biblioteca.realizar_devolucion(codigo)
        elif opcion == "4":
            biblioteca.mostrar_multas()
        elif opcion == "5":
            print("👋 Saliendo del sistema... ¡Hasta pronto!")
            break
        else:
            print("❌ Opción no válida, intente nuevamente.")


if __name__ == "__main__":
    main()
