print('Leyendo Datos')
with open('Day 2/input.txt') as f:
    lines = f.readlines()

total_points = 0

for match in lines:
  #Sumo los puntos de mi eleccion
  if(match[2]== 'X'):
    total_points+=1
  if(match[2]== 'Y'):
    total_points+=2
  if(match[2]== 'Z'):
    total_points+=3
  # Reviso si gane o perdi y sumo puntos.
    #Rocas
  if(match[2]== 'X' and match[0]== 'A' ):
    total_points+=3
  if(match[2]== 'X' and match[0]== 'C' ):
    total_points+=6
    #Papeles
  if(match[2]== 'Y' and match[0]== 'B' ):
    total_points+=3
  if(match[2]== 'Y' and match[0]== 'A' ):
    total_points+=6
    #Tijeras
  #Papeles
  if(match[2]== 'Z' and match[0]== 'C' ):
    total_points+=3
  if(match[2]== 'Z' and match[0]== 'B' ):
    total_points+=6

print('Total puntos: ' + str(total_points))

# Part 2
total_points = 0

for match in lines:
  #Sumo los puntos del resultado
  if(match[2]== 'Y'):
    total_points+= 3
  if(match[2]== 'Z'):
    total_points+= 6
  # Analisamos los casos ahora para ver cuanto sumamos x nuestra eleccion.
    #Perder
  if(match[2]== 'X' and match[0]== 'A' ):
    total_points+=3
  if(match[2]== 'X' and match[0]== 'B' ):
    total_points+=1
  if(match[2]== 'X' and match[0]== 'C' ):
    total_points+=2
      #Empatar
  if(match[2]== 'Y' and match[0]== 'A' ):
    total_points+=1
  if(match[2]== 'Y' and match[0]== 'B' ):
    total_points+=2
  if(match[2]== 'Y' and match[0]== 'C' ):
    total_points+=3
        #Ganar
  if(match[2]== 'Z' and match[0]== 'A' ):
    total_points+=2
  if(match[2]== 'Z' and match[0]== 'B' ):
    total_points+=3
  if(match[2]== 'Z' and match[0]== 'C' ):
    total_points+=1

print('Resultado nueva strat: ' + str(total_points))