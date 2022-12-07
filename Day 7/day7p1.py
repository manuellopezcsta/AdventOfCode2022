print('Leyendo Datos')
with open('Day 7/input.txt') as f:
  lines = f.readlines()

current_dir = "/"
eldisco = {}
eldisco_pesos = {}
adding_files = False


def ReadInstruction(linea, current_dir):
  global adding_files
  if (linea == "$ cd /"):
    current_dir = "/"
    #We check if its a command
  elif(linea.startswith("$ ")):
    command = linea.split("$ ")[1]
    adding_files = False
    #print(command)
    if(command == "ls"):
      adding_files = True

    if(command.startswith("cd ")):
      new_dir = command.split("cd ")[1]
      #print(new_dir)
      if(new_dir == ".."):
        #Codigo para ir pa atras.
        holder = ""
        holder = holder + (current_dir[0:-1])
        #print(holder)
        index = holder.rfind("/")
        holder = holder[0:index]
        #print(index)
        #print("NEW: " + holder + "   OLD: " + current_dir)
        
        current_dir = holder
        #print(current_dir + "\r")
      else:
        #Agregamos al directorio.
        current_dir = current_dir + "/" + new_dir + "/"
        current_dir = current_dir.replace("//","/")
        current_dir = "/" + current_dir
        #print(current_dir)

  # Hasta aca parte de comandos
  elif(adding_files):
      #Si es un directorio
    if(linea.startswith("dir ")):
      cosa = linea.split("dir ")[1]
      #Sino es un archivo con peso
    else:
      # Es un archivo
      cosa = int(linea.split(" ")[0])
      #Creamos el directorio si no existe
    if(current_dir not in eldisco):
      #print("se creo nuevo dir")
      eldisco[current_dir] = []
    
    #Si existe, le agregamos la cosa
    eldisco[current_dir].append(cosa)
  return current_dir
    
      

# Armamos el disco
for stuff in lines:
  linea = stuff.strip()
  current_dir = ReadInstruction(linea, current_dir)

# Sumamos los archivos ? / Armamos el peso de cada dir
for x in eldisco:
  # is the key
  suma_archivos_carpeta = 0
  eldisco_pesos[x] = 0
  for j in eldisco[x]:    
    #Archivo
    if(type(j) == int):
      suma_archivos_carpeta += j
  eldisco_pesos[x] = suma_archivos_carpeta

#print(eldisco["//wlqhpwqv/ppf/tfjnj/vljqlw/pjqwq/vwp/"])

# Sumamos las carpetas con carpetas adentro
for x in eldisco_pesos:
  peso_de_x = eldisco_pesos[x]
  #print(x, " PESA ", eldisco_pesos[x], "TIENE", eldisco[x])
  if(eldisco_pesos[x] <= 100000):
    for j in eldisco:
      #Si tiene una key que existe le sumamos
      #if((x + str(j) +"/") in eldisco.keys()):

      if str(j).startswith(x) and str(j)!= x:
        # Si j es una subcarpeta
        peso_de_x += eldisco_pesos[j]
        #Actualizamos el peso en el disco al correcto.
  eldisco_pesos[x] = peso_de_x


      
  
# Sumamos las carpetas finales
suma_archivos_carpeta = 0
for x in eldisco_pesos:
  #X is the key
  if(eldisco_pesos[x] <= 100000):
    print(x + " " + str(eldisco_pesos[x]))
    suma_archivos_carpeta += eldisco_pesos[x]

print("Peso Final: " + str(suma_archivos_carpeta))
#print(eldisco.keys())
#print(eldisco_pesos["/"])

print("---BARRA SEPARADORA DE SEGUNDA PARTE---")
#Part 2 !! WOHOOOOOOOOOOOOOO THis took too long q/q
#print("Main Dir:", eldisco_pesos["/"])
for x in eldisco["/"]:
  #print(x, "--", eldisco[x], "PESO", eldisco_pesos[x])
  if(type(x)!= int):
    # Si tiene un dir
    eldisco_pesos["/"] += eldisco_pesos["//" + x + "/"]

print("True peso de dir base: ", eldisco_pesos["/"])
total_disk_space = 70000000
need_at_least = 30000000
free_space = total_disk_space - eldisco_pesos["/"]
print("Espacio Disponible:",free_space)
need_to_free = need_at_least - free_space
print("Espacio necesario a liberar:",need_to_free)

closest_one = 99999999999999
closest_one_key = ""
for x in eldisco_pesos:
  if (eldisco_pesos[x] < closest_one and eldisco_pesos[x] > need_to_free):
    closest_one = eldisco_pesos[x]
    closest_one_key = x

print("El directorio mas cercano es: ", x, "con un valor de: ", closest_one)
print("Done")