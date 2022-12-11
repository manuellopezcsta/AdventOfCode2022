import math 


print('Leyendo Datos')
with open('Day 11/input.txt') as f:
  lines = f.readlines()

class Monkey:
  def __init__(self, number, items, op, test, true_to_n, false_to_n,times_inspected):
    #Number that identifies the monkey
    self.number = number
    #Array with the worry levels
    self.items = items
    # Operation it realises to items its in string
    self.op = op
    # number to see if its disivible by
    self.test = test 
    #If true go to monkey n
    self.true_to_n = true_to_n
    #If false go to monkey n
    self.false_to_n = false_to_n
    #How many times it inspected something
    self.times_inspected = times_inspected

  def debug_monkey_stuff(self):
    print("Monkey N:", self.number)
    print("Monkey Items:", self.items)
    print("Monkey Op:", self.op)
    print("Monkey Test:", self.test)
    print("Monkey True:", self.true_to_n)
    print("Monkey False:", self.false_to_n)
    print("Items Inspected:", self.times_inspected)
    print("=============================")

monkey_array = []

# We build the monkeys !
for x in range(0, len(lines)):
  line = lines[x].strip()
  if(line.startswith("Monkey ")):
    # We get the monkey N
    monkey_number = int(line.split("Monkey ")[1].replace(":", ""))
    # We get its numbers
    monkey_starting_items = []
    data = lines[x+1].split("Starting items: ")[1]
    holder = data.split(",")
    for item in holder:
      monkey_starting_items.append(int(item.strip()))
    # We get its operation
    operation = lines[x+2].split("Operation: new = ")[1]
    operation = operation.strip()
    # We get the test number
    test = int(lines[x+3].split("Test: divisible by ")[1])
    # We get the true monkey number
    true_n = int(lines[x+4].split("If true: throw to monkey ")[1])
    # We get the false monkey number
    false_n = int(lines[x+5].split("If false: throw to monkey ")[1])

    #We give the data to the monkey :D!
    new_monkey = Monkey(monkey_number, monkey_starting_items,
                       operation, test, true_n, false_n, 0)
    monkey_array.append(new_monkey)
    print("Added Monkey Number", monkey_number)

#We finished reading the input file
print("======= DONE =======\r")

def resolve_monkey_round(monkey):
  #print(monkey.items,"FOR MONKEY")
  for x in list(monkey.items):
    #We add 1 to items inspected
    monkey.times_inspected += 1
    #Relisamos la Op
    new = 0
    old = x
    new = int(math.trunc(eval(monkey.op)/3))
    #print("New worry lv:", new)
    #Update the value of the item
    # Puede llegar a causar problemas
    item_index = monkey.items.index(x)
    monkey.items[item_index] = new
    # We check the Test
    current_item = monkey.items.pop(0)
    if(new % monkey.test == 0):
      monkey_array[monkey.true_to_n].items.append(current_item)
    else:
      monkey_array[monkey.false_to_n].items.append(current_item)
  #print("Monkey N" + str(monkey.number) + " resolved.")

# We do the monkey rounds now
for x in range(0,20):
  for monkey in monkey_array:
    resolve_monkey_round(monkey)

# We find the monkey buisness
max_values = []
for monkey in monkey_array:
  print("=============================")
  monkey.debug_monkey_stuff()
  max_values.append(monkey.times_inspected)

valor_max = max_values.pop(max_values.index(max(max_values)))
monkey_buisness_lv = valor_max
valor_max = max_values.pop(max_values.index(max(max_values)))
monkey_buisness_lv *= valor_max
print("LV DE MONKEY BUISNESS:", monkey_buisness_lv)