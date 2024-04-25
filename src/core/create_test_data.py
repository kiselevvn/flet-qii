import csv
from random import randrange

GROUPS = (0, 1)


def generate_csv(filename="data.csv", count=500):

    def get_group(index, count_all):
        if index < (count_all / 2):
            return GROUPS[1]
        return GROUPS[0]

    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['group', 'A', 'B', 'C', 'D', 'E', 'K', 'V']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for num in range(count):
            g = get_group(num, count)
            A = randrange(40,50) if g == 0 else randrange(60,70)
            B = randrange(36,70)
            C = randrange(20,68)
            D = randrange(40,50) if g == 0 else randrange(50,55)
            E = randrange(10,40)
            K = randrange(60,100)
            V = randrange(10,30) if g == 0 else randrange(32,50)

            writer.writerow({'group': g, 'A': A, 'B': B, 'C': C, 'D': D, 'E': E, 'K': K, 'V': V})

if __name__ == "__main__":
    default_name = 'data10.csv'
    default_count = 10
    generate_csv(default_name, default_count)
