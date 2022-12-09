print('Leyendo Datos')
with open('Day 9/input.txt') as f:
  lines = f.readlines()
  
starting_point = (0, 0)
current_head_point = (0, 0)
head_positions = [(0,0)]

# Poblamos todas las posiciones que visita
for line in lines:
  line = line.strip()
  if(line.startswith("U")):
    data = int(line.split("U ")[1])
    for x in range (1, data + 1):      
      new_head_point = (current_head_point[0], current_head_point[1] + x)
      head_positions.append(new_head_point)
  if(line.startswith("D")):
    data = int(line.split("D ")[1])
    for x in range (1, data + 1):    
      new_head_point = (current_head_point[0], current_head_point[1] - x)
      head_positions.append(new_head_point)
  if(line.startswith("R")):
    data = int(line.split("R ")[1])
    for x in range (1, data + 1):
      new_head_point = (current_head_point[0] + x, current_head_point[1])
      head_positions.append(new_head_point)
  if(line.startswith("L")):
    data = int(line.split("L ")[1])
    for x in range (1, data + 1):
      new_head_point = (current_head_point[0] - x, current_head_point[1])
      head_positions.append(new_head_point)
  #Actualizamos al nuevo headpoint
  current_head_point = head_positions[len(head_positions) -1]

#Ahora que ya tenemos el array listo ?
print("Array con movimientos ya ha sido generado")
tail_positions = []
c_tail_pos = (0,0)

for x in range(0, len(head_positions)):
  caso = -1
  h_c_pos = head_positions[x]
  distance_x = abs(h_c_pos[0] - c_tail_pos[0])
  distance_y = abs(h_c_pos[1] - c_tail_pos[1])

  if(distance_x == 0 and distance_y == 0):
    caso = 0
    tail_positions.append(c_tail_pos)

  # Si la distancia es de solo 1 en alguno de los 2
  elif((distance_x == 1 and distance_y < 2) or (distance_y == 1 and distance_x < 2)):
    caso = 1
    tail_positions.append(c_tail_pos)
    
  elif(distance_x == 2 or distance_y == 2):
    caso = 2
    #Si solo se mueve en eje x y no en diagonal
    if(distance_x == 2 and distance_y == 0):
      caso = 2.5
      point1 = (c_tail_pos[0] + 1, c_tail_pos[1])
      point2 = (c_tail_pos[0] - 1, c_tail_pos[1])
      if(abs(h_c_pos[0] - point1[0]) == 1):
        # Es el punto 1
        c_tail_pos = point1
      else:
        c_tail_pos = point2
      tail_positions.append(c_tail_pos)
        
    #Si solo se mueve en eje y, pero no en diagonal
    elif(distance_x == 0 and distance_y == 2):
      caso = 3
      point1 = (c_tail_pos[0], c_tail_pos[1] + 1)
      point2 = (c_tail_pos[0], c_tail_pos[1] - 1)
      if(abs(h_c_pos[1] - point1[1]) == 1):
        # Es el punto 1
        c_tail_pos = point1
      else:
        c_tail_pos = point2
        
      tail_positions.append(c_tail_pos)
    
    # Si se tiene que mover en diagonal
    else:
      caso = 4
      point1 = (c_tail_pos[0] + 1,c_tail_pos[1] + 1)
      point2 = (c_tail_pos[0] - 1,c_tail_pos[1] - 1)
      point3 = (c_tail_pos[0] + 1,c_tail_pos[1] - 1)
      point4 = (c_tail_pos[0] - 1,c_tail_pos[1] + 1)
      # We check which point is closer to the head
      if(abs(point1[0] - h_c_pos[0]) <= 1):
        #Es el punto 1 o 3
        if(abs(point1[1] - h_c_pos[1]) > 1):
          # Es el 3
          c_tail_pos = point3
        else:
          # Es el 1
          c_tail_pos = point1
      elif(abs(point2[0] - h_c_pos[0]) <=1):
        #Es el punto 2 o 4.
        if(abs(point2[1] - h_c_pos[1]) > 1):
          # Es el 4
          c_tail_pos = point4
        else:
          # Es el 2
          c_tail_pos = point2
            
      # Guardamos el punto correcto    
      tail_positions.append(c_tail_pos)

print("Array con movimientos cola ya ha sido generado")
print("Buscando dupes..")

#Buscamos repetidos en colas
unique_tails_pos = list(set(tail_positions))

# Printeamos la cantidad de posiciones que estuvo la cola
print("La cola estubo en", len(unique_tails_pos), "posiciones")
print("=== PARTE 2 ===")
knot_2 = []
knot_3 = []
knot_4 = []
knot_5 = []
knot_6 = []
knot_7 = []
knot_8 = []
knot_9 = []

sign = lambda a: (a>0) - (a<0)

c_knot_pos = (0,0)
def calculatePosNodeBasedOnLastOne (pastKnot):
  global c_knot_pos
  distance_x = abs(pastKnot[0] - c_knot_pos[0])
  distance_y = abs(pastKnot[1] - c_knot_pos[1])
  # Calculo el simbolo del movimiento 
  signx = sign(pastKnot[0] - c_knot_pos[0])
  signy = sign(pastKnot[1] - c_knot_pos[1])
  #Si se mueve devuelvo el nuevo valor
  if (signx != 0 or signy != 0) and max(distance_x,distance_y)>1:
    return (c_knot_pos[0]+signx,c_knot_pos[1]+signy)
  #Sino devuelvo el mismo
  else:
    return c_knot_pos

  

# Para el knot 2
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(tail_positions[x])
  knot_2.append(c_knot_pos)
c_knot_pos = (0,0)

# Para el knot 3
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(knot_2[x])
  knot_3.append(c_knot_pos)
c_knot_pos = (0,0)

# Para el knot 4
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(knot_3[x])
  knot_4.append(c_knot_pos)
c_knot_pos = (0,0)

# Para el knot 5
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(knot_4[x])
  knot_5.append(c_knot_pos)
c_knot_pos = (0,0)

# Para el knot 6
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(knot_5[x])
  knot_6.append(c_knot_pos)
c_knot_pos = (0,0)

# Para el knot 7
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(knot_6[x])
  knot_7.append(c_knot_pos)
c_knot_pos = (0,0)

# Para el knot 8
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(knot_7[x])
  knot_8.append(c_knot_pos)
c_knot_pos = (0,0)

# Para el knot 9
for x in range(0, len(tail_positions)):
  c_knot_pos = calculatePosNodeBasedOnLastOne(knot_8[x])
  knot_9.append(c_knot_pos)
c_knot_pos = (0,0)

print("LEN DE TAILS ",len(tail_positions))
print("Len knot 2", len(knot_2))
print("Len knot 3", len(knot_3))
print("Len knot 4", len(knot_4))
print("Len knot 5", len(knot_5))
print("Len knot 6", len(knot_6))
print("Len knot 7", len(knot_7))
print("Len knot 8", len(knot_8))
print("Len knot 9", len(knot_9))
#Usamos un set, ya que estos no pueden tener cosas repetidas
print("La cola de 10 nudos estubo en ",len({x for x in knot_9}), "posiciones")
print("Done")