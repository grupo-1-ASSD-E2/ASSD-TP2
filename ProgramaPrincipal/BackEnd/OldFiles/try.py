file1 = open('violin.txt', 'r')




lines = file1.readlines()

for line in lines:
    print(line.strip() + ',')



file1.close()