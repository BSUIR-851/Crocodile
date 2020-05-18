from distutils.core import setup
import py2exe

setup(
	console=['clientTCP.py'],
	options={
		'py2exe': {
			'packages': ['pyqt5']
		}
	}
)