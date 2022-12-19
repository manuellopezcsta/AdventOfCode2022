print('Leyendo Datos')
with open('Day 18/input.txt') as f:
  lines = f.readlines()

def BuildLava():
  dropplets = []
  for l in lines:
    input = l.strip()
    final = "("
    input += ")"
    final += input
    tuple_obj = eval(final)
    dropplets.append(tuple_obj)

  return dropplets

def FindSurfaceScore(arr, l_index):
  score = 6
  value = arr[l_index]
  # We test the 6 sides and do -1, for each one that fails the test
  modifier1 = (value[0] + 1, value[1], value[2])
  modifier2 = (value[0] - 1,value[1], value[2])
  modifier3 = (value[0], value[1] + 1, value[2])
  modifier4 = (value[0], value[1] - 1, value[2])
  modifier5 = (value[0], value[1], value[2] + 1)
  modifier6 = (value[0], value[1], value[2] - 1)

  if(modifier1 in arr):
    score -= 1
  if(modifier2 in arr):
    score -= 1
  if(modifier3 in arr):
    score -= 1
  if(modifier4 in arr):
    score -= 1
  if(modifier5 in arr):
    score -= 1
  if(modifier6 in arr):
    score -= 1
    
  return score

def FindMinMax(arr):
  output = 0
  # We get the values of min x, y and z and max x, y and z
  # Then we scan it all if its not a point defined in the arr
  # to see if it has air
  minX = sorted(arr, key=lambda x: x[0], reverse=False)[0][0]
  maxX = sorted(arr, key=lambda x: x[0], reverse=True)[0][0]
  minY = sorted(arr, key=lambda x: x[1], reverse=False)[0][1]
  maxY = sorted(arr, key=lambda x: x[1], reverse=True)[0][1]
  minZ = sorted(arr, key=lambda x: x[2], reverse=False)[0][2]
  maxZ = sorted(arr, key=lambda x: x[2], reverse=True)[0][2]
  print("Min X:", minX, "Max X:", maxX, "Min Y:", minY, "Max Y:", maxY, "Min Z:", minZ, "Max Z:", maxZ)
  return minX, maxX, minY, maxY, minZ, maxZ


visitados = set()
pendientes = set()
water_array = {}

def FindBubbles():
  global lava
  global box
  global visitados # Array de vecinos.
  global pendientes

  nuevopendiente = set()
  # We create a block a little bigger than the obsidian
  # Flood it to find all the points around it.
  for e in pendientes:
    if e not in visitados: # Si no visitamos el punto
      p = e
      p1 = (p[0], p[1] +1, p[2])
      p2 = (p[0] + 1, p[1], p[2])
      p3 = (p[0], p[1] - 1, p[2])
      p4 = (p[0] - 1, p[1], p[2])
      p5 = (p[0], p[1], p[2] + 1)
      p6 = (p[0], p[1], p[2] -1)
      points = [p1,p2,p3,p4,p5,p6]
      for point in points:
        if ((point in box) and (point not in lava) and point not in visitados):
          nuevopendiente.add(point)
      visitados.add(e)

  if len(nuevopendiente) > 0:
    pendientes = nuevopendiente
    return FindBubbles()
    
  print("Caja de agua armada.") 

def BuildBox(arr):
  minX, maxX, minY, maxY, minZ, maxZ = FindMinMax(arr)
  minimo = min(minX, minY, minZ)
  maximo = max(maxX, maxY, maxZ)
  output = {}
  print("Armando caja de aire...")
  for x in range(minimo -1, maximo +2):
    for y in range(minimo -1, maximo +2):
      for z in range(minimo -1 , maximo + 2):
        output[(x,y,z)] = False
  return output

def CalculateCorrectOutsideSurface(water_arr):
  # Calculate the area of the water block
  water_score = 0
  print("Calculando Correct Surface..")
  for x in range(0, len(water_arr)):
    water_score += FindSurfaceScore(list(water_arr), x)
  # We find the score of 1 wall and x4 it..
  minX, maxX, minY, maxY, minZ, maxZ = FindMinMax(water_arr)
  alto = maxX -minX +1
  ancho = maxY - minY +1
  print(alto,ancho)
  lado = alto * ancho
  # We then just remove that from the water score
  output = water_score - (lado * 6)
  return output
  
# Main code
lava = BuildLava() # We build the lava
# We find each droplet score and add it to a total.
final_score = 0
print("Calculando Area de Lava..")
for d in range(0, len(lava)):
  final_score += FindSurfaceScore(lava, d)
print("Final surface area of the lava is:", final_score)

print("====== PART 2 ======")
print("Buscando burbujas de aire..")
pendientes.add((0,-1,-1)) # Agregamos el primer punto a visitar
box = BuildBox(lava) # Armamos caja de aire
print("Armando Caja de Agua..")
FindBubbles() # Simulamos el agua
final_score = CalculateCorrectOutsideSurface(visitados)
print("Done.. Correct Size:", final_score)