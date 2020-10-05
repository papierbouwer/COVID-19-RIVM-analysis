import numpy as np
import matplotlib.pyplot as plt

LOCAL = "./data/"

def main():
    firstDate = input("Give the first date as (YYYYMMDD): ")
    secondDate = input("Give the decond date as (YYYYMMDD): ")

    first, second = getDifference(date1, date2)

    plt.plot(first, label="Gevallen")
    plt.plot(first - second, label="Nieuwe gevallen")

    plt.xlabel("Aantal dagen na 1-1-2020")
    plt.ylabel("Aantal gevallen")

    plt.legend()

    plt.title("Totaal en nieuwe gevallen COVID-19 tussen " + secondDate + " en " + firstDate + "\nTotaal nieuwe gevallen " + str(np.sum(first - second)))
    plt.savefig("plots/" + firstDate + secondDate + "diff.png")

    plt.show()
    print(np.sum(first - second))

def getDifference(date1, date2):
    first  = readFile(LOCAL + date1 + "/cases.txt")
    second = readFile(LOCAL + date2 + "/cases.txt")

    # Make both arrays the same length by appending zero's.
    if len(first) != len(second):
        difference = len(first) - len(second)
        for i in range(difference):
            second.append(0)

    first = np.array(first)
    second = np.array(second)
    return first, second

def readFile(fileName):
    tempNumber = 0
    number = False

    returnArray = []

    with open(fileName) as readFile:
        for line in readFile:
            for letter in line:
                if '0' <= letter <= '9':
                    number = True
                    tempNumber *= 10
                    tempNumber += int(letter)
                else:
                    if number:
                        returnArray.append(tempNumber)
                    tempNumber = 0
                    number = False
    return returnArray

if __name__ == "__main__":
    main()
