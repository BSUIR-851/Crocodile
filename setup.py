from distutils.core import setup
import py2exe

setup(
	console=['clientController.py'],
	options={
		'py2exe': {
			'packages': ['pyqt5']
		}
	}
)