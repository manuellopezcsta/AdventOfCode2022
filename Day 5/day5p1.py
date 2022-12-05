print('Leyendo Datos')
with open('Day 5/input.txt') as f:
    lines = f.readlines()
# Uso strip xq sigo lee el final de linea como un caracter extra..
arr1 = []
arr2 = []
arr3 = []
arr4 = []
arr5 = []
arr6 = []
arr7 = []
arr8 = []
arr9 = []

print("Armando Arrays..")
# Armamos de forma crota los array
for x in reversed(range(8)):
  linea = lines[x]
  
  if(linea[1] != " "):
   arr1.append(linea[1])
  if(linea[5] != " "):
   arr2.append(linea[5])
  if(linea[9] != " "):
   arr3.append(linea[9])
  if(linea[13] != " "):
   arr4.append(linea[13])
  if(linea[17] != " "):
   arr5.append(linea[17])
  if(linea[21] != " "):
   arr6.append(linea[21])
  if(linea[25] != " "):
   arr7.append(linea[25])
  if(linea[29] != " "):
   arr8.append(linea[29])
  if(linea[33] != " "):
   arr9.append(linea[33])

# Ahora limpiamos las instrucciones. ind 10 a 511

identificador = [arr1, arr2, arr3, arr4, arr5, arr6, arr7, arr8, arr9]

print("Realizando movimientos..")
for x in range(10,512):
  cant = lines[x].split("move ")[1].split(" from")[0]
  desde = lines[x].split(" from")[1].split(" to")[0]
  hasta = lines[x].split("to ")[1].strip()

  #Manejamos la instruccion
  # Cantidad de movimientos.
  for x in range(int(cant)):
    letra = identificador[int(desde)-1].pop()
    identificador[int(hasta)-1].append(letra)

    
print("Resultado Final p1: ")
print(arr1[-1] + arr2[-1] + arr3[-1] + arr4[-1] + arr5[-1] + arr6[-1] + arr7[-1] + arr8[-1] + arr9[-1])