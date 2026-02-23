import xml.etree.ElementTree as ET
import os


class Vuelo:
    def __init__(self, codigo, origen, destino, duracion, aerolinea):
        self.codigo = codigo
        self.origen = origen
        self.destino = destino
        self.duracion = int(duracion)
        self.aerolinea = aerolinea

    def __str__(self):
        return f"Código: {self.codigo}\nOrigen: {self.origen}\nDestino: {self.destino}\nDuración: {self.duracion} horas\nAerolínea: {self.aerolinea}"


class GestorVuelos:
    def __init__(self):
        self.vuelos = []
        self.codigos_existentes = set()

    def cargar_archivo(self, ruta_archivo):
        """Carga y procesa el archivo XML"""
        try:
            if not os.path.exists(ruta_archivo):
                print(f"Error: El archivo '{ruta_archivo}' no existe.")
                return False

            tree = ET.parse(ruta_archivo)
            root = tree.getroot()

            vuelos_cargados = 0
            vuelos_duplicados = 0

            for vuelo_elem in root.findall('vuelo'):
                codigo = vuelo_elem.find('codigo').text

                # Verificar si el código ya existe
                if codigo in self.codigos_existentes:
                    print(f"Advertencia: El vuelo con código {codigo} ya existe. Se omitirá.")
                    vuelos_duplicados += 1
                    continue

                # Crear objeto Vuelo
                vuelo = Vuelo(
                    codigo=codigo,
                    origen=vuelo_elem.find('origen').text,
                    destino=vuelo_elem.find('destino').text,
                    duracion=vuelo_elem.find('duracion').text,
                    aerolinea=vuelo_elem.find('aerolinea').text
                )

                self.vuelos.append(vuelo)
                self.codigos_existentes.add(codigo)
                vuelos_cargados += 1

            print(f"Archivo cargado exitosamente. {vuelos_cargados} vuelos cargados.")
            if vuelos_duplicados > 0:
                print(f"{vuelos_duplicados} vuelos duplicados omitidos.")

            return True

        except ET.ParseError:
            print("Error: El archivo no tiene un formato XML válido.")
            return False
        except Exception as e:
            print(f"Error inesperado al cargar el archivo: {e}")
            return False

    def buscar_vuelo(self, codigo):
        """Busca un vuelo por su código"""
        for vuelo in self.vuelos:
            if vuelo.codigo == codigo:
                return vuelo
        return None

    def mostrar_detalle_vuelo(self, codigo):
        """Muestra el detalle de un vuelo específico"""
        vuelo = self.buscar_vuelo(codigo)
        if vuelo:
            print("\n" + "=" * 50)
            print("DETALLE DEL VUELO")
            print("=" * 50)
            print(vuelo)
            print("=" * 50)
        else:
            print(f"No se encontró ningún vuelo con el código '{codigo}'.")

    def agrupar_por_aerolinea(self):
        """Agrupa los vuelos por aerolínea"""
        if not self.vuelos:
            print("No hay vuelos cargados.")
            return

        grupos = {}
        for vuelo in self.vuelos:
            if vuelo.aerolinea not in grupos:
                grupos[vuelo.aerolinea] = []
            grupos[vuelo.aerolinea].append(vuelo.codigo)

        print("\n" + "=" * 50)
        print("VUELOS AGRUPADOS POR AEROLÍNEA")
        print("=" * 50)

        for aerolinea, codigos in grupos.items():
            print(f"\n{aerolinea}:")
            for codigo in codigos:
                print(f"  - {codigo}")

    def ordenar_por_duracion_desc(self):
        """Ordena los vuelos por duración de mayor a menor"""
        if not self.vuelos:
            print("No hay vuelos cargados.")
            return

        vuelos_ordenados = sorted(self.vuelos, key=lambda x: x.duracion, reverse=True)

        print("\n" + "=" * 50)
        print("VUELOS ORDENADOS POR DURACIÓN (MAYOR A MENOR)")
        print("=" * 50)

        for vuelo in vuelos_ordenados:
            print(f"Código: {vuelo.codigo} - Duración: {vuelo.duracion} horas - {vuelo.aerolinea}")


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n" + "=" * 50)
    print("SISTEMA DE GESTIÓN DE VUELOS")
    print("=" * 50)
    print("1. Cargar Archivo XML")
    print("2. Detalle de vuelo específico")
    print("3. Agrupar vuelos por aerolínea")
    print("4. Ordenar de mayor a menor duración")
    print("5. Salir")
    print("=" * 50)


def main():
    gestor = GestorVuelos()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-5): ").strip()

        if opcion == '1':
            ruta = input("Ingrese la dirección del archivo XML: ").strip()
            gestor.cargar_archivo(ruta)

        elif opcion == '2':
            if not gestor.vuelos:
                print("Primero debe cargar un archivo de vuelos.")
                continue

            codigo = input("Ingrese el código del vuelo: ").strip()
            gestor.mostrar_detalle_vuelo(codigo)

        elif opcion == '3':
            gestor.agrupar_por_aerolinea()

        elif opcion == '4':
            gestor.ordenar_por_duracion_desc()

        elif opcion == '5':
            print("¡Gracias por usar el sistema!")
            break

        else:
            print("Opción no válida. Por favor, seleccione una opción del 1 al 5.")

        input("\nPresione Enter para continuar...")


if __name__ == "__main__":
    main()