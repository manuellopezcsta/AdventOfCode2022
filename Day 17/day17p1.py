import time


print('Leyendo Datos')
with open('Day 17/input.txt') as f:
  lines = f.readlines()
  line = lines[0].strip()

def BuildBase():
  output = {}
  for x in range (0, 7):
    output[(x,0)] = "#"
# X menor a 0 o manyor a 7 es pared.
  return output

def SimulateBlock(type_of_block):
  global tower
  global current_maxY;
  #print("--------------------------------------")
  can_move = True
  turn = 1  # If turn % 2 == 0, cae, sino se mueve.
  n = IdentifyBlock(type_of_block)
  spawnpos = CalculteSpawnPos(current_maxY, n)
  #print("Spawn Pos:", spawnpos)
    
  while(can_move):
    #print("Current Pos:",spawnpos)
    if(turn % 2 == 0):
      #print("Cayendo..")
      #FALL DOWN CASE
      new_pos = []
      for item in spawnpos:
        x = item[0]
        y = item[1]
        new_point = (x, y-1)
        new_pos.append(new_point)
      if(CheckIfMoveWasValid(new_pos)):
        # Move was valid
        spawnpos = new_pos
      else:
      # CANT MOVE DOWN ANY MORE.. FIX THE BLOCK
        for item in spawnpos:
          tower[item] = "#"
        new_pos = []
        can_move = False
      #Increment the turn
      turn += 1
    else:
      # Move case
      new_pos = []
      modifier = DetectNextMove()
      #print("Moviendo>", modifier)
      for item in spawnpos:
        x = item[0]
        y = item[1]
        new_point = (x + modifier, y)
        new_pos.append(new_point)
      # WE check the validity of the move to see if we should move it
      if(CheckIfMoveWasValid(new_pos)):
        # Move was valid
        spawnpos = new_pos
      #  We increment the turn
      turn +=1
      # We update the max Y
  current_maxY = sorted(tower.keys(), key=lambda x: x[1], reverse=True)[0][1]
  #print("Done.")
  return # Finished

def CheckIfMoveWasValid(pos_array):
  for item in pos_array:
    if(TryGetValue(item) == "#"):
      return False
  return True
  

def IdentifyBlock(num):
  result = num % 5
  #print("Rock type is N", result)
  return result

def DetectNextMove():
  global line
  # If we run out of line add more
  if(len(line) == 0):
    #print("Reseteando Linea")
    line += lines[0].strip()
  # We get the first element and pop it out
  result = line[0]
  holder = line[1:len(line)]
  line = holder
  #print(" new line", line, len(line))
  modifier = (0,0)
  if(result == ">"):
    modifier = 1
  else:
    modifier = -1
  return modifier

def CalculteSpawnPos(y, block_type):
  pos = []
  if(block_type == 1):
    punta = (2, y + 4) # Signo menos
    p2 = (3, y+4)
    p3 = (4, y+4)
    p4 = (5, y+4)
    pos = [punta, p2, p3, p4]
  elif(block_type == 2):
    punta = (3, y + 4) # Signo mas
    p2 = (3, y + 5)
    p3 = (3, y + 6)
    p4 = (2, y + 5)
    p5 = (4, y + 5)
    pos = [punta, p2, p3, p4, p5]
  elif(block_type == 3):
    punta = (2, y + 4) # La l al reves.
    p2 = (3, y + 4)
    p3 = (4, y + 4)
    p4 = (4, y + 5)
    p5 = (4, y + 6)
    pos = [punta, p2, p3, p4, p5]
  elif(block_type == 4):
    punta = (2, y + 4) # Signo Palo
    p2 = (2, y + 5)
    p3 = (2, y + 6)
    p4 = (2, y + 7)
    pos = [punta, p2, p3, p4]
  elif(block_type == 0):
    punta = (2, y + 4) # Signo Roca
    p2 = (3, y + 4)
    p3 = (2, y + 5)
    p4 = (3, y + 5)
    pos = [punta, p2, p3, p4]
  return pos


# Main Code

def TryGetValue(point):
  global tower
  x = point[0]
  y = point[1]
  if(x < 0 or x > 6):
    value = "#" # Pared
  else:
    value = tower.get((x,y),".")
  return value

def PrintTower():
  global tower
  max_y = sorted(tower.keys(), key=lambda x: x[1], reverse=True)[0][1]
  print("Max Y:" , max_y)
  for y in range(max_y + 2, -1, -1):
    line = ""
    for x in range(0, 7):
      line += TryGetValue((x,y))
    print(line)

def TrimDictionary(current_maxY):
  global tower
  min_y = sorted(tower.keys(), key=lambda x: x[1], reverse=False)[0][1]
  # We find a y where there is a full line and trim it
  for y in range(current_maxY, current_maxY -200 , -1):
    limpiar = True
    for x in range(0,7): # Son 7 espacios, (0,6 max)
      if(TryGetValue((x,y)) == "."):
        limpiar = False
        break
    if(limpiar):
      print("Se encontro linea completa!, limpiando dic Y=", y)
      for x in range(0,7):
        for y in range(min_y, y):
          tower.pop((x,y), None)
      print("Done Limpiando.")
      return
  print("No se encontro linea completa :c")

def UpdateTimeEta(st, curr_rock_num, max_rocks):
  et = time.time()
  secs = et - st
  mins = secs/60
  final = round(mins, 2)
  print("Tiempo Elapsado", final, "minutos")
  a = round((max_rocks/curr_rock_num) * final, 2)
  print("Tiempo Estimado Restante:", a, "minutos")
  
      
start = time.time()
tower = BuildBase()
howManyRocks = 2022
current_maxY = 0

for x in range(1, howManyRocks +1):
  if(x % 1000 == 0):
    TrimDictionary(current_maxY)
    print("Simulating Rock N", x)
    UpdateTimeEta(start, x, howManyRocks)
  SimulateBlock(x)
print("The tower is", current_maxY, "units tall")
# We draw the tower
#PrintTower()