import functions as f

N = 1000 # Número de conjuntos de prendas a generar

# Outfit = 
outfitSet = []
for i in range(N):
    outfit = [] # Nuevo outfit
    
    # Determinar si el conjunto de prendas poseerá sombrero
    hasHat = f.hasHat()
    if hasHat:
        hat = f.randomHat()
        outfit.append(hat)

    firstLayer = f.randomFirstLayer()
    outfit.append(firstLayer)

    # Determina de manera probabilista si es que se utilizará segunda y/o tercera capa
    hasSecondLayer, hasThirdLayer = f.hasLayers()
    if hasSecondLayer:
        secondLayer = f.randomSecondLayer()
        outfit.append(secondLayer)
    
    if hasThirdLayer:
        thirdLayer = f.randomThirdLayer()
        outfit.append(thirdLayer)
    
    # Agrega la parte inferior del conjunto
    pants = f.randomLowerbody()
    outfit.append(pants)

    # Agrega el par de zapatos para el conjunto de prendas.
    shoes = f.randomShoes()
    outfit.append(shoes)
    outfitSet.append( outfit ) 



total = len(outfitSet)
print(f"Generados de manera exitosa un total de {total} atuendos")
mainFlag = True
while mainFlag:
    print("¿Qué desea hacer?")
    print("1. Visualizar vestuario por Id")
    print("2. Subir conjuntos a la Base de Datos")
    print("3. Salir")
    opcion = int(input("Ingrese una opción: "))
    if opcion == 1:
        flag = True
        while flag:
            id = int(input("Ingrese un número válido de outfit para visualizarlo (0 para salir): "))
            flag = f.showOutfit(id, outfitSet)
    elif opcion == 2:
        result = f.insertOutfitsIntoTable(outfitSet)
        if result:
            print("Subida exitosa")
        else:
            print("Ocurrió un error")
    elif opcion == 3:
        mainFlag = False
    else:
        print("Ingrese una opción válida")

print("- Programa finalizado.")    




















"""
# Determina si el conjunto de prendas poseerá una prenda de primera capa de tipo FullBody
hasFullBody = f.hasFullBody()
if (hasFullBody):
    firstLayer = f.randomFullBody()
else:
    # Si el resultado es negativo, el conjunto poseerá una prenda de primera capa de tipo UpperBody
    firstLayer = f.randomShirt()
outfit.append(firstLayer)
"""