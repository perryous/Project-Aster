# This is the initial script around which the rude calculator will be based
print("What do you want to do?")
print("1) Add")
print("2) Subtract")
print("3) Multiply")
print("4) Divide")

# Take input from the user 
# I am convinced this is where the error lies
choice = input("Enter choice: ")

if choice == 1:
   add1 = input("Enter your first number: ")
   add2 = input("Enter your second number: ")
   sum = add1+add2 
   print(sum)

elif choice == 2:
   sub1 = input("Enter your first number: ")
   sub2 = input("Enter your second number: ")
   loss = sub1+sub2
   print(loss)

elif choice == 3:
   tot1 = input("Enter your first number: ")
   tot2 = input("Enter your second number: ")
   total = tot1*tot2 
   print(total)
   
elif choice == 4:
   div1 = input("Enter your first number: ")
   div2 = input("Enter your second number: ")
   div = div1/div2 
   print(div)
   
else:
   print("Invalid input")
   
