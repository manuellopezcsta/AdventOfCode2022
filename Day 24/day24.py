from queue import PriorityQueue
from math import gcd


print('Leyendo Datos')
with open('./input.txt') as f:
  lines = f.readlines()

def CleanInput(input):
  output = []
  for l in input:
    clean = l.strip()
    output.append(clean)
  return output

def BuildOriginalMap(input):
  # We make a dic and add stuff to it.
  output = {}
  for y in range(0,len(input)):
    for x in range(0, len(input[0])):
      output[(x,y,0)] = input[y][x]
  return output

def PrintMapSlice(map, z):
  print("===== MAP AT Z" + str(z) + " =====")
  max_x = max(list(map))[0]
  max_y = max(list(map))[1]
  min_x = min(list(map))[0]
  min_y = min(list(map))[1]
  for y in range(min_y, max_y + 1):
    line = ""
    for x in range(min_x, max_x + 1):
      value = GetValue((x, y, z), map)
      if(len(value) > 1):
        value = str(len(value))
      else:
        value = value[0]
      line += value
    line+= str(y) + "\r"
    print(line)
  print(min_x, "------------", max_x)

def GetValue(coord, map):
  value = map.get(coord, "#") # We will give back a wall if it doesnt exist
  return value

def CalculateMCM(lines):
  v1 = len(lines) - 2
  v2 = len(lines[0]) - 2

  mcm=int(v1*v2/gcd(v1,v2)) 
  print("MCM de", v1, "y", v2, "=", mcm)
  return mcm

def MakeMap3D(map, input):
  print("Making the supermap.")
  supermap = {}
  mcm = CalculateMCM(input)

  for y in range(0,len(input)):
    for x in range(0,len(input[0])):
      for z in range(0, mcm):
        if(z == 0): # If it the first one we just copy it.
          supermap[(x,y,z)] = map[(x,y,z)]
        else:   # We simulate the rest
          point = (x,y,z)
          point_on_zero = (x,y,0)
          if(GetValue(point_on_zero, map) == "#"): # if its a wall
            supermap[point] = "#"
          elif(GetValue(point_on_zero, map) == "."): # if its air)
            continue
          else: # Its a wind
            puntofuturo, forma = SimulateWind(point) # Vientito es la forma.
            if(forma != None):
              #print("PUNTO FUTURO:", puntofuturo, "FORMA:", forma)
              arr_valores_punto_futuro = supermap.get(puntofuturo, [])
              arr_valores_punto_futuro.append(forma)
              supermap[puntofuturo] = arr_valores_punto_futuro

  # After this add the unsimulated spaces for the map as air.
  for y in range(0,len(input)):
    for x in range(0,len(input[0])):
      for z in range(0, mcm):
        if((x,y,z) in supermap.keys()):
          continue
        else:
          supermap[(x,y,z)] = "."
  print("Super Map is Done. IT HAS", len(supermap.keys()), "points.")
  # Return the final supermap
  return supermap

def TrimConnections(conn):
  global final_map
  print("Trimeando Connections..")
  output = {}

  for key in conn.keys():
    #Revisamos si para cada key, hay alguno q la tenga de hijo en el piso anterior., si es asi la agregamos a output.
    x = key[0]
    y = key[1]
    z = key[2]
    if(z == 0): # We do not trim z0 cause we could delete important start points.
      output[key] = conn[key]
      #print("Se agrego z0")
      continue

    v_mod = [(0,1,-1), (0,-1,-1), (1,0,-1), (-1,0,-1), (0,0,-1)]
    for p in v_mod:
      vecino = (p[0]+x,p[1]+y,p[2]+z)
      se_encontro = False # Flag to exit the loop
      if(vecino not in final_map.keys() or vecino not in conn.keys()): # If it doesnt exist, continue to the next one.
        continue
      #Check the neighboars for the key.
      #print("vecino", vecino)
      for item in conn[vecino]:
        #print("ITEM", item, "KEY", key)
        if(item == key):
          output[key] = conn[key]
          #print("Se agrego x vecino")
          se_encontro = True
          break
      if(se_encontro):
        break

  print("Done... New size:", len(output.keys()))
  return output

