print("\nAumento de Salário!!")

#Entrada
salario = float(input("\n\nDigite o valor do salário:"))
porcentagem = float(input("\n\nDigite o número da porcentagem:"))

#Cálculos
valorPorcentagem = porcentagem / 100
aumento = salario * valorPorcentagem
newSalario = aumento + salario

print("\n\nNovo salário:",newSalario,"\n")