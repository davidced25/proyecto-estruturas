# SISTEMA DE GESTION DE EMPLEADOS - VERSION 2
# Proyecto de estructura de datos - Tercer semestre
# Implementacion con Lista Doblemente Enlazada Circular + Arbol AVL
#
# Integrante 1: David Santiago Cediel Remolina - 2250933
# Integrante 2: David Santiago Gomez Caicedo   - 2252119
# Integrante 3: Daniel Andres Floraz Duran     - 2251786
# Integrante 4: Alejandro Ramirez Mejia        - 2250930
# Integrante 5: Mateo Amaya                    - 2250921

import re  # se usa para validar que el nombre solo tenga letras y espacios


# Parte original del proyecto
# Lista doblemente enlazada circular
# Esta fue la estructura principal de la entrega 1
# Aqui se guardan todos los empleados de forma ordenada
# y se puede recorrer tanto hacia adelante como hacia atras

class Nodo:
    # Nodo de la lista doblemente enlazada circular
    # Guarda la informacion basica de un empleado
    def __init__(self, id_empleado, nombre, cargo, zona_acceso):
        self.id_empleado = id_empleado
        self.nombre = nombre
        self.cargo = cargo
        self.zona_acceso = zona_acceso
        self.anterior = None
        self.siguiente = None


class ListaEmpleados:
    # Lista doblemente enlazada circular donde se almacenan
    # todos los empleados del sistema

    def __init__(self):
        self.cabeza = None   # primer nodo de la lista
        self.cantidad = 0    # numero total de empleados

    def esta_vacia(self):
        # revisa si no hay ningun nodo en la lista
        return self.cabeza is None

    def contar_empleados(self):
        # retorna cuantos empleados hay guardados
        return self.cantidad

    def imprimir_lista(self):
        # muestra todos los empleados recorriendo la lista circular
        if self.esta_vacia():
            print("\nNo hay empleados registrados.")
            return

        print("\nLista de empleados:")
        nodo_actual = self.cabeza
        contador = 1

        # se usa while True porque la lista es circular
        while True:
            print(f"\nEmpleado #{contador}")
            print(f"ID     : {nodo_actual.id_empleado}")
            print(f"Nombre : {nodo_actual.nombre}")
            print(f"Cargo  : {nodo_actual.cargo}")
            print(f"Zona   : {nodo_actual.zona_acceso}")

            nodo_actual = nodo_actual.siguiente
            contador += 1

            # cuando vuelve al inicio, ya recorrio toda la lista
            if nodo_actual == self.cabeza:
                break

        print(f"\nTotal de empleados: {self.cantidad}")

    def id_existe(self, id_empleado):
        # revisa si ya hay un empleado con ese ID
        if self.esta_vacia():
            return False

        nodo_actual = self.cabeza
        while True:
            if nodo_actual.id_empleado == id_empleado:
                return True

            nodo_actual = nodo_actual.siguiente

            if nodo_actual == self.cabeza:
                break

        return False

    def validar_nombre(self, nombre):
        # valida que el nombre no este vacio y solo tenga letras y espacios
        if nombre.strip() == "":
            return False

        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s]+$"
        return re.match(patron, nombre) is not None

    def agregar_al_inicio(self, id_empleado, nombre, cargo, zona_acceso):
        # primero se revisa que los datos esten completos y sean validos
        if id_empleado is None or id_empleado.strip() == "":
            print("\nEl ID no puede estar vacio.")
            return False

        if self.id_existe(id_empleado):
            print(f"\nYa existe un empleado con ID '{id_empleado}'.")
            return False

        if not self.validar_nombre(nombre):
            print(f"\nNombre invalido: '{nombre}'.")
            return False

        if cargo is None or cargo.strip() == "":
            print("\nEl cargo no puede estar vacio.")
            return False

        if zona_acceso is None or zona_acceso.strip() == "":
            print("\nLa zona de acceso no puede estar vacia.")
            return False

        nuevo_nodo = Nodo(id_empleado, nombre, cargo, zona_acceso)

        # si la lista esta vacia, el nodo se apunta a si mismo
        if self.esta_vacia():
            nuevo_nodo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = nuevo_nodo
            self.cabeza = nuevo_nodo
        else:
            # si ya existe lista, se inserta al inicio y se ajustan enlaces
            ultimo_nodo = self.cabeza.anterior

            nuevo_nodo.siguiente = self.cabeza
            nuevo_nodo.anterior = ultimo_nodo

            self.cabeza.anterior = nuevo_nodo
            ultimo_nodo.siguiente = nuevo_nodo

            self.cabeza = nuevo_nodo

        self.cantidad += 1
        print(f"\nEmpleado '{nombre}' agregado correctamente.")
        return True

    def buscar_por_id(self, id_buscado):
        # busca recorriendo toda la lista hasta encontrar el ID
        if self.esta_vacia():
            print("\nLa lista esta vacia.")
            return None

        if id_buscado is None or id_buscado.strip() == "":
            print("\nEl ID a buscar no puede estar vacio.")
            return None

        nodo_actual = self.cabeza
        while True:
            if nodo_actual.id_empleado == id_buscado:
                print("\nEmpleado encontrado:")
                print(f"ID     : {nodo_actual.id_empleado}")
                print(f"Nombre : {nodo_actual.nombre}")
                print(f"Cargo  : {nodo_actual.cargo}")
                print(f"Zona   : {nodo_actual.zona_acceso}")
                return nodo_actual

            nodo_actual = nodo_actual.siguiente

            if nodo_actual == self.cabeza:
                break

        print(f"\nNo se encontro ningun empleado con ID: {id_buscado}")
        return None


