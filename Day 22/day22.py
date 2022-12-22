import re


print('Leyendo Datos')
with open('./input.txt') as f:
  lines = f.readlines()

def ParseInput(lines):
  output = []

  for j in lines:
    if(j[0].isdigit()): # Ultima linea con instrucciones.
      output.append(j)
      continue

    x = j[0: len(j) - 1]
    output.append(x)
  
  return output

def BuildInstructions(instr_line):
  output = re.split('(\d+)', instr_line)
  for count, x in enumerate(output):
    if x == "":
      output.pop(count)
      continue

  for count, x in enumerate(output):
    if x[0].isdigit(): # If its a number we make it a number
      output[count] = int(x)

  return output

def BuildMap(input):
  print("Building Map...")
  input.pop(len(input) -1) # We remoe the instructions
  output = {}

  for y in range(1, len(input) +1):
    for x in range(1, len(input[y - 1]) + 1):
      if(input[y-1][x-1] == " "):
        output[(x,y)] = "T"
      else:
        output[(x,y)] = input[y-1][x-1]
  
  return output

def GetValue(coord):
  global map
  value = map.get(coord, "T") # We will give back a T as in Teleport if it doesnt exist.
  return value

def PrintMap(map):
  max_x = max(list(map))[0]
  max_y = max(list(map))[1]
  for y in range(0, max_y + 2):
    line = ""
    for x in range(0,max_x + 3):
      value = GetValue((x, y))
      line += value
    line+= "\r"
    print(line)

def GetStartingPoint(first_line):
  point = (0, 0)
  for x in range(0, len(first_line)):
    if(first_line[x] == "."):
      point = (x+1, 1)
      break
  print("Starting Point found at:", point)
  
  return point

def FindMinMaxForPoint(point):
  global clean_lines

  cx = point[0]
  cy = point[1]

  min_x = -10
  max_x = -10
  min_y = -10
  max_y = -10
  #Izq Min X
  for x in range(cx, -2, -1):
    point = (x,cy)
    v = GetValue(point)
    if(v == "T"):
      min_x = point[0] +1
      break
  #Der Max X
  for x in range(cx, 1000): # I just eye balled the value and added like 30 to it.., 
                              #you could just get the max len of clean lines and use that
    point = (x,cy)
    v = GetValue(point)
    if(v == "T"):
      max_x = point[0] -1
      break
  
  #Arriba Min Y
  for y in range(cy, -2, -1):
    point = (cx,y)
    v = GetValue(point)
    if(v == "T"):
      min_y = point[1] + 1
      break

  #Abajo Max Y
  for y in range(cy, len(clean_lines) + 100):
    point = (cx,y)
    v = GetValue(point)
    if(v == "T"):
      max_y = point[1] - 1
      break

  if(min_x == -10 or max_x == -10 or min_y == -10 or max_y == -10):
    print("ERROR MISCALCULATION! in minMax func")
    print("mX:", min_x, "MX:", max_x, "mY:", min_y, "MY:", max_y)
    return

  return min_x, max_x, min_y, max_y

