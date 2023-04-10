print("Bienvenido a lightning Register")
print("Seleccione una opción:")
print("1. Real")
print("2. Simulación")

opcion = int(input("Seleccione una opción: "))

if opcion == 1:
    # Ejecuta el archivo main.py
    exec(open('main.py').read())
elif opcion == 2:
    # Ejecuta el archivo test.py
    exec(open('test.py').read())
else:
    print("Opción no válida")