# Parte agregada en la version 2
# Arbol AVL indexado por nombre
# Esta parte se agrego para mejorar la busqueda por nombre
# La idea es que la lista siga siendo la estructura principal
# pero el AVL funcione como un indice rapido por nombre
#
# Ventajas de esta parte nueva:
# - Buscar por nombre o fragmento de nombre
# - Mostrar empleados en orden alfabetico
# - Mantener el arbol balanceado para que no se degrade

class NodoAVL:
    # Nodo del arbol AVL
    # La clave se guarda en minusculas para comparar sin importar
    # si el usuario escribe mayusculas o minusculas
    def __init__(self, nombre, datos_empleado):
        self.clave = nombre.lower()
        self.nombre = nombre
        self.empleados = [datos_empleado]
        self.izq = None
        self.der = None
        self.altura = 1


class ArbolAVL:
    # Arbol AVL usado como indice por nombre
    # Permite insertar, buscar por fragmento y listar en orden alfabetico

    def __init__(self):
        self.raiz = None

    def _altura(self, nodo):
        # devuelve la altura del nodo o 0 si no existe
        return nodo.altura if nodo else 0

    def _balance(self, nodo):
        # calcula el factor de balance de un nodo
        return self._altura(nodo.izq) - self._altura(nodo.der) if nodo else 0

    def _actualizar_altura(self, nodo):
        # recalcula la altura despues de insertar o rotar
        nodo.altura = 1 + max(self._altura(nodo.izq), self._altura(nodo.der))

    def _rotar_derecha(self, y):
        # rotacion simple a la derecha
        x = y.izq
        T2 = x.der

        x.der = y
        y.izq = T2

        self._actualizar_altura(y)
        self._actualizar_altura(x)
        return x

    def _rotar_izquierda(self, x):
        # rotacion simple a la izquierda
        y = x.der
        T2 = y.izq

        y.izq = x
        x.der = T2

        self._actualizar_altura(x)
        self._actualizar_altura(y)
        return y

    def _balancear(self, nodo, clave):
        # revisa si el nodo quedo desbalanceado despues de insertar
        self._actualizar_altura(nodo)
        bal = self._balance(nodo)

        # caso izquierda izquierda
        if bal > 1 and clave < nodo.izq.clave:
            return self._rotar_derecha(nodo)

        # caso derecha derecha
        if bal < -1 and clave > nodo.der.clave:
            return self._rotar_izquierda(nodo)

        # caso izquierda derecha
        if bal > 1 and clave > nodo.izq.clave:
            nodo.izq = self._rotar_izquierda(nodo.izq)
            return self._rotar_derecha(nodo)

        # caso derecha izquierda
        if bal < -1 and clave < nodo.der.clave:
            nodo.der = self._rotar_derecha(nodo.der)
            return self._rotar_izquierda(nodo)

        return nodo

    def _insertar(self, nodo, nombre, datos_empleado):
        clave = nombre.lower()

        # si no hay nodo, se crea uno nuevo
        if nodo is None:
            return NodoAVL(nombre, datos_empleado)

        # segun la clave se va a la izquierda o derecha
        if clave < nodo.clave:
            nodo.izq = self._insertar(nodo.izq, nombre, datos_empleado)
        elif clave > nodo.clave:
            nodo.der = self._insertar(nodo.der, nombre, datos_empleado)
        else:
            # si el nombre ya existe, se guarda en la misma lista
            nodo.empleados.append(datos_empleado)
            return nodo

        # despues de insertar, se revisa si hace falta balancear
        return self._balancear(nodo, clave)

    def insertar(self, nombre, datos_empleado):
        # punto de entrada publico para insertar en el arbol
        self.raiz = self._insertar(self.raiz, nombre, datos_empleado)

    def _buscar_fragmento(self, nodo, fragmento, resultados):
        # recorrido en orden para conservar el orden alfabetico
        if nodo is None:
            return

        self._buscar_fragmento(nodo.izq, fragmento, resultados)

        # si el fragmento aparece dentro del nombre, se agrega
        if fragmento in nodo.clave:
            for emp in nodo.empleados:
                resultados.append(emp)

        self._buscar_fragmento(nodo.der, fragmento, resultados)

    def buscar_por_nombre(self, texto):
        # busca coincidencias por nombre completo o parcial
        fragmento = texto.strip().lower()
        resultados = []
        self._buscar_fragmento(self.raiz, fragmento, resultados)
        return resultados

    def _inorden(self, nodo, lista):
        # recorrido inorden para obtener el arbol en orden alfabetico
        if nodo is None:
            return

        self._inorden(nodo.izq, lista)

        for emp in nodo.empleados:
            lista.append(emp)

        self._inorden(nodo.der, lista)

    def listar_alfabetico(self):
        # retorna todos los empleados ordenados de A a Z
        lista = []
        self._inorden(self.raiz, lista)
        return lista


