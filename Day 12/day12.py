from queue import PriorityQueue


print('Leyendo Datos')
with open('Day 12/input.txt') as f:
  lines = f.readlines()

def ClearInput(input_array):
  output = []
  for x in lines:
    clean = x.strip()
    output.append(clean)
  return output
  

def getValueMap(input_array):
  j = "abcdefghijklmnopqrstuvwxyz"
  output = []
  for x in input_array:
    result = []
    x_index = input_array.index(x)
    for element in x:
      y = x.index(element)
      letter = input_array[x_index][y]
      #print("Letra:", letter)
      if(letter == "S"):
        cp_value = 0
      elif(letter == "E"):
        #The ending has the highest value
        cp_value = j.index("z") + 2
      else:
        cp_value = j.index(letter) + 1
      result.append(cp_value)
    output.append(result)
  #Devolvemos el array final
  return output

def FindStartingPoint(map):
  print("Buscando Origen...")
  #print("LEN: ", len(map),len(map[0]))
  for y in range(0, len(map)):
    for x in range(0, len(map[y])):
      if(map[y][x] == 0):
        print("Origen encontrado X:", x, "Y:", y)
        return x, y
        
def FindEndPoint(map):
  print("Buscando Origen...")
  #print("LEN: ", len(map),len(map[0]))
  for y in range(0, len(map)):
    for x in range(0, len(map[y])):
      if(map[y][x] == 27):
        print("Final encontrado X:", x, "Y:", y)
        return (x, y)

def CreateDictionaryGraph(map):
  print("Generando Diccionario de conecciones..")
  #Encontramos vecinos inmediatos
  vecinos = [(0,1), (0,-1), (1,0), (-1,0)]
  new_vecinos = {}
  for y in range(0,len(map)):
    for x in range(0, len(map[y])):
      current_x_index = x
      current_y_index = y
      punto = (current_x_index, current_y_index)
      current_point_value = map[punto[1]][punto[0]]
      # Usando el punto actual
      holder = []
      for j in range(0, len(vecinos)):
        #We check if that index exist
        #print("DEBUG", punto[0])
        new_x_index = punto[0] + vecinos[j][0]
        new_y_index = punto[1] + vecinos[j][1]
        if(new_x_index < len(map[y]) and new_x_index >= 0):
          #Existe x
          if(new_y_index < len(map) and new_y_index >= 0):
            #Existe y // WE CHECK FOR THE VALUE.
            new_cell_value = map[new_y_index][new_x_index]
            if(new_cell_value <= current_point_value or
              new_cell_value == (current_point_value + 1)):
              # Add to posibles vecinos
              holder.append((new_x_index, new_y_index))
      # Agregamos todos los compatibles al diccionario
      new_vecinos[punto] = holder

    #We give back the dictionary with the finished graph connections
  print("Done..")
  return new_vecinos


class Graph:
  def __init__(self, num_of_vertices):
    self.v = num_of_vertices
    self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
    self.visited = []

  def add_edge(self, u, v, weight):
        #print("U:", u, "V", v);
        self.edges[u][v] = weight

########### FIN DE GRAPH ###################

def dijkstra(graph, start_vertex):
  print("Buscando Caminos..")
  D = {v:float('inf') for v in range(graph.v)}
  D[start_vertex] = 0

  pq = PriorityQueue()
  pq.put((0, start_vertex))

  while not pq.empty():
    (dist, current_vertex) = pq.get()
    graph.visited.append(current_vertex)

    for neighbor in range(graph.v):
      if graph.edges[current_vertex][neighbor] != -1:
        distance = graph.edges[current_vertex][neighbor]
        if neighbor not in graph.visited:
          old_cost = D[neighbor]
          new_cost = D[current_vertex] + distance
          if new_cost < old_cost:
            pq.put((new_cost, neighbor))
            D[neighbor] = new_cost
  print("Hecho...")
  return D

########### FIN DEL ALGORITMO DE DIJKSTRA ##############

def FromTupleToNodeNumber(tuple):
  global map
  contador = 0
  for x in range(0, len(map[0])):
    for y in range(0, len(map)):
      if(tuple == (x, y)):
        number = contador 
      else:
        contador += 1
  return number


def PoblarGrafo(grafo, c_map):
  print("Conectando grafo...")
  for key in c_map.keys():
    key_node_n = FromTupleToNodeNumber(key)
    for nodo in c_map[key]:
      nodo_n = FromTupleToNodeNumber(nodo)
      grafo.add_edge(key_node_n, nodo_n, 1)
  grafo_tuneado = grafo
  print("Done...")
  return grafo_tuneado

#Limpiamos el input
input = ClearInput(lines)
#Generamos el Mapa de alturas
map = getValueMap(input)
#Buscamos el origen
starting_x, starting_y = FindStartingPoint(map)
#Generamos el diccionario de conecciones Key tuples.
c_map = CreateDictionaryGraph(map)
#Creamos el grafo
###print("LEN DE C_MAP KEYS:", len(c_map.keys()))
g = Graph(len(c_map.keys())) # Cantidad de nodos.
#Poblamos las conecciones
final_graph = PoblarGrafo(g, c_map)
#Buscamos el punto final
final_point_tuple = FindEndPoint(map)

resultado = dijkstra(final_graph, FromTupleToNodeNumber((starting_x, starting_y)))
#Imprimimos el camino mas corto, que esta guardado en la key del nodo final
print("Los pasos requeridos para llegar al final son:", resultado[FromTupleToNodeNumber(final_point_tuple)])

####### PARTE 2 #######

# WE ADD A FAKE NODE 40, with connections to all the points with an a(value 1 in the map)
print("########### PARTE 2 ###########")
def FindAllPosibleStartingNodes(map):
  print("Buscando Starting points posibles")
  possible_points = []
  for y in range(0,len(map)):
    for x in range(0, len(map[y])):
      if(map[y][x] == 1):
        possible_points.append((x, y))
  #print(possible_points)

  possible_points_nodes_n = []
  for spot in possible_points:
    node_n = FromTupleToNodeNumber(spot)
    possible_points_nodes_n.append(node_n);

  return possible_points_nodes_n

def AddFakePaths(graph, points, map):
  for x in points:
    graph.add_edge(len(map) * len(map[0]) , x, 0)


# Crear nuevo grafo o no va a andar... xq el edge 40 no existe para v..
starting_points = FindAllPosibleStartingNodes(map)
g = Graph(len(c_map.keys()) + 1) # Cantidad de nodos.
#Poblamos las conecciones
final_graph = PoblarGrafo(g, c_map)
#Agregamos los puntos falsos
AddFakePaths(final_graph, starting_points, map)
           

resultado = dijkstra(final_graph, (len(map) * len(map[0])))
##como le paso el nuevo starting point , len x len..
print("Los pasos requeridos para el minimo camino NUEVO son:", resultado[FromTupleToNodeNumber(final_point_tuple)])
         
## For Debugging
#for x in map:
  #print(x)

#for x in v_map:
  #print(x)

#for x in c_map.keys():
  #print("KEY:",x, "VALUES:", c_map[x])