def calcular_costo_envio(ciudad_origen, ciudad_destino, tipo_envio, paquetes):
    costos_por_kilo = {
        ("Cali", "Bogota"): 20000,
        ("Cali", "Medellin"): 20000,
        ("Cali", "Cartagena"): 35000,
        ("Cali", "Santa Marta"): 35000,
        ("Cali", "Barranquilla"): 35000,
        ("Cali", "Otra Ciudad"): 36500,
        ("Bogota", "Cali"): 20000,
        ("Medellin", "Cali"): 20000,
        ("Cartagena", "Cali"): 35000,
        ("Santa Marta", "Cali"): 35000,
        ("Barranquilla", "Cali"): 35000,
        ("Otra Ciudad", "Cali"): 36500
    }

    
    porcentaje_rapido = 0.1
    porcentaje_extra_rapido = 0.25

    costo_total = 0

    if (ciudad_origen, ciudad_destino) in costos_por_kilo:
        costo_por_kilo = costos_por_kilo[(ciudad_origen, ciudad_destino)]

        for peso in paquetes:
            costo_total += peso * costo_por_kilo

        if tipo_envio == "rápido" or "rapido":
            costo_total *= 1 + porcentaje_rapido
        elif tipo_envio == "extra rápido" or "extra rapido":
            costo_total *= 1 + porcentaje_extra_rapido

        return costo_total
    else:
        return "La combinación de ciudades no tiene un costo definido."

contador_envios = 0

while True:
    print("Ingrese los datos del envío:")
    ciudad_origen= input("Ciudad de origen: ")
    ciudad_destino = input("Ciudad de destino: ")
    tipo_envio = input("Tipo de envío (normal, rapido, extra rapido): ")
    num_paquetes = int(input("Número de paquetes: "))
    date = input("Fecha de envio: ")
    name_origin = input("Digite el nombre del remitente: ")
    name_dest = input("Digite el nombre del destinatario: ")
    num_origin = input("Digite el numero del remitente: ")    
    name_dest = input("Digite el numero del destinatario: ")  
    adr = input("Digite la dirección del destinatario: ")
    contador_envios += 1
    
    paquetes = []
    for i in range(num_paquetes):
        peso = float(input(f"Peso del paquete {i + 1} (en kilos): "))
        paquetes.append(peso)

    costo_total_envio = calcular_costo_envio(ciudad_origen, ciudad_destino, tipo_envio, paquetes)
    print(f"El costo total del envío {contador_envios} es: ${costo_total_envio}")

    continuar = input("¿Desea calcular otro envío? (s/n): ")
    if continuar.lower() != "s":
        print("Gracias por usar el sistema de cálculo de envíos.")
        break