def SimulateWind(point):
  # We simulate the state based out of the original map and return the point where it lands, and its shape
  global map
  global lines

  x = point[0]
  y = point[1]
  z = point[2]
  point_on_zero = (x, y, 0)
  vientito = GetValue(point_on_zero, map)
  steps = z # Siempre positivo
  l_v_x = len(lines[0]) -2
  l_v_y = len(lines) -2
  #print(vientito, "VIENTITO")

  if(vientito == "#"):
    print("ERROR VIENTITO ES UNA PARED. 103")
    return None,None
  elif(vientito == "."):
    print("ERROR VIENTITO ES AIRE. 106")
    return None,None
  else:
    # CASOS DE LOS VIENTOS !
    forma = GetValue(point_on_zero, map)
    if(forma == "^"):
      if(y - steps >= 1): # It doesnt loop
        new_y = y - steps
      else: # it loops
        new_y = ((y-1 - steps) % l_v_y + l_v_y ) % l_v_y + 1
      # We return the new point
      new_point = (x,new_y, z)
      return new_point, "^"

    elif(forma == "v"):
      if(y + steps <= l_v_y): # It doesnt loop
        new_y = y + steps
      else: # it loops
        new_y = ((y-1 + steps) % l_v_y + l_v_y ) % l_v_y + 1
      # We return the new point
      new_point = (x,new_y, z) 
      return new_point, "v"

    elif(forma == "<"):
      if(x - steps >= l_v_x): # It doesnt loop
        new_x = x - steps
      else: # it loops
        new_x = ((x-1 - steps) % l_v_x + l_v_x ) % l_v_x + 1
      # We return the new point
      new_point = (new_x,y, z)  
      return new_point, "<"

    elif(forma == ">"):
      if(x + steps <= l_v_x): # It doesnt loop
        new_x = x + steps
      else: # it loops
        new_x = ((x-1 + steps) % l_v_x + l_v_x ) % l_v_x + 1
      # We return the new point
      new_point = (new_x,y, z) 
      return new_point, ">"

    else:
      print("ERROR DE FORMA 102")
      return None, None
  print("GT")
###################### PATHFINDING STUFF ######################

def CreateDictionaryGraph(map):
  print("Generando Diccionario de conecciones..")
  output = {}
  #Encontramos vecinos inmediatos
  v_mod = [(0,1,1), (0,-1,1), (1,0,1), (-1,0,1), (0,0,1)]
  max_z = sorted(map, key=lambda a: a[2], reverse=True)[0][2]
  for k in map.keys():
    point = k
    # If its not air we dont care to connect it.
    if(GetValue(point, map) != "."):
      continue
    # If its not air we continnue.
    x = point[0]
    y = point[1]
    z = point[2]
    holder = []
    for p in v_mod:
      vecino = (p[0]+x,p[1]+y,p[2]+z)
      if(vecino[2] == max_z+1):
        vecino = (vecino[0], vecino[1], 0) # We connect the max z to 0.. so it can loop.
      if(GetValue(vecino, map) == "."):
        holder.append(vecino)
    output[point] = holder
  #We give back the dictionary with the finished graph connections
  print("Done.. Size of dic", len(output.keys()))
  return output

class Graph:

  def __init__(self, num_of_vertices):
    print("Initializing Graph.")
    self.v = num_of_vertices
    self.edges = dict(
    )  # [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
    self.visited = set()

  def add_edge(self, u, v, weight):
    #print("U:", u, "V", v);
    s = self.edges.get(u, set())
    s.add(v)
    self.edges[u] = s  #[u][v] = weight

  def reset(self):
    self.visited = set()

def FastTupleToNodeNumber():
  global connections
  return dict([(k,count) for (count,k) in enumerate(connections.keys())])

def FromTupleToNodeNumber(tuple):
  global fast
  return fast.get(tuple, None)

