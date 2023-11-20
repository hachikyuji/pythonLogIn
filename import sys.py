

'''
class UpSaWork:
    def __init__(self, empName, dailyRate, bilangNgAraw, bale):
        self.empName = empName
        self.dlyRate = dailyRate
        self.dayCount = bilangNgAraw
        self.bale = bale

    def sueldo(self):
        netpay = self.dlyRate * self.dayCount
        netpay -= self.bale
        print(f'Employee Name: {self.empName} \nNet pay: {netpay}')


taol = UpSaWork('John', 1000, 3, 100)

taol.sueldo()


class Barrel:
    def __init__(self, taas=1, diaHalf=1):
        self.height = taas
        self.middleRadius = diaHalf

    def kabuuangSukat(self):
        R = pow(self.middleRadius, 2)
        r = pow(self.middleRadius, 2)
        vol = R + 2 * r
        vol2 = (3.14 * self.height)
        volume = vol * vol2
        volume /= 3
        print(volume)

    
c = Barrel(5, 6)

c.kabuuangSukat()
'''

'''
AT 4
class Sphere:
    def __init__(self, radius):
        self.radius = radius

    def volume(self):
        volume = 4/3 * 3.14*pow(self.radius, 3)
        return f'{volume} cm^3'
    
s = Sphere(3)

print(s.volume())
'''

'''
sentence = 'Print only the words that start with s in this sentence'

# Split the sentence into words
words = sentence.split()

# Iterate through the words and print those that start with 's'
for word in words:
    if word.startswith('s') or word.startswith('S'):
        print(word)


for num in range(0, 11, 2):
    print(num)
    
st = 'Print every word in this sentence that has an even number of letters'

wsplit = st.split()

for w in wsplit:
    if len(w) %2 == 0:
        print(w)

  
for num in range(1, 101):
    if num % 3 == 0 and num % 5 == 0:
        print("FizzBuzz")
    elif num % 3 == 0:
        print("Fizz")
    elif num % 5 == 0:
        print("Buzz")
    else:
        print(num)
        


import random

def guess_game():
    secret_number = random.randint(1, 100)
    guess = 0
    prev_guess = 0
    guess_count = 0

    while True:
        try:
            guess = int(input("Enter your guess (between 1 and 100): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        if guess < 1 or guess > 100:
            print("OUT OF BOUNDS")
            continue

        guess_count += 1

        if guess_count == 1:
            if abs(guess - secret_number) <= 10:
                print("WARM!")
            else:
                print("COLD!")
        else:
            if abs(guess - secret_number) < abs(prev_guess - secret_number):
                print("WARMER!")
            else:
                print("COLDER!")

        if guess == secret_number:
            print(f"Congratulations! You guessed the number in {guess_count} attempts.")
            break

        prev_guess = guess

guess_game()
    
'''

'''
d1 = {'simple_key': 'hello'}
result_d1 = d1['simple_key']
print(result_d1)

d2 = {'k1': {'k2': 'hello'}}
result_d2 = d2['k1']['k2']
print(result_d2)

d3 = {'k1': [{'nest_key': {'this is deep': ['hello']}}]}
result_d3 = d3['k1'][0]['nest_key']['this is deep'][0]
print(result_d3)

d4 = {'k1': [1, 2, {'k2': {'this is tricky': {'tough': [1, 2, ['hello']]}}}]}
result_d4 = d4['k1'][2]['k2']['this is tricky']['tough'][2][0]
print(result_d4)

my_list = [1, 2, 2, 33, 4, 4, 11, 22, 3, 3, 2]

unique_set = set(my_list)

unique_list = list(unique_set)

print(unique_list)

print(2 > 3)

print(3 <= 2)

print (3 == 2.0)

print (3.0 == 3)

print (4**0.5 != 2)

one = [1, 2, [3, 4]]
two = [1, 2, {'k1': 4}]

print (one[2][0] >= two[2]['k1'])

'''