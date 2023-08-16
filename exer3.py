def obtener_datos_docente():
    nombre = input("Ingrese el nombre del docente: ")
    apellido = input("Ingrese el apellido del docente: ")
    direccion = input("Ingrese la dirección del docente: ")
    tiene_pregrado = input("¿Tiene título de pregrado? (S/N): ").upper() == "S"
    tiene_especialista = input("¿Tiene título de especialista? (S/N): ").upper() == "S"
    tiene_maestria = input("¿Tiene título de maestría? (S/N): ").upper() == "S"
    tiene_doctorado = input("¿Tiene título de doctorado? (S/N): ").upper() == "S"
    años_experiencia = int(input("Ingrese la cantidad de años de experiencia: "))
    departamento = input("Ingrese el nombre del departamento al que pertenece: ")
    return nombre, apellido, direccion, tiene_pregrado, tiene_especialista, tiene_maestria, tiene_doctorado, años_experiencia, departamento


def obtener_datos_publicacion(numero_publicacion):
    titulo = input(f"Ingrese el título de la publicación {numero_publicacion}: ")
    año = int(input("Ingrese el año de publicación: "))
    numero_autores = int(input("Ingrese el número de autores: "))
    tipo_publicacion = input("Ingrese el tipo de publicación (L/CL/AA/A): ").upper()
    valoracion_evaluador = int(input("Ingrese la valoración del evaluador (1/2/3): "))
    return titulo, año, numero_autores, tipo_publicacion, valoracion_evaluador


def calcular_puntos_publicacion(tipo_publicacion, valoracion_evaluador):
    if tipo_publicacion in ["L", "CL"]:
        if valoracion_evaluador == 1:
            return 20
        else:
            return 14
    elif tipo_publicacion == "AA":
        return 16
    elif tipo_publicacion == "A":
        if valoracion_evaluador == 3:
            return 4
        else:
            return 10


def obtener_puntos_titulos(tiene_pregrado, tiene_especialista, tiene_maestria, tiene_doctorado):
    puntos = 0
    if tiene_pregrado:
        puntos += 10
    if tiene_especialista:
        puntos += 50
    if tiene_maestria:
        puntos += 100
    if tiene_doctorado:
        puntos += 140
    return puntos


def obtener_categoria(puntos_totales):
    if puntos_totales < 150:
        return "Instructor"
    elif 150 <= puntos_totales < 250:
        return "Asistente"
    elif 250 <= puntos_totales < 350:
        return "Asociado"
    else:
        return "Titular"


def mostrar_info_docente(nombre, apellido, departamento, puntos_totales):
    categoria = obtener_categoria(puntos_totales)
    print(f"Nombre: {nombre} {apellido}")
    print(f"Departamento: {departamento}")
    print(f"Categoría: {categoria}")


def mostrar_info_publicaciones(nombre, apellido, publicaciones):
    print(f"Publicaciones de {nombre} {apellido}:")
    for publicacion in publicaciones:
        titulo, tipo, puntos = publicacion
        print(f"- Título: {titulo}")
        print(f"  Tipo: {tipo}")
        print(f"  Puntos asignados: {puntos}")


def main():
    docente_data = obtener_datos_docente()
    publicaciones = []


    cantidad_publicaciones = int(input("Ingrese la cantidad de publicaciones: "))
    for i in range(1, cantidad_publicaciones + 1):
        publicacion_data = obtener_datos_publicacion(i)
        puntos_publicacion = calcular_puntos_publicacion(publicacion_data[3], publicacion_data[4])
        publicaciones.append((publicacion_data[0], publicacion_data[3], puntos_publicacion))


    puntos_titulos = obtener_puntos_titulos(*docente_data[3:7])
    puntos_experiencia = docente_data[7] * 10
    puntos_totales = sum([puntos_titulos, puntos_experiencia] + [p[2] for p in publicaciones])


    mostrar_info_docente(docente_data[0], docente_data[1], docente_data[8], puntos_totales)
    mostrar_info_publicaciones(docente_data[0], docente_data[1], publicaciones)


if __name__ == "__main__":
    main()
