#3. Crie um programa que solicite o código do produto e a quantidade, calcule e exiba o total do item, então solicite novamente código e quantidade até que o usuário digite 0 (zero). Então exiba o total da compra.

#Entrada
valor = 0
soma = 0
print("Mercado!")

#Processamento e saída
while True:
    code = int(input("\nDigite o código do produto:\nPara sair Digite \"0\"!\n"))
    if(code == 0):
        print("\n\nO total foi de R${:.2f}".format(soma))
        break
    else:
        valor = float(input("Digite o preço do produto de código {}:  ".format(code)))
        quantia = int(input("Digite a quantidade do produto:  "))
        soma = soma + (valor * quantia)