# Menu y programa principal
# Aqui se juntan las dos estructuras para trabajar en conjunto:
# la lista guarda los datos y el AVL ayuda a buscar por nombre

def mostrar_menu():
    print("\nSistema de gestion de empleados")
    print("1. Verificar si la lista esta vacia")
    print("2. Contar empleados registrados")
    print("3. Ver todos los empleados")
    print("4. Agregar nuevo empleado")
    print("5. Buscar empleado por ID")
    print("6. Cargar datos de ejemplo")
    print("7. Buscar empleados por nombre")
    print("8. Ver empleados en orden alfabetico")
    print("0. Salir")
    print("Seleccione una opcion: ", end="")


def cargar_datos_ejemplo(lista, avl):
    # Carga empleados de ejemplo en las dos estructuras
    # Primero se guarda en la lista y luego en el AVL
    empleados_ejemplo = [
        ("E001", "Carlos Ramirez", "Gerente", "Edificio A - Piso 3"),
        ("E002", "Ana Torres", "Desarrolladora", "Edificio B - Piso 1"),
        ("E003", "Luis Gomez", "Seguridad", "Edificio A - Entrada"),
        ("E004", "Maria Perez", "Contabilidad", "Edificio C - Piso 2"),
        ("E005", "Jorge Mendoza", "Sistemas", "Edificio B - Piso 2"),
        ("E006", "Sofia Castillo", "Recursos H.", "Edificio C - Piso 1"),
        ("E007", "Andres Vargas", "Seguridad", "Edificio A - Entrada"),
        ("E008", "Camila Herrera", "Desarrolladora", "Edificio B - Piso 1"),
    ]

    for eid, nombre, cargo, zona in empleados_ejemplo:
        agregado = lista.agregar_al_inicio(eid, nombre, cargo, zona)
        if agregado:
            # solo se inserta en el AVL si se pudo agregar en la lista
            avl.insertar(nombre, {
                "id": eid,
                "nombre": nombre,
                "cargo": cargo,
                "zona": zona
            })

    print("\nDatos de ejemplo cargados correctamente en lista y arbol AVL.")