def FindEndPoints(connection_map, lines, result, returning=False):
  index_x = lines[len(lines) - 1].index(".")
  index_y = len(lines) - 1
  # if returning we give it the other point.
  if(returning):
    index_x = lines[0].index(".")
    index_y = 0

  node_numbers = []
  for k in connections.keys():
    if(k[0] == index_x and k[1] == index_y):
      number = FromTupleToNodeNumber(k)
      node_numbers.append(number)

  # We scan the results on the end points and save the min distance.
  min = 99999999999
  correct_node = 5959595959
  
  for n in node_numbers:
    if(result[n] < min):
      min = result[n]
      correct_node = n

  return min, correct_node

def PoblarGrafo(grafo, c_map):
  global fast
  fast=FastTupleToNodeNumber()
  print("Conectando grafo...")
  for key in c_map.keys():
    key_node_n = FromTupleToNodeNumber(key)
    for nodo in c_map[key]:
      nodo_n = FromTupleToNodeNumber(nodo)
      grafo.add_edge(key_node_n, nodo_n, 1)
  grafo_tuneado = grafo
  print("Done...")
  return grafo_tuneado


def dijkstra(graph, start_vertex, debug=False):
  print("Buscando Caminos..")
  D = {v:float('inf') for v in range(graph.v)}
  D[start_vertex] = 0
  graph.reset()

  count = 0

  pq = PriorityQueue()
  pq.put((0, start_vertex))

  while not pq.empty():
    count +=1
    if(debug):
      if count % 100000 ==0:
        print (f"PERF {count} {pq.qsize()} {len(graph.visited)}")
    (dist, current_vertex) = pq.get()
    graph.visited.add(current_vertex)

    for neighbor in graph.edges.get(
        current_vertex, set()):  
        distance = 1
        if neighbor not in graph.visited:
          old_cost = D[neighbor]
          new_cost = D[current_vertex] + distance
          if new_cost < old_cost:
            pq.put((new_cost, neighbor))
            D[neighbor] = new_cost
  print("Hecho...")
  return D


# Main code #
# We will build a 3d map
# Each layer will have the next wind simulation, until we have them all using mcm
# After that we will find the posible moves using the rules from 1 layer to the next, and build a node network
# Then we can run a pathfinding algorythm.
lines = CleanInput(lines)
# We build the Z0 map
map = BuildOriginalMap(lines)
PrintMapSlice(map, 0)
# Using the Z0 map we generate all the rest of scenarios
final_map = MakeMap3D(map, lines)
# We make a connection map
connections = CreateDictionaryGraph(final_map)
# We trim it even more
connections = TrimConnections(connections)
# We create the graph
g = Graph(len(connections.keys()))
#Poblamos las conecciones
final_graph = PoblarGrafo(g, connections)
# We run The pathfinding
start_point = (1,0,0)
resultado = dijkstra(final_graph, FromTupleToNodeNumber(start_point))
print("========================================================================================")
# We find the correct End point
min_distance, n = FindEndPoints(connections, lines, resultado)
print("El elfo llego al final luego de", min_distance, "turnos")
print("======= PART 2 =======")
# Guardamos el tiempo del viaje inicial
total_time = min_distance
# Cambiamos el punto de inicio y lo corremo
print("Cambiando el start point a node N:", n)
start_point = n
resultado = dijkstra(final_graph, start_point)
min_distance, n = FindEndPoints(connections, lines, resultado, returning=True)
print("Res viaje 2:", min_distance)
# Sumamos el resultado del segundo viaje.
total_time += min_distance
#Cambiamos el punto de inicio y lo volvemos a correr
print("Cambiando el start point a node N:", n)
start_point = n
resultado = dijkstra(final_graph, start_point)
min_distance, n = FindEndPoints(connections, lines, resultado, returning=False)
print("Res viaje 3:", min_distance)
total_time += min_distance
print("========================================================================================")
print("El elfo rescato las snacks luego de", total_time, "minutos")
