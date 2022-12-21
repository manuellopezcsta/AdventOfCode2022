print('Leyendo Datos')
with open('./input.txt') as f:
  lines = f.readlines()


monkey_values = {} # Contains the name of the monkey and its value.
unknow_monkeys = {}
monkey_uses = {}

def BuildDic():
    global monkey_values
    global unknow_monkeys
    global p2
    for x in lines:
        line = x.strip()
        monkey_name = line.split(":")[0]
        value =line.split(": ")[1]
        # If it has numbers we just add them to the list.
        if(has_numbers(value)):
            monkey_values[monkey_name] = int(value)
        else:
            # We just store it and save the variable names in a diff array.
            monkey1 = value.split(" ")[0]
            monkey2 = value.split(" ")[2]
            if(monkey_name == "root" and p2):
                op = "=="
            else:
                op = value.split(" ")[1]
            holder = [monkey1, monkey2, op]
            unknow_monkeys[monkey_name] = holder


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def SolveMonkey(key_name):
    global monkey_values
    global unknow_monkeys
    # If it was solved already just return
    if(key_name in monkey_values.keys()):
        #print("Mono ya tiene un valor def, volviendo.")
        return
    #print("Intentando resolver:", key_name)
    m1 = TryGetMonkeyData(unknow_monkeys[key_name][0])
    m2 = TryGetMonkeyData(unknow_monkeys[key_name][1])
    if(m1 != "" and m2 != ""):
        op = unknow_monkeys[key_name][2]
        result = 0
        if(op == "+"):
            result = m1 + m2
        elif(op == "-"):
            result = m1 - m2
        elif(op == "*"):
            result = m1 * m2
        elif(op == "/"):
            result = m1 / m2
        elif(op == "=="):
            # Caso de root para p2
            result = (m1 == m2)
        else:
            print("ERROR UNKNOWN OP:", op)
            return
        GetMonkeyOrder(key_name)
        
        
        monkey_values[key_name] = result
        unknow_monkeys.pop(key_name)
        #print("Se resolvio mono:", key_name,":", m1, op, m2, "=", result)
    else:
        return

def GetMonkeyOrder(key_value):
  global monkey_uses
  global unknow_monkeys
  output = []
  m1 = unknow_monkeys[key_value][0]
  m2 = unknow_monkeys[key_value][1]
  if(m1 not in monkey_uses):
    output += [m1]
  if(m2 not in monkey_uses):
    output += [m2]
  if(m1 in monkey_uses.keys()):
    output += monkey_uses[m1]
  if(m2 in monkey_uses.keys()):
    output += monkey_uses[m2]  
  
  monkey_uses[key_value] = output

def TryGetMonkeyData(monkey_name):
    global monkey_values
    value = monkey_values.get(monkey_name, "")
    return value

def ChangeInput(value):
    global monkey_values
    monkey_values["humn"] = value

def BruteForceP2(test_value):
    print("Intentando valor:", test_value)
    # Return True or False
    global monkey_values
    global unknow_monkeys
    monkey_values = {}
    unknow_monkeys = {}
    BuildDic()
    ChangeInput(test_value)
    x = 0
    while(type(TryGetMonkeyData("root")) != bool):
        if(len(unknow_monkeys.keys()) -1 >= x):
            SolveMonkey(list(unknow_monkeys.keys())[x])
            x +=1
        else:
            x = 0
    # Una vez que tenemos el resultado.
    if(TryGetMonkeyData("root") == False):
        return False
    else:
        print("Valor que cumple con la equidad:", test_value)
        return True

def GetRootMonkeys():
    output = [unknow_monkeys["root"][0], unknow_monkeys["root"][1]]
    return output

