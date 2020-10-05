import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from difference import getDifference
import datetime

def main():
    plt.rcParams.update({'font.family': 'serif', 'font.size': 16,
    'axes.labelsize': 18,'axes.titlesize': 20, 'figure.titlesize' : 22})
    plt.rcParams.update({"text.usetex": True})

    dates = getDates()
    days, cases = getDifferenceData(dates)

    popt, pcov = curve_fit(exp, days, cases)
    perr = np.sqrt(np.diag(pcov))

    plt.plot(days, cases, label="Nieuwe gevallen")

    xLinHigh = np.linspace(np.min(days), np.max(days), 10*len(days))

    plt.plot(xLinHigh, exp(xLinHigh, *popt), label="$f(t)\\propto \\exp\\left({:.4f}t\\right)$".format(popt[1]))

    plt.ylim(0, 1.1*np.max(cases))

    plt.xlabel("Dagen sinds " + datetime.datetime.today().strftime("%Y-%m-%d"))
    plt.ylabel("Nieuwe gevallen")

    plt.legend()
    plt.tight_layout()

    plt.savefig("plots/" + dates[-1] + "expFit.png")

    plt.show()

def getDates():
    dates = [x[0][5:len(x[0])] for x in os.walk("data")]
    dates = [date for date in dates if len(date) > 0]
    return sorted(dates)

def getDifferenceData(dates):
    cases = []
    xAxis = []

    today = datetime.datetime.today()

    for i in range(len(dates) - 1):
        dateChecked = datetime.datetime.strptime(dates[i], "%Y%m%d")
        xAxis.append((dateChecked - today).days)

        first, second = getDifference(dates[i+1], dates[i])
        cases.append(np.abs(np.sum(first - second)))
    return np.array(xAxis), np.array(cases)



def exp(x, a, b):
    return a * np.exp(b*x)

if __name__ == "__main__":
    main()
