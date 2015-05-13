from setuptools import setup
import py2exe

setup(
    name='pieEngine',
    version='0.1.1',
    packages=['pie'],
    instal_requires=['pygame', 'numpy'],
    windows=['pie/demo/pie_bg_parallax.py'],
    options={
            "py2exe":{
                    "unbuffered": True,
                    "optimize": 2,
                    "bundle_files": 1
            }
    },
    url='https://github.com/adoc/pieEngine',
    license='MIT',
    author='Nick Long',
    author_email='adoc@code.webmob.net',
    description='Game engine for Pygame.'
)
