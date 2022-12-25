from queue import PriorityQueue
from math import gcd


print('Leyendo Datos')
with open('./input.txt') as f:
  lines = f.readlines()

def CleanInput(input):
  output = []
  for l in input:
    clean = l.strip()
    output.append(clean)
  return output

def GetTheNumbers(input):
  print("Generating the numbers")
  output = []
  max_l = -5
  for l in input:
    if len(l) > max_l:
      max_l = len(l)
    output.append(l)
  # We add filler to the numbers that are not max l
  for i,n in enumerate(output):
    if(len(n) != max_l):
      agregar = max_l - len(n)
      new_string =""
      for x in range(0,agregar):
        new_string += "0"

      output[i] = new_string + output[i]

  return output

def SnafuArrToDec(arr):
  print("Convirtiendolos a decimales..")
  output = []
  max_l = len(arr[0])
  for number in arr:
    value = 0
    modifier = max_l - 1
    for letter in number:
      v = 5 ** modifier
      if(letter == "1"):
        value += (1 * v)
      if(letter == "2"):
        value += (2 * v)
      if(letter == "="):
        value -= (2 * v)
      if(letter == "-"):
        value -= (1 * v)
      modifier -= 1
    output.append(value)
  return output

def SnafuToDec(n):
  #print("Convirtiendo", n, "a decimal")
  output = 0
  max_l = len(n)
  modifier = max_l - 1
  for letter in n:
    v = 5 ** modifier
    if(letter == "0"):
      value = 0
    if(letter == "1"):
      value = (1 * v)
    if(letter == "2"):
      value = (2 * v)
    if(letter == "="):
      value = (-2 * v)
    if(letter == "-"):
      value = (-1 * v)
    modifier -= 1
    output += value
  return output

def SumDecimals(arr):
  print("Sumando...")
  result = 0
  for number in arr:
    result += number
  print("El resultado de la suma es de", result)
  return result    

def DecimalToBase5(number):
  result = []
  rest = number
  while((rest != 0) or (number != 0)) :
    Bnumber = number
    number = number // 5
    rest = Bnumber - (number * 5)
    result.append(rest)

  result.reverse()
  result.pop(0)
  output = ""
  for n in result:
    output += str(n)
  print("El num en base 5 es", output)
  return int(output)

def Base5toSnafu(number):
  print("Convirtiendo a SNAFU")
  output = ""
  dic = { -2:"=", -1:"-", 0:"0", 1:"1", 2:"2"}
  carry_over = 0
  for n in range(len(str(number)) -1, -1, -1):
    digit = int(str(number)[n]) + carry_over
    # Reset the carry over
    carry_over = 0
    if(digit > 2):
      digit = digit - 5
      carry_over = 1
    output = dic[digit] + output

  print("Convertido:", output)
  return output


# MAIN CODE
lines = CleanInput(lines)
snafu_numbers = GetTheNumbers(lines)
#print(snafu_numbers)
dec_arr = SnafuArrToDec(snafu_numbers)
#print(dec_arr)
sum = SumDecimals(dec_arr)
base5 = DecimalToBase5(sum)
result = Base5toSnafu(base5)