def mostrar_empleado(emp):
    # imprime un empleado con el mismo formato en todo el programa
    print(f"  ID     : {emp['id']}")
    print(f"  Nombre : {emp['nombre']}")
    print(f"  Cargo  : {emp['cargo']}")
    print(f"  Zona   : {emp['zona']}")


def main():
    lista = ListaEmpleados()
    avl = ArbolAVL()

    print("\nBienvenido al Sistema de Gestion de Empleados - Version 2")
    print("Empresa: Control de Accesos y Zonas")

    while True:
        mostrar_menu()
        opcion = input().strip()

        # opciones de la lista original
        if opcion == "1":
            if lista.esta_vacia():
                print("\nLa lista SI esta vacia. No hay empleados registrados.")
            else:
                print(f"\nLa lista NO esta vacia. Hay {lista.contar_empleados()} empleado(s).")

        elif opcion == "2":
            print(f"\n[INFO] Total de empleados: {lista.contar_empleados()}")

        elif opcion == "3":
            lista.imprimir_lista()

        elif opcion == "4":
            print("\nAgregar nuevo empleado")
            id_emp = input("ID del empleado: ").strip()
            nombre = input("Nombre completo: ").strip()
            cargo = input("Cargo: ").strip()
            zona = input("Zona de acceso: ").strip()

            if id_emp and nombre and cargo and zona:
                agregado = lista.agregar_al_inicio(id_emp, nombre, cargo, zona)
                if agregado:
                    # si se agrego en la lista, tambien se guarda en el AVL
                    avl.insertar(nombre, {
                        "id": id_emp,
                        "nombre": nombre,
                        "cargo": cargo,
                        "zona": zona
                    })
            else:
                print("\nTodos los campos son obligatorios.")

        elif opcion == "5":
            print("\nBuscar por ID")
            id_buscar = input("ID a buscar (ej: E003): ").strip()
            lista.buscar_por_id(id_buscar)

        elif opcion == "6":
            cargar_datos_ejemplo(lista, avl)

        # opciones nuevas del AVL
        elif opcion == "7":
            print("\nBuscar por nombre")
            print("Ingrese el nombre o un fragmento del nombre")
            print("(ejemplo: ana, gomez, car): ", end="")
            texto = input().strip()

            if texto == "":
                print("\nDebe ingresar al menos un caracter para buscar.")
            else:
                resultados = avl.buscar_por_nombre(texto)

                if resultados:
                    print(f"\nSe encontraron {len(resultados)} resultado(s) para '{texto}':")
                    print("Resultados ordenados alfabeticamente")
                    print("")

                    for i, emp in enumerate(resultados, 1):
                        print(f"\nResultado #{i}")
                        mostrar_empleado(emp)
                else:
                    print(f"\nNo se encontro ningun empleado con '{texto}' en el nombre.")

            print("\nVENTAJA DEL ARBOL AVL:")
            print("La busqueda recorre el arbol de forma ordenada.")
            print("Los resultados ya vienen en orden A->Z sin ordenar despues.")
            print("Con la lista de la entrega 1, habia que recorrer toda la lista.")

        elif opcion == "8":
            print("\nEmpleados en orden alfabetico")
            empleados_ordenados = avl.listar_alfabetico()

            if not empleados_ordenados:
                print("\nNo hay empleados en el arbol. Agregue o cargue datos primero.")
            else:
                print(f"\nTotal: {len(empleados_ordenados)} empleado(s) ordenados A->Z:\n")
                for i, emp in enumerate(empleados_ordenados, 1):
                    print(f"  {i:>2}. [{emp['id']}] {emp['nombre']:<20} | {emp['cargo']:<16} | {emp['zona']}")

            print("\nVENTAJA DEL ARBOL AVL:")
            print("El recorrido InOrden del arbol entrega los nombres en orden alfabetico.")
            print("Con la lista enlazada, primero habia que ordenar los datos.")

        elif opcion == "0":
            print("\nHasta luego. El sistema ha sido cerrado.\n")
            break

        else:
            print("\nOpcion invalida. Ingrese un numero del 0 al 8.")


if __name__ == "__main__":
    main()