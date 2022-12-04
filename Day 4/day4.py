print('Leyendo Datos')
with open('Day 4/input.txt') as f:
    lines = f.readlines()
# Uso strip xq sigo lee el final de linea como un caracter extra..

contador = 1
total_repetidos = 0
total_repetidos_p2 = 0

# Funcion que da True si el array 1 es subconjunto del 2 o biceversa
def esSubconjuntode(array1, array2):
  if(set(array1).issubset(set(array2)) or set(array2).issubset(set(array1))):
    return True;
  else:
    return False;

def checkPorCualquierOverlap(array1, array2):
  exit = False
  global total_repetidos_p2
  for x in array1:
    if x in array2:
      total_repetidos_p2 += 1
      exit = True
    if(exit):
      return
      

for stuff in lines:
  linea = stuff.strip()
  first_part = linea.split(',')[0]
  second_part = linea.split(',')[1]
  
  #Obtenemos el rango
  first_range = []
  second_range = []

  # First elf
  start_value = int(first_part.split('-')[0])
  end_value = int(first_part.split('-')[1])
  for x in range(start_value,end_value+1):
    first_range.append(x)
  # Second elf
  start_value = int(second_part.split('-')[0])
  end_value = int(second_part.split('-')[1])
  for x in range(start_value,end_value+1):
    second_range.append(x)

  #print(first_range)
  #print(second_range)
  #Buscamos los repetidos
  if(esSubconjuntode(first_range, second_range)):
    #print(str(contador) + "- Se repiten el task")
    total_repetidos+=1
  #else:
    #print(linea)

  #Parte 2
  checkPorCualquierOverlap(first_range, second_range)

  contador+=1;
#Resultado Final
print("El total de rangos repetidos es: " + str(total_repetidos))
print("El total parte 2 es: " + str(total_repetidos_p2))