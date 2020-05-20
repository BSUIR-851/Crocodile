import os 

def getWords(filepath):
	words = [
		'солнце',
		'карандаш',
		'компьютер',
		'луна',
		'звезда',
		'снег',
		'вода'
	]
	
	if os.path.exists(filepath):
		f = open(filepath, 'r')
		words = f.read().split('\n')
		f.close()
	return words