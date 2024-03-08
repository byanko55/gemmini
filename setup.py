from setuptools import setup, find_packages

__version__ = '1.0.2'

with open('README.md', encoding='utf-8') as f:
    readme = f.read()

if __name__ == "__main__":
    setup(
        name='gemmini',
        version=__version__,
        long_description=readme,
        long_description_content_type='text/markdown',
        description='Python package for constructing and handling geometric objects',
        author='Yankos',
        author_email='byanko55@gmail.com',
        url='https://github.com/byanko55/gemmini',
        install_requires=['numpy', 'matplotlib', 'scipy'],
        packages=find_packages(),
        keywords=['geometry', 'drawing 2D/3D graphic'],
        python_requires='>=3.7',
    )
