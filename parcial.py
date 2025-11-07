# Parcial_programacion
# ============================================================
# ASIGNATURA : PROGRAMACIÓN ORIENTADA A OBJETOS
# NOMBRE : Gipsi Katerine Lozada Zabaleta, Juan Diego Zapata Pulido, Alisson Tatiana Hernández Ortiz 
# CÓDIGO : 
# FECHA : 21/10/2025
# ============================================================
# Aplicativo: Gestión de Biblioteca
# Características:
# - Usa clases, objetos, herencia, encapsulamiento y polimorfismo
# - Permite gestionar: inventario, préstamo, devolución y multas
# ============================================================

from datetime import datetime, timedelta

# ------------------------------------------------------------
# CLASE BASE: MaterialBibliografico
# ------------------------------------------------------------
# Representa un material general (libro, revista, etc.)
# Usa encapsulamiento con atributos privados (__)
# ------------------------------------------------------------
class MaterialBibliografico:
    def __init__(self, codigo, titulo, autor, disponible=True):
        self.__codigo = codigo          # Atributo privado (encapsulamiento)
        self.__titulo = titulo          # Atributo privado
        self.__autor = autor            # Atributo privado
        self.__disponible = disponible  # Atributo privado

    # Métodos getter y setter para acceder a los atributos privados
    def get_codigo(self):
        return self.__codigo

    def get_titulo(self):
        return self.__titulo

    def get_autor(self):
        return self.__autor

    def esta_disponible(self):
        return self.__disponible

    def set_disponible(self, estado):
        self.__disponible = estado

    # Método polimórfico (puede redefinirse en clases hijas)
    def tipo_material(self):
        return "Material bibliográfico general"

    def __str__(self):
        estado = "Disponible" if self.__disponible else "Prestado"
        return f"{self.__codigo} - {self.__titulo} ({self.__autor}) [{estado}]"


# ------------------------------------------------------------
# CLASE HIJA: Libro (Hereda de MaterialBibliografico)
# ------------------------------------------------------------
class Libro(MaterialBibliografico):
    def __init__(self, codigo, titulo, autor, genero):
        super().__init__(codigo, titulo, autor)
        self.genero = genero

    # Polimorfismo: redefinición del método tipo_material
    def tipo_material(self):
        return f"Libro - Género: {self.genero}"


# ------------------------------------------------------------
# CLASE HIJA: Revista (Hereda de MaterialBibliografico)
# ------------------------------------------------------------
class Revista(MaterialBibliografico):
    def __init__(self, codigo, titulo, autor, edicion):
        super().__init__(codigo, titulo, autor)
        self.edicion = edicion

    # Polimorfismo: redefinición del método tipo_material
    def tipo_material(self):
        return f"Revista - Edición Nº {self.edicion}"


# ------------------------------------------------------------
# CLASE PRINCIPAL: Biblioteca
# ------------------------------------------------------------
class Biblioteca:
    def __init__(self):
        # Inventario almacenado como lista de materiales
        self.inventario = []
        # Diccionario para guardar préstamos (código → fecha)
        self.prestamos = {}

    # Método para agregar materiales al inventario
    def agregar_material(self, material):
        self.inventario.append(material)

    # Mostrar el inventario actual
    def mostrar_inventario(self):
        print("\n--- INVENTARIO ---")
        if not self.inventario:
            print("No hay materiales en el inventario.")
        else:
            for m in self.inventario:
                print(m, "-", m.tipo_material())

    # Realizar préstamo de material
    def realizar_prestamo(self, codigo):
        for m in self.inventario:
            if m.get_codigo() == codigo:
                if m.esta_disponible():
                    m.set_disponible(False)
                    fecha_prestamo = datetime.now()
                    self.prestamos[codigo] = fecha_prestamo
                    print(f"✅ Préstamo realizado: {m.get_titulo()}")
                    print(f"Fecha del préstamo: {fecha_prestamo.strftime('%d/%m/%Y')}")
                    print("Debe devolverlo en 7 días.")
                    return
                else:
                    print("❌ Este material ya está prestado.")
                    return
        print("❌ Código no encontrado en el inventario.")

    # Realizar devolución de material
    def realizar_devolucion(self, codigo):
        if codigo in self.prestamos:
            for m in self.inventario:
                if m.get_codigo() == codigo:
                    m.set_disponible(True)
                    fecha_prestamo = self.prestamos.pop(codigo)
                    fecha_devolucion = datetime.now()
                    dias_prestamo = (fecha_devolucion - fecha_prestamo).days

                    print(f"📘 Material devuelto: {m.get_titulo()}")
                    print(f"Días en préstamo: {dias_prestamo} día(s)")

                    if dias_prestamo > 7:
                        multa = (dias_prestamo - 7) * 500
                        print(f"⚠️ Multa por retraso: ${multa}")
                    else:
                        print("✅ Devolución sin multas. ¡Gracias!")
                    return
        print("❌ No hay registro de préstamo con ese código.")

    # Calcular multas activas
    def mostrar_multas(self):
        print("\n--- MULTAS ACTIVAS ---")
        hoy = datetime.now()
        hay_multas = False
        for codigo, fecha_prestamo in self.prestamos.items():
            dias_prestamo = (hoy - fecha_prestamo).days
            if dias_prestamo > 7:
                multa = (dias_prestamo - 7) * 500
                for m in self.inventario:
                    if m.get_codigo() == codigo:
                        print(f"{m.get_titulo()} - Retraso: {dias_prestamo - 7} días - Multa: ${multa}")
                        hay_multas = True
        if not hay_multas:
            print("No hay multas activas.")


# ------------------------------------------------------------
# FUNCIÓN PRINCIPAL (MENÚ)
# ------------------------------------------------------------
def menu():
    biblioteca = Biblioteca()

    # Materiales de ejemplo
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

        # Python 3.10+: match-case (equivalente al switch)
        opcion = input("Seleccione una opción: ")

        match opcion:
            case "1":
                biblioteca.mostrar_inventario()
            case "2":
                codigo = input("Ingrese el código del material a prestar: ")
                biblioteca.realizar_prestamo(codigo)
            case "3":
                codigo = input("Ingrese el código del material a devolver: ")
                biblioteca.realizar_devolucion(codigo)
            case "4":
                biblioteca.mostrar_multas()
            case "5":
                print("👋 Saliendo del sistema... ¡Hasta pronto!")
                break
            case _:
                print("❌ Opción no válida, intente nuevamente.")


# ------------------------------------------------------------
# EJECUCIÓN PRINCIPAL
# ------------------------------------------------------------
if __name__ == "__main__":
    menu()