def MakeMove(curr_pos, steps):
  global curr_dir

  cx = curr_pos[0]
  cy = curr_pos[1]

  min_x, max_x, min_y, max_y = FindMinMaxForPoint(curr_pos)

  # Scan the direction for a # or a T..
  if(curr_dir == 0):
    start = cx+1
    # Scan right
    for x in range(start, start + steps):
      point = (x, cy)
      if(GetValue(point) == "#"):
        # Caso toca pared
        curr_pos = (x-1, cy)
        return curr_pos

      if(GetValue(point) == "T"):
        #Caso teleport
        new_steps = steps - (point[0] - cx)
        curr_pos = (min_x, cy)
        # Before we teleport we check the new location for a rock, it it has we cancel the tp and return with the current pos.
        if(GetValue(curr_pos) == "#"):
          print("CANNOT TP TO ROCK")
          curr_pos = (x -1, cy)
          return curr_pos
        return MakeMove(curr_pos, new_steps)
    # Si salimos del for nos movemos normal
    curr_pos = (cx + steps, cy)
    return curr_pos
        
  elif(curr_dir == 1):
    # Scan down
    start = cy+1  # y sube hacia abajo.
    for y in range(start, start + (steps)):
      point = (cx, y)
      if(GetValue(point) == "#"):
        # Caso toca pared
        curr_pos = (cx, y-1)
        return curr_pos

      if(GetValue(point) == "T"):
        #Caso teleport
        new_steps = steps - (y - cy)
        curr_pos = (cx, min_y)
        # Before we teleport we check the new location for a rock, it it has we cancel the tp and return with the current pos.
        if(GetValue(curr_pos) == "#"):
          print("CANNOT TP TO ROCK")
          curr_pos = (cx, y -1)
          return curr_pos
        return MakeMove(curr_pos, new_steps)
    # Si salimos del for nos movemos normal
    curr_pos = (cx, cy + steps)
    return curr_pos
  
  elif(curr_dir == 2):
    start = cx-1
    # Scan left
    for x in range(start, start - (steps), -1):
      point = (x, cy)
      if(GetValue(point) == "#"):
        # Caso toca pared
        curr_pos = (x+1, cy)
        return curr_pos

      if(GetValue(point) == "T"):
        #Caso teleport
        new_steps = steps - (cx - x)
        curr_pos = (max_x, cy)
        # Before we teleport we check the new location for a rock, it it has we cancel the tp and return with the current pos.
        if(GetValue(curr_pos) == "#"):
          print("CANNOT TP TO ROCK")
          curr_pos = (x +1, cy)
          return curr_pos
        return MakeMove(curr_pos, new_steps)
    # Si salimos del for nos movemos normal
    curr_pos = (cx - steps, cy)
    return curr_pos

  elif(curr_dir == 3):
    # Scan up
    start = cy-1  # y sube hacia abajo.
    for y in range(start, start - (steps),-1):
      point = (cx, y)
      if(GetValue(point) == "#"):
        # Caso toca pared
        curr_pos = (cx, y+1)
        return curr_pos

      if(GetValue(point) == "T"):
        #Caso teleport
        new_steps = steps - (cy - y)
        curr_pos = (cx, max_y)
        # Before we teleport we check the new location for a rock, it it has we cancel the tp and return with the current pos.
        if(GetValue(curr_pos) == "#"):
          print("CANNOT TP TO ROCK")
          curr_pos = (cx, y + 1)
          return curr_pos
        return MakeMove(curr_pos, new_steps)
    # Si salimos del for nos movemos normal
    curr_pos = (cx, cy - steps)
    return curr_pos
  else:
    print("ERROR IN MAKE MOVE, DIR DOESNT EXIST")
    return

def Turn(instruction):
  global curr_dir
  # Dir... 0 right, 1 down, 2 left, 3 up
  if(instruction == "R"):
    print("Se giro derecha.")
    curr_dir += 1
    # Handle edge cases
    if(curr_dir == 4):
      curr_dir = 0
  elif(instruction == "L"):
    print("Se giro izq.")
    curr_dir -= 1
    # Handle edge cases
    if(curr_dir == -1):
      curr_dir = 3
  else:
    print("ERROR turn unclear!.")

def GetPassword(current_position, current_dir):
  row = current_pos[1]
  column = current_pos[0]
  output = (row * 1000) + (column * 4) + curr_dir
  return output

# Main code...
clean_lines = ParseInput(lines)
instructions = BuildInstructions(clean_lines[-1])
map = BuildMap(clean_lines)
starting_pos = GetStartingPoint(clean_lines[0])  # For test is (9,1) // Real input is.

# We set the starting values
curr_dir = 0
current_pos = starting_pos

# We make the moves
for move in instructions:
  if type(move) == int:
    current_pos = MakeMove(current_pos, move)
    print("Se movio, nueva pos:", current_pos)
    if(GetValue(current_pos) == "#" or GetValue(current_pos) == "T"):
      print("ERROR EN NUEVA POS !, se movio a un", GetValue(current_pos))
      break
  else:
    Turn(move)

map[current_pos] = "o"
print("Finished Moving..")
# We get the password
pswd = GetPassword(current_pos, curr_dir)
print("The password is:", pswd)

# We show the end position
#PrintMap(map)