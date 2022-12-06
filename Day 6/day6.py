from collections import Counter


print('Leyendo Datos')
with open('Day 6/input.txt') as f:
  line = f.readlines()


start_of_signal_found = False
keyFinal = ""
contador = 0

def CheckForSignal(signalLen):
  global contador
  signal = line[0][contador:(contador + signalLen)]
  # Check if they are the same if they are print contador
  freq = Counter(signal)
  if(len(freq) == len(signal)):
    global keyFinal
    keyFinal = signal
    #Le sumamos para que este bien el indice q pide la respuesta.
    contador+= signalLen
    global start_of_signal_found
    print(" La key era: " + keyFinal +" y el num es:" + str(contador))
    start_of_signal_found = True
  else:
    contador+= 1

while (not start_of_signal_found):
  # We do 4 for part 1
  CheckForSignal(4)

start_of_signal_found = False
contador = 0

while (not start_of_signal_found):
  # We do 14 for part 2
  CheckForSignal(14)