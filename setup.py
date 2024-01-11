from setuptools import setup, find_packages

__version__ = "0.0.2"

if __name__ == "__main__":
    setup(
        name='gemmini',
        version=__version__,
        description='Python package for constructing and handling geometric objects',
        author='Yankos',
        author_email='byanko55@gmail.com',
        url='https://github.com/byanko55/gemmini',
        install_requires=['numpy', 'matplotlib'],
        packages=find_packages(exclude=[]),
        keywords=['geometry', 'drawing 2D/3D graphic'],
        python_requires='>=3.6',
    )
