#Entrada
print("\nCalculadora em Python\nEscolha uma opção!!")

op = str(input("\n1 - Adição\n2 - Subtração\n3 - Multiplicação\n4 - Divisão\n"))

if(op == "1"):
    #Entrada
    num = float(input("\n\nDigite o primeiro:"))
    num1 = float(input("\n\nDigite o segundo:"))

    #Cálculos
    adicao = num + num1

    #Saída
    print("Resultado:",adicao)

elif(op == "2"):
    #Entrada
    num = float(input("\n\nDigite o primeiro:"))
    num1 = float(input("\n\nDigite o segundo:"))

    #Cálculos
    subtracao = num - num1

    #Saída
    print("Resultado:",subtracao)

elif(op == "3"):
    #Entrada
    num = float(input("\n\nDigite o primeiro:"))
    num1 = float(input("\n\nDigite o segundo:"))

    #Cálculos
    multiplicacao = num * num1

    #Saída
    print("Resultado:",multiplicacao)

elif(op == "4"):
    #Entrada
    num = float(input("\n\nDigite o primeiro:"))
    num1 = float(input("\n\nDigite o segundo:"))

    #Cálculos
    divisao = num / num1

    #Saída
    print("Resultado:",divisao)