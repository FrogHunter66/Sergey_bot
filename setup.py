from setuptools import setup, find_packages
from setuptools.dist import Distribution


class BinaryDistribution(Distribution):
    def has_ext_modules(foo):
        return True


def parse_requirements(file_path):
    with open(file_path, 'r') as f:
        lines = f.read().splitlines()
        lines = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        return lines


setup(
    name='Sergey_bot',
    version='0.1',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    entry_points={
        'console_scripts': [
            'Sergey_bot = bot:main'
        ]
    },
    distclass=BinaryDistribution,
)