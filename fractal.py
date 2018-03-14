import cmath
import sympy
import itertools
import numpy as np
from scipy import optimize

def makeFunc(order):
	
	fList = np.random.randint(-10, 10, order + 1)
	fpList = np.array([fList[o + 1] * (o + 1) for o in range(0, order)])
	
	return fList, fpList

def evalFunc(fList, x):

	return fList.dot(np.array([x ** o for o in range(0, len(fList))]))

def getSol(fList, fpList, x0):

	sol = optimize.newton(
		lambda x : fList.dot(np.array([x ** o for o in range(0, len(fList))])),
		x0,
		fprime = lambda x : fpList.dot(np.array([x ** o for o in range(0, len(fpList))])))

	return sol

def symbolicSol(fList):

	xSym = sympy.symbos('z')

	string = ''

	for o in range(0, len(fList)):

		if fList[o] > 0 and o != 0:

			string = string + ' + ' + str(fList[o]) + '*z**' + str(o)

		elif fList[o] < 0:

			string = string + ' - ' + str(fList[o])[1:] + '*z**' + str(o)

		else:

			pass

	return string

f, fp = makeFunc(4)
print(f)
print(fp)

width = 10
height = 10
resolution = 10
reRange = np.linspace(-width / 2, width / 2, num = resolution, endpoint = True)
imRange = np.linspace(-height / 2, height / 2, num = resolution, endpoint = True)

print(symbolicSol(f))

for (a, b) in itertools.product(reRange, imRange):

	x0 = a + 1j * b
	#print(x0)
	sol = getSol(f, fp, x0)

	print(cmath.polar(sol))