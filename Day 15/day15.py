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



def GetValueFromPoint(point):
  # If it doesnt exist, it creates it.
  global map_dic
  value = map_dic.get(point, "o")
  return value


def CalculateRangeFromPair(pair):
  sensor = pair[0]
  #print("Sensor at: ", sensor)
  beacon = pair[1]
  abs_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
  return abs_distance
  #print("ABS DISTANCE:", abs_distance)


def ScanRowForNoBeacon(y_number, minX, maxX, coords, beacon_list):
  print("Escaneando linea n:", y_number)
  holder = set()
  beacon_set = set(beacon_list)
  result = 0
  for pair in coords:
    signal_radius = CalculateRangeFromPair(pair)
    if(pair[0][1] + signal_radius < y_number ):
      print("Skipping this sensor , doesnt reach")
      continue # If sensor + abs is less than the y, continue
    print("Scanning Beacon of signal range:", signal_radius)
    for x in range(min_x -1780270, max_x + 1780270):
      if((x,y_number) in beacon_set):
        # If its a beacon we skip it.
        continue
      sensor_to_point_radius = CalculateRangeFromPair([pair[0], (x, y_number)])
      if(signal_radius >= sensor_to_point_radius):
        # Si esta dentro del rango, sumamos 1 al resultado
        holder.add((x, y_number))
  result = len(holder)
  #print(sorted(list(holder)))
  return result

def GenerateBeaconList(coords):
  result = []
  for element in coords:
    result.append(element[1])
  return result

############### MAIN CODE ###############
coords = ReadInput(lines)
beacon_list = GenerateBeaconList(coords)
max_x, max_y, min_x, min_y = GetMinMaxValues(coords)
#result = ScanRowForNoBeacon(10, min_x, max_x, coords, beacon_list) #2000000
#print("Espacios Vacios en esa linea:", result)

print("############ PARTE 2 ############")


def ScannerP2(maxX, maxY, coords):
  for x in range(0, maxX +1):
    if x % 100000 == 0:
      print("Escaneando linea x:", x, "de", maxX)
    y = 0
    while y < maxY +1:
      point = (x,y)
      flag = True
      for pair in coords:
        signal_radius = CalculateRangeFromPair(pair)
        v_point = CalculateRangeFromPair([pair[0], point])
        if(signal_radius >= v_point):
          y+= signal_radius - v_point
          flag = False
          break
      if(flag):
        return point
      y +=1

  ######### MAIN CODE

point = ScannerP2(4000000, 4000000, coords)
print("Se encontro! El Punto es:", point, "y la tuning frequency es de:", (point[0] * 4000000) + point[1])