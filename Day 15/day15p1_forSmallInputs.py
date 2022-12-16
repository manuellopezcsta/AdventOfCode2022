print('Leyendo Datos')
with open('Day 15/input.txt') as f:
  lines = f.readlines()
# THIS SOLUTION WORKS ON SMALL MAPS Q_Q NOT BIG ONES
# LIKE THE REAL INPUT Q_Q


def ReadInput(lines):
  output = []
  #Returns an array of type [[sensor,beacon],[sensor2, beacon2]]
  for line in lines:
    l = line.strip()
    x = l.split("Sensor at x=")[1].split(",")[0]
    x = int(x)
    y = l[l.index("y") + 2:].split(":")[0]
    y = int(y)
    #print("Sensor at X:", x, "Y:", y)
    bx = l.split("Sensor at x=")[1].split("x=")[1].split(",")[0]
    #print(bx)
    bx = int(bx)
    by = l.split("closest beacon is at ")[1].split("y=")[1]
    by = int(by)
    #print(by)
    point = (x, y)
    b_point = (bx, by)
    holder = []
    holder.append(point)
    holder.append(b_point)
    output.append(holder)

  return output


def GetMinMaxValues(input):
  currentX_max = 0
  currentY_max = 0
  currentX_min = 0
  currentY_min = 0
  for x in input:
    for element in x:
      x = element[0]
      if (currentX_max < x):
        currentX_max = x
      if (currentX_min > x):
        currentX_min = x

      y = element[1]
      if (currentY_max < y):
        currentY_max = y
      if (currentY_min > y):
        currentY_min = y
  print("MAX X:", currentX_max, "MAX Y:", currentY_max)
  print("MIN X:", currentX_min, "MIN Y:", currentY_min)
  return currentX_max, currentY_max, currentX_min, currentY_min


def BuildMap(coords, minxX, minY, maxX, maxY):
  print("Building Map...")
  output = {}
  #Generate the normal map with air.
  for x in range(minxX, maxX + 1):
    for y in range(minY, maxY + 1):
      point = (x, y)
      output[point] = "o"

  #We add the beacon and sensors to the dic
  for x in coords:
    sensor = x[0]
    beacon = x[1]
    output[sensor] = "S"
    output[beacon] = "B"

  return output


def GetValueFromPoint(point):
  # If it doesnt exist, it creates it.
  global map_dic
  value = map_dic.get(point, "o")
  return value


def DrawSensorToBeacon(pair):
  global map_dic
  sensor = pair[0]
  print("Simulating Sensor at: ", sensor)
  beacon = pair[1]
  abs_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
  print("ABS DISTANCE:", abs_distance)
  # We draw first the 4 points if they are not stuff and then
  # We draw the diagonals...
  for n in range(1, abs_distance + 1):
    points = [(sensor[0], sensor[1] - n), (sensor[0] + n, sensor[1]),
              (sensor[0], sensor[1] + n), (sensor[0] - n, sensor[1])]
    for p in points:
      value_on_point = GetValueFromPoint(p)
      if (value_on_point == "o"):
        map_dic[p] = "#"
    #Linea de arriba a abajo a la derecha
    p1 = points[0]
    p2 = points[1]
    add_point = p1  # p1 +1 +1 para ir hacia abajo
    while (add_point != (p2)):
      add_point = (add_point[0] + 1, add_point[1] + 1)
      value = GetValueFromPoint(add_point)
      if (value == "o"):
        map_dic[add_point] = "#"
    #Linea de la derecha a abajo
    p1 = points[1]
    p2 = points[2]
    add_point = p1  # p1 -1 +1 para ir hacia abajo a la izq
    while (add_point != (p2)):
      add_point = (add_point[0] - 1, add_point[1] + 1)
      value = GetValueFromPoint(add_point)
      if (value == "o"):
        map_dic[add_point] = "#"
    #Linea abajo a medio izq
    p1 = points[2]
    p2 = points[3]
    add_point = p1  # p1 -1 -1 para ir hacia arriba la izq
    while (add_point != (p2)):
      add_point = (add_point[0] - 1, add_point[1] - 1)
      value = GetValueFromPoint(add_point)
      if (value == "o"):
        map_dic[add_point] = "#"
    #Linea izquierda medio a arriba
    p1 = points[3]
    p2 = points[0]
    add_point = p1  # p1 +1 -1 para ir hacia arriba la izq
    while (add_point != (p2)):
      add_point = (add_point[0] + 1, add_point[1] - 1)
      value = GetValueFromPoint(add_point)
      if (value == "o"):
        map_dic[add_point] = "#"


def ScanRowForNoBeacon(y_number, minX, maxX):
  print("Escaneando linea n:", y_number)
  holder = []
  result = 0
  for x in range(minX - 5000, maxX + 5000):
    point = (x, y_number)
    value = GetValueFromPoint(point)
    holder.append(value)
  for item in holder:
    if item == "#":
      result += 1
  return result


############### MAIN CODE ###############
coords = ReadInput(lines)
max_x, max_y, min_x, min_y = GetMinMaxValues(coords)
map_dic = BuildMap(coords, min_x, min_y, max_x, max_y)
#print(map_dic[(2,9)])

for pair in coords:
  DrawSensorToBeacon(pair)
#DrawSensorToBeacon(coords[0])

# We count the asked line
result = ScanRowForNoBeacon(10, min_x, max_x)
print("Hay", result, "espacios en la linea esa.")

#DIBUJAMOS
print("Dibujando..")
dibujo = open("test.txt", "w")
for y in range(min_y, max_y + 1):
  linea = ""
  for x in range(min_x - 10, max_x + 10):
    linea += GetValueFromPoint((x, y))
  linea += "\n"
  dibujo.write(linea)
dibujo.close()
print("Finished.")