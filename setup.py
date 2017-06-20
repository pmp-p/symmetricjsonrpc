#!/usr/bin/env python
 
from distutils.core import setup
 
setup(name='symmetricjsonrpc',
	version='0.1.0',
	description='A more beautiful JSON-RPC implemenation in python',
	author='niligulmohar',
	url='http://github.com/niligulmohar/python-symmetric-jsonrpc',
	packages=['symmetricjsonrpc'],
	py_modules=['dispatcher','json','rpc','wrappers'],
	long_description="",
	license="LGPL"
)
