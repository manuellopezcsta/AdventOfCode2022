print('Leyendo Datos')
with open('Day 10/input.txt') as f:
  lines = f.readlines()

#Starts on cycle 1
#Shows value at the end of each cycle
signal_x_per_cycle = []
signal_value = 1

def calculateNewSignalValue(instruction):
  global signal_value
  if (instruction.startswith("noop")):
    #It adds the same signal after 1 cycle.
    signal_x_per_cycle.append(signal_value)
  else:
    value = int(instruction.split("addx ")[1])
    #First cycle same value
    signal_x_per_cycle.append(signal_value)
    #Second cycle adds new value
    signal_value += value
    signal_x_per_cycle.append(signal_value)

def calculate_strenght_during_cycle(cycle_number):
  fuerza = cycle_number * signal_x_per_cycle[cycle_number-2]
  return fuerza

def sum_signals_strenghts(lastcylce, everyXcycles):
  totalSum = 0
  for x in range (20, lastcylce +1, everyXcycles):
    #Como pide DURING EL CYCLE y no al terminar, le damos el valor anterior
    totalSum += calculate_strenght_during_cycle(x)
    print("Cyc:", x, "X:", str(signal_x_per_cycle[x-2]), "V:", str(calculate_strenght_during_cycle(x)), "Sum:", totalSum)
  return totalSum

# We fill the array of cycles
for x in lines:
  data = x.strip()
  calculateNewSignalValue(data)

# We print the ones we want and add them cycle is index-1
# So cycle 1 would be index 0
  
result = sum_signals_strenghts(220, 40)
print("La suma de la fuerza de la signal es de:", str(result))
print("=== PART 2 ===")
for x in range(1,7):
  linea_final = ""
  for k in range(0,40):
    cycle_n = (x-1)*40 + k + 1
    if(cycle_n == 1):
      x_pixel_value = 1
    elif(cycle_n == 2):
      x_pixel_value = signal_x_per_cycle[0]
    else:
      x_pixel_value = signal_x_per_cycle[cycle_n-2]
    #print(x_pixel_value)
    if(x_pixel_value == k):
      linea_final += "#"
    elif(x_pixel_value == k-1):
      linea_final += "#"
    elif(x_pixel_value == k+1):
      linea_final += "#"
    else:
      linea_final += "."
    #print("Cycle:", cycle_n, "Valor Durante ciclo:", x_pixel_value, "Sprite:", linea_final[-1])
  print(linea_final)