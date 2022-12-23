print('Leyendo Datos')
with open('./input.txt') as f:
  lines = f.readlines()

def BuildDic(arr):
  output = {}
  holder = []
  elf_pos = []
  for line in lines:
    l = line.strip()
    holder.append(l)
  
  for y in range(0, len(holder)):
    for x in range(0, len(holder[0])):
      point = (x,y)
      output[point] = holder[y][x]
      if(holder[y][x] == "#"):
        elf_pos.append(point)
  return output, elf_pos

def PrintMap(map):
  max_x = max(list(map))[0]
  max_y = max(list(map))[1]
  min_x = min(list(map))[0]
  min_y = min(list(map))[1]
  for y in range(min_y - 1, max_y + 1):
    line = ""
    for x in range(min_x -1, max_x + 1):
      value = GetValue((x, y))
      line += value
    line+= str(y) + "\r"
    print(line)
  print(min_x-1, "------------", max_x)

def CalculateAir(elf_pos, debug=False):
  print("Calculando Aire..")
  output = 0
  #Now we get the limits of the elf square...
  min_x = sorted(elf_pos, key=lambda a: a[0], reverse=False)[0][0]
  max_x = sorted(elf_pos, key=lambda a: a[0], reverse=True)[0][0]
  min_y = sorted(elf_pos, key=lambda a: a[1], reverse=False)[0][1]
  max_y = sorted(elf_pos, key=lambda a: a[1], reverse=True)[0][1]
  if(debug):
    print("mX:", min_x, "MX:", max_x, "mY:", min_y, "MY:", max_y)
    #print("Elfs:", elf_pos)
  # We scan it and add to the output if its air
  for y in range(min_y, max_y + 1):
    for x in range(min_x, max_x + 1):
      if(GetValue((x,y)) == "."):
        output += 1
  return output

def GetValue(coord):
  global map
  value = map.get(coord, ".") # We will give back a T as in Teleport if it doesnt exist.
  return value

def DoARound(elf_pos, debug = False, p2= False):
  global map
  global rotation
  global can_move

  new_elf_pos = []
  if(debug):
    print("This round rotation =", rotation)
  for c, elf in enumerate(elf_pos):
    if(debug):
      print("Doing elf N" + str(c))
    move_to = TryMove(elf, rotation, debug)
    new_elf_pos.append(move_to)

  # Now that we finished checking the elf movements we check for dupes...
  new_elf_pos = CheckForDupesAndFixThem(elf_pos, new_elf_pos)

  # FOR PART 2
  if(p2):
    if(all(elem in elf_pos for elem in new_elf_pos) and (len(elf_pos) == len(new_elf_pos))):
      print("NO SE REALIZARON MOVIMIENTOS PARANDO.")
      can_move = False
      return
  # Actualizamos el mapa para que haya aire en las pos antiguas de los elfos, y luego colocamos las nuevas.
  for pos in elf_pos:
    map[pos] = "."
  for pos in new_elf_pos:
    map[pos] = "#"
  #for p, pos in enumerate(new_elf_pos):  # For debugging with numbers.
    #map[pos] = str(p)  # ACA TENIA el "#"

  # Giramos la rotation para la nueva vuelta
  d = rotation.pop(0)
  rotation.append(d)
  # Retornar el nuevo vvalor de elf_pos
  return new_elf_pos

def TryMove(elf,rotation, debug):
  # RETORNA UN VALOR (x,y) de a donde se quiere mover.
    around_elf = FindNewPos(elf)
    isAlone = True # We start assuming the elf is alone.
    # We check if the elf is surrounded by air
    for pos in around_elf:
      if GetValue(pos) == ".":
        continue
      else: # There is an elf around it.
        isAlone = False
        if(debug):
          debug_string = ""
          for i, cp in enumerate(around_elf):
            debug_string +=  str(i) +" " + str(GetValue(cp)) + " | "
          print(debug_string)
        # We do check based on round order
        for dir in rotation:
          # Check North
          if(GetValue(around_elf[0]) == "." and GetValue(around_elf[1]) == "." and GetValue(around_elf[7]) == "." and dir == "n"):
            #Move north
            if(debug):
              print("El elfo desea moverse al norte")
            return around_elf[0]

          # Check South
          if(GetValue(around_elf[3]) == "." and GetValue(around_elf[4]) == "." and GetValue(around_elf[5]) == "." and dir == "s"):
            # Move South
            if(debug):
              print("El elfo desea moverse al sur")
            return around_elf[4]

          # Check West
          if(GetValue(around_elf[5]) == "." and GetValue(around_elf[6]) == "." and GetValue(around_elf[7]) == "." and dir == "w"):
            #Move West
            if(debug):
              print("El elfo desea moverse al oeste")
            return around_elf[6]

          # Check East
          if(GetValue(around_elf[1]) == "." and GetValue(around_elf[2]) == "." and GetValue(around_elf[3]) == "." and dir == "e"):
            # Move East
            if(debug):
              print("El elfo desea moverse al este")
            return around_elf[2]

          # It cant move so it stays there  # This should only execute on the last rotation.
          if(dir == rotation[3]):
            if(debug):
              print("El elfo no tiene a donde moverse")
            return elf

    # If it is exits the for the elf is alone and does nothing..
    if(isAlone):
      if(debug):
        print("El elfo esta solo no se movera")
      return elf

def CheckForDupesAndFixThem(original, new):
  if(len(original) != len(new)):
    print("ERROR ARR LENGHTS ARE DIFFERENT!")
    print("O:", len(original), "N:", len(new))
    return None
  for i, pos in enumerate(new):
    for j, posc in enumerate(new):
      # if we find 2 different elf with the same movement planned.
      if(pos == posc and i != j):
        # We reset their location so they dont move.
        new[i] = original[i]
        new[j] = original[j]
  return new

def FindNewPos(pos):
#                  N      NE    E     SE     S     SW      W      NW
  new_pos_mod = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
  output = []
  for p in new_pos_mod:
    point = (pos[0] + p[0], pos[1] + p[1])
    output.append(point)
  return output

####### MAIN CODE #######
map, elf_pos = BuildDic(lines)
print("===ORIGINAL MAP===")
PrintMap(map)
# We do the rounds
n_of_rounds = 10
rotation = ["n","s","w","e"]

for x in range(0, n_of_rounds):
  print("=== STARTING ROUND",x+1,"===")
  elf_pos = DoARound(elf_pos, False)
  print("=== AFTER ROUND",x+1,"===")
  #PrintMap(map)
# We calculate the air at the min rectangle
air = CalculateAir(elf_pos, False)
print("El aire en el cuadrado es de", air, "bloques.")

print("====== PART 2 ======")
# Im assuming its more than 10 rounds...
can_move = True
while(can_move):
  n_of_rounds += 1
  print("Simulating Round N:", n_of_rounds)
  elf_pos = DoARound(elf_pos, False, p2=True)
  #PrintMap(map)
print("La 1era ronda donde no se mueve es la N:", n_of_rounds)