def SolveP2(root_monkeys):
    global monkey_values
    global unknow_monkeys
    global monkey_uses
    # WE store the value of the final monkeys..
    m1v = monkey_values[root_monkeys[0]]
    m2v = monkey_values[root_monkeys[1]]

    # We find out which one doesnt use the input humn
    monkey_values = {}
    unknow_monkeys = {}
    BuildDic() # We clear the dic to get the values.
    monkey1 = unknow_monkeys["root"][0]
    monkey2 = unknow_monkeys["root"][1]

    if("humn" in monkey_uses[monkey1]):
        print("El input esta en el mono 1", monkey1)
        # Guardamos el resuelto
        monkey_values[monkey2] = m2v
        monkey_values[monkey1] = m2v


    if("humn" in monkey_uses[monkey2]):
        print("El input esta en el mono 2", monkey2)
        #Guardamos el resuelto
        monkey_values[monkey1] = m1v
        monkey_values[monkey2] = m1v
    
    # Retiramos el valor de humn para que no cause problemas
    monkey_values.pop('humn', None)
    # We get the solve order for the side we already know
    order = GetSolveOrder(monkey_uses, False)
    for monkey in order:
        SolveMonkey(monkey)
    print("====== Solved part 1 of the tree ======")
    # We get the solve order for the other side
    order = GetSolveOrder(monkey_uses, True)
    for monkey in order:
        SolveMonkeyTopDown(monkey, order)
    print("====== Solved part 2 of the tree ======")


def GetSolveOrder(uses_dic, human_side):
    output = []
    for k in uses_dic.keys():
        # For the already solved side
        if("humn" not in uses_dic[k] and not human_side):
            output.append(k)
        # For the human side
        if("humn" in uses_dic[k] and human_side):
            output.append(k)
    if(human_side):
        # We reverse it... so we solve from the top to the bottom.
        output.reverse()
        output.append("humn")
        output.pop(0) # We pop root , so it doesnt cause trouble
    #print("Solve order:", output)
    return output

def SolveMonkeyTopDown(key_name, order):
    global monkey_values
    global unknow_monkeys
    global recipe_dic

    # If it was solved already just return
    if(key_name in monkey_values.keys()):
        #print("Mono ya tiene un valor def en", key_name, "volviendo.")
        return
    cmn = order[order.index(key_name) -1 ] # Correct Monkey Name
    receta = recipe_dic[cmn]

    # Usamos a = b ALGO c
    a = TryGetMonkeyData(cmn)
    #print("Intentando resolver:", key_name)
    b = TryGetMonkeyData(receta[0])
    c = TryGetMonkeyData(receta[1])
    op = receta[2]
    #print("RECETA para", key_name, "=", receta)
    #print("A:",a,"B:",b,"C:",c)
    # Me fijo cual esta vacio
    if(b == ""):
        # We solve for b
        if(op == "+"):
            result = a - c
        if(op == "-"):
            result = a + c
        if(op == "*"):
            result = a / c
        if(op == "/"):
            result = a * c
        # We solve for c
    elif(c == ""):
        if(op == "+"):
            result = a - b
        if(op == "-"):
            #result = a + b
            result = b - a
        if(op == "*"):
            result = a / b
        if(op == "/"):
            #result = a * b
            result = b / a
    else:
        print("ERROR NOR B OR C ARE NULL ,SOLVE 2:", op)
        return     
    # We store the value on our dic
    monkey_values[key_name] = result
    #print("Se resolvio mono:", key_name, "=", result)


    


# Main code
p2 = False
BuildDic()
print("Resolviendo Monos..")
root_monkeys = GetRootMonkeys() # We use this for part 2
recipe_dic = unknow_monkeys.copy() # This is a dic we wont change, that contains the recipes we use in p2 to solve for values.

x = 0
while(TryGetMonkeyData("root") == ""):
    if(len(unknow_monkeys.keys()) -1 >= x):
        SolveMonkey(list(unknow_monkeys.keys())[x])
        x +=1
    else:
        x = 0
print("Valor de root:", monkey_values.get("root", "ERROR"))

print("===== PART 2 =====")
p2 = True
y = 3343167719435
input_m_name = "humn"
#print(BruteForceP2(y))

# I tried doing bruteforce for a bit... left the correct value in y if you wanna try it.
#while(BruteForceP2(y) == False):
    #y += 1

SolveP2(root_monkeys)
print("Monkey Value for humn is", monkey_values["humn"])