print('Leyendo Datos')
with open('Day 1/input.txt') as f:
    lines = f.readlines()
result = 0
elf_calories = []

print('Organizandolos segun elfos')
for item in lines:
  if(item.strip() != ''):
    result += int(item)
  else:
    ##print(result)
    elf_calories.append(result)
    result = 0

print('Buscando el de mayor valor calorico');
max_value = max(elf_calories)
print("La maxima cant de calorias es "+ str(max_value))

print("Calculando la suma calorias top 3")
top3 = max_value
for x in range(2):
  elf_calories.remove(max_value)
  max_value = max(elf_calories)
  ##print(max_value)
  top3 += max_value

print('La suma top 3 es ' + str(top3))