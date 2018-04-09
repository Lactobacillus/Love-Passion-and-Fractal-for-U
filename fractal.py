import cmath
import sympy
import timeit
import itertools
import numpy as np
import multiprocessing
from scipy import optimize
import matplotlib.pyplot as plt
import matplotlib.image as Image
from joblib import Parallel, delayed
from sympy.parsing.sympy_parser import parse_expr

np.seterr(all = 'ignore')
np.warnings.filterwarnings('ignore')

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
		fprime = lambda x : fpList.dot(np.array([x ** o for o in range(0, len(fpList))])),
		tol = 1.0e-5,
		maxiter = 100)

	return sol

def symbolicSol(fList):

	z = sympy.symbols('z', complex = True)

	string = ''

	for o in range(0, len(fList)):

		if fList[o] > 0:

			string = string + ' + ' + str(fList[o]) + '*z**' + str(o)

		elif fList[o] < 0:

			string = string + ' - ' + str(fList[o])[1:] + '*z**' + str(o)

		else:

			continue

	expr = parse_expr(string)
	sol = sympy.solve(sympy.Eq(expr, 0), domain = sympy.S.Complexes)

	return [s.evalf() for s in sol]

def assignIdx(trueSol, sol):

	#radius, angle = cmath.polar(sol)
	error = [(sympy.re(t) - sol.real)**2 + (sympy.im(t) - sol.imag)**2 for t in trueSol]

	if min(error) < 0.001:

		return error.index(min(error))

	else:

		return len(error)

def getPixel(f, fp, trueSol, a, b):

	x0 = a + 1j * b
	sol = getSol(f, fp, x0)

	return (a, b, assignIdx(trueSol, sol))

def main():

	width = 10
	height = 10
	order = 3
	resolution = 5000
	numProcess = multiprocessing.cpu_count()
	
	reRange = np.linspace(-width / 2, width / 2, num = resolution, endpoint = True)
	imRange = np.linspace(-height / 2, height / 2, num = resolution, endpoint = True)
	color = {'R' : np.random.rand(order), 'G' : np.random.rand(order), 'B' : np.random.rand(order)}
	image = np.zeros((resolution, resolution, 3))

	f, fp = makeFunc(order)

	#f = np.array([-1, 0, 0, 1])
	#fp = np.array([0, 0, 3])

	trueSol = symbolicSol(f)

	print('Start : ', f, fp)
	print(trueSol)

	timeNow = timeit.default_timer()
	result = Parallel(n_jobs = numProcess)(delayed(getPixel)(f, fp, trueSol, a, b) for (a, b) in itertools.product(reRange, imRange))
	print('Time : ', timeit.default_timer() - timeNow)

	for (i, j) in itertools.product([t for t in range(0, resolution)], [t for t in range(0, resolution)]):

		image[i, j, 0] = color['R'][result[i * resolution + j][2]]
		image[i, j, 1] = color['G'][result[i * resolution + j][2]]
		image[i, j, 2] = color['B'][result[i * resolution + j][2]]

	#for (x, y, c) in result:

		#image[x, y, 0] = color['R'][c]
		#image[x, y, 1] = color['G'][c]
		#image[x, y, 2] = color['B'][c]
		#print(x, y, c)
	Image.imsave(str(f) + '.png', image)
	#plt.imshow(image, interpolation = None)
	#plt.scatter(X, Y, c = C, marker = 'o', alpha = 0.4)
	#plt.show()

if __name__ == '__main__':

	for i in range(50):

		main()