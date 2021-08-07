cm = int(input('Enter your height in cm: '))

inches = cm / 2.54
ft = inches / 12
inches = inches % 12

print('Your height is',int(ft),'feet and',inches,'inches.')

