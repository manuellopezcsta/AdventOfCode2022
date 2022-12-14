from functools import cmp_to_key


print('Leyendo Datos')
with open('Day 13/input.txt') as f:
  lines = f.readlines()


def BuildPairs(input_array):
  
  
  print("Armando pares...")
  output = []
  pair = []
  for x in lines:
    j = x.strip()
    #We separate at the empty string and reset the pair
    if (j == ""):
      output.append(pair)
      pair = []
    # We add to the pair
    else:
      data = eval(j)
      pair.append(data)
  # We append the last one since there is no space to do it for us
  output.append(pair)
  return output

def CompareItem(signal1, signal2):
  """
  0 igual
  neg signal1<signal2
  pos signal1>signal2"""
  if(type(signal1) == int and type(signal2) == int):
    return signal1 - signal2
  elif type(signal1) == int and type(signal2) == list:
    return CompareItem([signal1], signal2)
  elif type(signal1) == list and type(signal2) == int:
    return CompareItem(signal1, [signal2])
  else: # los dos lista
    l_s1 = len(signal1)
    l_s2 = len(signal2)
    # We compare stuff
    for x in range(0, min(l_s1, l_s2)):
      comp = CompareItem(signal1[x], signal2[x])
      if comp != 0:
        return comp

    if l_s1 == l_s2:
      return 0 # son igales
    elif l_s1 < l_s2:
      return -1
    else:
      return 1

def SumIndexes(results):
  index_final = 0
  for x in results:
    if x <= 0:
     index_final += results.index(x) + 1
  return index_final

# Version usando enumerate
def SumIndexes(results):
  index_final = 0
  for i, x in enumerate(results):
    if x <= 0:
     index_final += i + 1
  return index_final
  
  
# Main Code
pairs = BuildPairs(lines)
results = []
for x in pairs:
  results.append(CompareItem(x[0],x[1]))
#print(results)
index_final = SumIndexes(results)


print(" La suma de indices es:", index_final)



print("##### PARTE 2 #####")

def NewImput(pairs):
  results = []
  for x in pairs:
    results.append(x[0])
    results.append(x[1])
  results.append([[2]])
  results.append([[6]])
  return results
def GetFinalValue(sorted_array):
  index1 = sorted_array.index([[2]]) + 1
  index2 = sorted_array.index([[6]]) + 1
  print("El valor final es de:",index1 * index2)

# New Input for part 2

#CUSTOM SORTER
input = NewImput(pairs)
sorted_input = sorted(input, key=cmp_to_key(CompareItem))
# We find the indexes and multiply them
GetFinalValue(sorted_input)