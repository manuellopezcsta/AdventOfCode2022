print('Leyendo Datos')
with open('Day 20/input.txt') as f:
  lines = f.readlines()


def BuildArray(lines):
  output = []
  for l in lines:
    q = int(l.strip())
    output.append(q)
  return output


def MoveNumber(i, orig_arr, mixed, debug=True):
  # i index
  number = orig_arr[i]
  if(debug):
    print(number, "Arr Before", mixed)
  arr_len = len(orig_arr)
  new_index = 0
  curr_index = mixed.index((i, number))
  new_index = ((curr_index + number) % (arr_len-1))
      
  # X si queda negativo le sumo arr lenght q seria como 1 vuelta
  # gratis.. para q quede positivo.. 
  # Y si es positivo no le hace nada...
  # Es -1 xq quitamos un elemento al moverlo..
  new_index=(new_index+arr_len-1)%(arr_len-1)
  p = mixed.pop(curr_index)
  mixed.insert(new_index, p)
  if(debug):
    print("N:", number, "After", mixed,"CI:",curr_index, "NI:", new_index)
    print("------------------------")
  return mixed


def GetAndAddCoordinates(original, input):
  # We find the index of 0.
  i = original.index(0)
  i = input.index((i,0))
  l = len(input)
  holder = [1000, 2000, 3000]
  result = 0
  # Now we find the values.
  for valor in holder:
    v1 = (i + valor)%l
    v1 = input[v1][1]
    print("Valor en:", valor, v1)
    result += v1
  print("Resultado Final:", result)


#### MAIN CODE ####
original_order = BuildArray(lines)
#print("ORIGINAL:", original_order)
arr_len = len(original_order)
mixed_arr = [(i, n) for (i, n) in enumerate(original_order)]

print("Realizando Movimientos...")
for x in range(0, arr_len):
  mixed_arr = MoveNumber(x, original_order, mixed_arr, False)

print("Obteniendo Valores..")
GetAndAddCoordinates(original_order, mixed_arr)

def DoARound(arr_len, original_order, mixed_arr):
  for x in range(0, arr_len):
    mixed_arr = MoveNumber(x, original_order, mixed_arr, False)


print("==== PARTE 2 ====")
big_nums = []
for count, i in enumerate(original_order):
  big_nums.append((count, i * 811589153))

# Wre recreate original order
for x in range(0, len(original_order)):
  original_order[x] *= 811589153
  
# We do the rounds
for x in range(0,10):
  print("Realizando Ronda", x + 1)
  DoARound(arr_len, original_order, big_nums)

print("Obteniendo Valores P2..")
GetAndAddCoordinates(original_order, big_nums)
