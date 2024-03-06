from setuptools import setup, find_packages

__version__ = '1.0.1'

if __name__ == "__main__":
    setup(
        name='gemmini',
        version=__version__,
        description='Python package for constructing and handling geometric objects',
        author='Yankos',
        author_email='byanko55@gmail.com',
        url='https://github.com/byanko55/gemmini',
        install_requires=['numpy', 'matplotlib', 'scipy'],
        packages=find_packages(),
        keywords=['geometry', 'drawing 2D/3D graphic'],
        python_requires='>=3.7',
    )
