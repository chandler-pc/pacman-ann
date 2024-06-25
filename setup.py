from setuptools import setup, find_packages

# Leer las dependencias desde el archivo requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='PACMAN',
    version='1.0.0',
    description='A Pac-Man game with genetic algorithm for training neural networks',
    author='Tu Nombre',
    author_email='tu_email@example.com',
    url='https://github.com/chandler-pc/pacman-ann',
    packages=find_packages(include=['app', 'app.*', 'scripts', 'scripts.*']),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'run-pacman=scripts.run:main',
            'train-pacman=scripts.train:main',
            'test-pacman=scripts.test:main'
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)