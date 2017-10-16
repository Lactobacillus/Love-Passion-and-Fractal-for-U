import random
from sympy import *
import multiprocessing
from joblib import Parallel, delayed
from bokeh.palettes import Category20
from bokeh.plotting import figure, output_file, show

def makeTerm():

	option = random.randint(0, 1) % 2

	if option == 0:

		# real
		a = '{0:+d}'.format(random.randint(-9, 9))
		term = '(z' + a + ')'

	elif option == 1:

		# complex
		a = '{0:+d}'.format(random.randint(-9, 9))
		b = random.randint(-9, 9)
		c = -b
		b = '{0:+d}'.format(b)
		c = '{0:+d}'.format(c)
		term = '(z' + a + b + '*I)*(z' + a + c + '*I)'

	# not use now
	elif option == 2:

		# cos
		a = '{0:+d}'.format(random.randint(-3, 3))
		b = '{0:+d}'.format(random.randint(1, 3))
		term = '(z' + a + '*cos(' + b + '*z))'
	
	# not use now
	elif option == 3:

		# sin
		a = '{0:+d}'.format(random.randint(-3, 3))
		b = '{0:+d}'.format(random.randint(1, 3))
		term = '(z' + a + '*sin(' + b + '*z))'
	
	# not use now
	elif option == 4:

		# exp
		a = '{0:+d}'.format(random.randint(-9, 0))
		b = '{0:+d}'.format(random.randint(1, 3))
		c = '{0:+d}'.format(random.randint(1, 3))
		term = '(z' + a + '*exp(' + b + '*z**' + c + '))'

	return term

def makeFunc():

	func = ''

	for i in range(0, random.randint(3,5)):

		func = func + makeTerm() + '*'

	return sympify(func[:-1])

def newtonRaphson(f, df, init, iterN):





	# lambda 로 바꿔서 numpy 적용 하면 빠르게 될듯


	x = Symbol('x')

	#print(f)
	#print(df)

	#print(solve(f))

	x0 = f.evalf(subs = {x : init})
	xi = x0 - f.evalf(subs = {x : x0}) / df.evalf(subs = {x : x0})

	for i in range(0, iterN):

		xj = simplify(xi - f.evalf(subs = {x : xi}) / df.evalf(subs = {x : xi}))
		xi = xj
	
	print((init, xj))

	return xj

def calcLatice(f, df, width, height, initR, initI):

	result = dict()
	x = Symbol('x')

	initR = abs(initR)
	initI = abs(initI)

	dR = float(2 * initR) / width
	dI = float(2 * initI) / height

	numProcess = multiprocessing.cpu_count()
	initC = [(-initR + dR * i) + (-initI + dI * j) * I for i in range(0, width + 1) for j in range(0, height + 1)]
	tempResult = Parallel(n_jobs = numProcess)(delayed(newtonRaphson)(f, df, init, 100) for init in initC)

	for idx, value in enumerate(initC):

		result[(re(value), im(value))] = tempResult[idx]

	#for a in [-initR + dR * i for i in range(0, width + 1)]:
	#
	#	for b in [-initI + dI * i for i in range(0, height + 1)]:
	#
	#		print((a,b))
	#		result[(a,b)] = newtonRaphson(f, df, a + b*I, 100)

	return result

def compare(value, solutions):

	a = re(value)
	b = im(value)

	comp = [(re(c) - a)**2 + (im(c) - b)**2 for c in solutions]
	
	return comp.index(min(comp))

def draw(result, solutions):

	colors = Category20[20]
	output_file('result.html')
	picture = figure(plot_width = 500, plot_height = 500)

	x = [list() for i in range(len(solutions))]
	y = [list() for i in range(len(solutions))]

	for key, value in result.items():

		color = compare(value, solutions)
		x[color].append(float(key[0]))
		y[color].append(float(key[1]))

	for i in range(len(solutions)):

		picture.square(x[i], y[i], size = 10, color = colors[i], alpha = 1.0)

	show(picture)

def main():

	
	z = Symbol('z')
	f = makeFunc()

	#print(f)
	#print(solveset(Eq(f, 0), z))

	x = Symbol('x')
	fx = x**3 + 1
	dfx = diff(fx, x)
	iv = I

	print(solve(fx))

	#print(newtonRaphson(fx, dfx, iv, 100))
	result = calcLatice(fx, dfx, 30, 30, 30, 30)
	draw(result, solve(fx))

if __name__ == '__main__':

	main()



#output_file('result.html')

#p = figure(plot_width = 400, plot_height = 400)

# add a square renderer with a size, color, and alpha
#p.square([1, 2, 3, 4, 5], [1, 1, 1, 1, 1], size = 40, color = 'olive', alpha = 0.5)
#p.square([1, 2, 3, 4, 5], [2, 2, 2, 2, 2], size = 40, color = 'navy', alpha = 0.5)
#p.square([1, 2, 3, 4, 5], [3, 3, 3, 3, 3], size = 40, color = 'firebrick', alpha = 0.5)
#p.square([1, 2, 3, 4, 5], [4, 4, 4, 4, 4], size = 40, color = 'green', alpha = 0.5)
#p.square([1, 2, 3, 4, 5], [5, 5, 5, 5, 5], size = 40, color = 'yellow', alpha = 0.5)

# show the results
#show(p)