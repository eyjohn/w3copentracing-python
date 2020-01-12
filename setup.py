from setuptools import setup

setup(name='w3copentracing',
      version='0.1.5',
      description='A partial implementation of an OpenTracing tracer with W3C Trace Context compliance.',
      url='https://github.com/eyjohn/w3copentracing-python',
      author='Evgeny Yakimov',
      author_email='evgeny@evdev.me',
      license='Apache License Version 2.0',
      packages=['w3copentracing'],
      install_requires=['opentracing>=2.3.0'],
      zip_safe=False)
