print('Leyendo Datos')
with open('Day 14/input.txt') as f:
  lines = f.readlines()

def BuildCaveWalls(raw_input):
  print("Building Walls...")
  output = {}
  max_x = 0
  max_y = 0
  for line in raw_input:
    holder = []
    data = line.strip()
    points = data.split(" -> ")
    for p in points:
      x = int(p.split(",")[0])
      y = int(p.split(",")[1])
      # We check for a new max x and y, and save them if they exist
      if(x > max_x):
        max_x = x
      if(y > max_y):
        max_y = y
      # We store the border points in a holder array, to build the walls later
      holder.append((x,y))
    
    index_limit = len(holder) - 1
    for j in range(0, len(holder)):
      if (j != index_limit):
        #Nos fijamos que punto cambia.. y agregamos
        origin_point = holder[j]
        new_point = holder[j+1]
        result = (origin_point[0] - new_point[0], origin_point[1] - new_point[1])
        # Casos...
        #print("RESULT:", result, "P1:", origin_point, "P2:", new_point)
        if(result[0] != 0):
          # CASO X...
          start_x = (min(origin_point[0], new_point[0]))
          end_x = (max(origin_point[0], new_point[0]))
          for x in range(start_x, end_x + 1):
            output[(x,origin_point[1])] = "#"
        elif(result[1] != 0):   
          #CASO Y
          start_y = (min(origin_point[1], new_point[1]))
          end_y = (max(origin_point[1], new_point[1]))
          for y in range(start_y, end_y +1):
            output[origin_point[0], y] = "#"
        else:
          print("ERROR DIF ENTRE PAREDES! RESULT:", result)
      else:
        # Es el ultimo punto
        point = holder[j]
        output[point] = "#"

  print("Max X:", max_x, "Max Y:", max_y)
  return output, max_x, max_y

def BuildCaveAir(walls_dic, max_x, max_y):
  print("Building Air..")
  output = {}
  for x in range(0, max_x +1):
    for y in range(0, max_y +1):
      if((x,y) not in walls_dic.keys()):
        output[(x,y)] = "."

  return output

def BuildCaveFinal(walls_dic, air_dic, max_x, max_y):
  output = {}
  for item in walls_dic.keys():
    output[item] = walls_dic[item]
  for item in air_dic.keys():
    output[item] = air_dic[item]
  # We add the VOOOOID :o
  for x in range(-1, max_x + 2):
    point = (x, max_y + 1)
    output[point] = "V"
  return output

def BuildCaveFinalP2(walls_dic, air_dic, max_x, max_y):
  output = {}
  for item in walls_dic.keys():
    output[item] = walls_dic[item]
  for item in air_dic.keys():
    output[item] = air_dic[item]
  # We add more air to the right of the graph too
  for x in range(max_x + 1, max_x * 2):
    for y in range(0, max_y * 2):
      point = (x, y)
      output[point] = "."
  # We add the extra air layer and the floor
  for x in range(0, max_x *2+ 1):
    point = (x, max_y + 1)
    output[point] = "."
  # We add the floor layer. should be inf.. but im winging it.
  for x in range(-max_x*2, max_x + max_x*2):
    point = (x, max_y + 2)
    output[point] = "#"
  
  return output
      

def SimulateSandGrain(point):
  current_pos = (point[0], point[1]) # Starting pos
  global contador
  global complete_cave_dic
  # Array with the 3 pos cases in order, Abajo, Abajo Izq, Abajo Der
  new_p = [(current_pos[0], current_pos[1] + 1),
           (current_pos[0] - 1,current_pos[1] + 1),
           (current_pos[0] + 1, current_pos[1] + 1)]
  new_p_value = []
  for x in range(0, 3):
    if(new_p[x] in complete_cave_dic.keys()):
      new_p_value.append(complete_cave_dic[new_p[x]])
    else:
      # Si no existe el indice le agrego una pared para simplificar luego.
      new_p_value.append("#")

  # Now we only need to check the values...
  #Caso 0
  if(new_p_value[0] == "."):
    return SimulateSandGrain(new_p[0])
  elif(new_p_value[0] == "o" or new_p_value[0] == "#"):
    #Pasamos a caso 2..
    if(new_p_value[1] == "."):
      return SimulateSandGrain(new_p[1])
    elif(new_p_value[1] == "o" or new_p_value[1] == "#"):
      #Pasamos a caso 3..
      if(new_p_value[2] == "."):
        return SimulateSandGrain(new_p[2])
      elif(new_p_value[2] == "o" or new_p_value[2] == "#"):
        complete_cave_dic[current_pos] = "o"
        #For part 2...
        if(current_pos == (500,0)):
          contador += 1
          return False
        else:
          contador += 1
          return True
      #Si abajo tiene vacio caso 3
      elif(new_p_value[0] == "v"):
        return False
    #Si abajo tiene vacio caso 1
    elif(new_p_value[0] == "v"):
      return False
  #Si abajo tiene vacio caso 0
  elif(new_p_value[0] == "v"):
    return False

####################################################
# Main code
walls_dic, max_x, max_y = BuildCaveWalls(lines)
air_dic = BuildCaveAir(walls_dic, max_x, max_y)
complete_cave_dic = BuildCaveFinal(walls_dic, air_dic, max_x, max_y)
print("LEN WALLS:", len(walls_dic.keys()), "Correct one for example: 20")
#################### DEBUGGING ####################
print("---------------- DATA ABOUT THE CAVE ----------------")
print("There is", len(air_dic.keys()) ,"air blocks in the cave")
print("Max Cave Space =", (max_x +1) * (max_y + 1))
print("Cave Space - Air = Walls -->", (max_x +1) * (max_y + 1), "-", len(air_dic.keys()), "=", (max_x +1) * (max_y + 1) - len(air_dic.keys()))
print("Cave Space + void =", (max_x +1) * (max_y + 1), "+", (max_x +3), "=", ((max_x +1) * (max_y + 1)) + (max_x +3))
print("Final Cave Dic Size:", len(complete_cave_dic))
print("---------------- END OF CAVE DATA ----------------")
#################### END OF DEBUGGING ####################
print("Simulating grains")
contador = 0
canSimulate = True
while(canSimulate):
  canSimulate = SimulateSandGrain((500,0))

print("Termino simulacion se conto", contador, "granos de arena.")


############ PARTE 2 ############
print("---------------- PARTE 2 ----------------")
# Reseteamos todos
walls_dic, max_x, max_y = BuildCaveWalls(lines)
air_dic = BuildCaveAir(walls_dic, max_x, max_y)
complete_cave_dic = BuildCaveFinalP2(walls_dic, air_dic, max_x, max_y)

print("Simulating grains")
contador = 0
canSimulate = True
while(canSimulate):
  canSimulate = SimulateSandGrain((500,0))

print("Termino simulacion se conto", contador, "granos de arena antes de que se tapara (500,0) .")

# Para ver como queda la sim de arena
dibujo =  open("test.txt", "w")
for y in range(0, max_y * 2):
  linea = ""
  for x in range(0, max_x  * 2):
    linea += complete_cave_dic.get((x,y),".")
  linea+="\n"
  dibujo.write(linea)
dibujo.close()