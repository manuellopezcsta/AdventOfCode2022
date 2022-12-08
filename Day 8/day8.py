print('Leyendo Datos')
with open('Day 8/input.txt') as f:
  lines = f.readlines()

# Poblamos la matriz de arboles.
matriz = []
for x in range(len(lines)):
  matriz.append([])
  for c in lines[x].strip():
    matriz[x].append(int(c))


contador_arboles_visibles = 0
contador_arboles_invisibles = 0

def  isThisTreeVisible(index1,index2):
  global contador_arboles_invisibles
  valor_arbol = matriz[index1][index2]
  escondido_derecha = False
  escondido_izquierda = False
  escondido_arriba = False
  escondido_abajo = False
    
  #Revisamos si es visible por derecha
  for x in range(index2+1,len(matriz[index1])):
    if(valor_arbol > matriz[index1][x]):
      continue 
    else:
      escondido_derecha = True
      break
  #Revisamos si es visible x izq
  for x in range(0, index2):
    if(valor_arbol > matriz[index1][x]):
      continue 
    else:
      escondido_izquierda = True
      break
  #Revisamos si es visible x abajo
  for x in range(index1 + 1, len(matriz)):
    if(valor_arbol > matriz[x][index2]):
      continue 
    else:
      escondido_abajo = True
      break
  #Revisamos si es visible x arriba
  for x in range(0, index1):
    #print(matriz[x][index2])
    if(valor_arbol > matriz[x][index2]):
      continue 
    else:
      escondido_arriba = True
      break

  if(escondido_abajo and escondido_arriba and escondido_derecha and escondido_izquierda):
    #print("Arbol escondido:", index1, index2)
    contador_arboles_invisibles += 1
    
# Revisamos los arboles
contador_arboles_visibles = len(matriz) * len(matriz[0])

print("Len:",len(matriz[0]) , "Len2: ",len(matriz))
for x in range(len(matriz)):
  for y in range(len(matriz[0])):
    isThisTreeVisible(x, y)

contador_arboles_visibles -= contador_arboles_invisibles

print("---Barra separadora----")
print("Arboles Visibles:",contador_arboles_visibles)
print("---Start Parte 2----")

#Parte 2
current_best_scene_score = 0

def ValueTreeScore(index1, index2):
  global current_best_scene_score
  valor_arbol = matriz[index1][index2]
  score_der = 0
  score_iz = 0
  score_arr = 0
  score_abj = 0

  #Revisamos el score hacia la derecha
  for x in range(index2+1,len(matriz[index1])):
    #print(matriz[index1][x])
    if(valor_arbol > matriz[index1][x]):
      score_der += 1
      continue 
    else:
      #Si tiene el mismo valor o mayor, paro pero lo sumo.
      score_der += 1
      break
  #Revisamos el score hacia la izq
  for x in range(index2 -1, -1,-1):
    if(valor_arbol > matriz[index1][x]):
      score_iz += 1
      continue 
    else:
      #Si tiene el mismo valor o mayor, paro pero lo sumo.
      score_iz += 1
      break
    #Revisamos el score hacia arriba.
  for x in range(index1 - 1, -1, -1):
    if(valor_arbol > matriz[x][index2]):
      score_arr += 1
      continue 
    else:
      #Si tiene el mismo valor o mayor, paro pero lo sumo.
      score_arr += 1        
      break
    #Revisamos el score hacia abajo.
  for x in range(index1 + 1, len(matriz)):
    if(valor_arbol > matriz[x][index2]):
      score_abj += 1
      continue 
    else:
      #Si tiene el mismo valor o mayor, paro pero lo sumo.
      score_abj += 1
      break

  tree_score = score_abj * score_arr * score_der * score_iz

  if(tree_score > current_best_scene_score):
    current_best_scene_score = tree_score
  


for x in range(len(matriz)):
  for y in range(len(matriz[0])):
    ValueTreeScore(x, y)

print("Best Tree Score: ", current_best_scene_score)
  
print("Done")