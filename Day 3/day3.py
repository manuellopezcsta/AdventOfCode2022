print('Leyendo Datos')
with open('Day 3/input.txt') as f:
    lines = f.readlines()
# Uso strip xq sigo lee el final de linea como un caracter extra..

mitad = 0
# Con sacar su indice y sumarle 1 tengo el valor.
valores = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
total = 0
contador = 1
fails = 0;

for stuff in lines:
  mitad = int(len(stuff.strip())/2)
  #print(mitad)
  first_part = stuff[0:mitad]
  second_part = stuff[mitad:(mitad*2)]
  #print(first_part)
  #print(second_part)

  for letter in first_part:
    find = False
    if letter in second_part:
      peso = valores.index(letter) + 1
      #print("Linea " + str(contador) + "- " +"Letra: " + letter + " Valor de letra: " + str(peso))
      total+= peso
      contador+=1
      find = True
      break;
      
    if(find):
      break

print("El total es de: " + str(total))

#PARTE 2
total = 0
contador=0
for group in range(0, 299,3):
  #print(group)
  #print((group)+1)
  #print((group)+2)
  first_elf = lines[group].strip()
  second_elf = lines[(group)+1].strip()
  third_elf = lines[(group)+2].strip()

  contador+=1

  for letter in first_elf:
    if letter in second_elf:
      if letter in third_elf:
        peso = valores.index(letter) + 1
        #print("Grupo " + str(contador) + "- Letra " + letter + "/ Valor " + str(peso))
        total+= peso
        break
print("Peso Medallas total: " + str(total))