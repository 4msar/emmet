#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Many parts of this code are borrowed from sublime-v8 project:
# https://github.com/akira-cn/sublime-v8

import sys
import os
import os.path
import platform
import codecs
from file import File

SUPPORTED_PLATFORMS = {
	"Darwin": "PyV8/osx",
	"Linux": "PyV8/linux",
	"Windows": "PyV8/win32"
}

def make_path(base, filename):
	return os.path.normpath(os.path.join(base, filename))

def js_log(message):
	print(message)

def create_env(files=[]):
	"""
	Creates environment required to successfully run Zen Coding JS core
	@param files: Additional files to load
	@return JS context to run Zen Coding actions
	"""
	base_path = os.path.abspath(os.path.dirname(__file__))
	platform_supported = SUPPORTED_PLATFORMS.get(platform.system())
	if not platform_supported:
		raise Exception, '''
			Sorry, the v8 engine for this platform are not built yet. 
			Maybe you need to build v8 follow the guide of lib/PyV8/README.md. 
		'''
	lib_path = platform_supported
	if not lib_path in sys.path:
		sys.path.append(os.path.join(base_path, lib_path))
		sys.path.append(base_path)

	import PyV8
	ctx = PyV8.JSContext()
	ctx.enter()

	core_files = ['zencoding.js', 'python-wrapper.js']
	files_to_load = [] + core_files + files

	for file_name in files_to_load:
		f = codecs.open(make_path(base_path, file_name), 'r', 'utf-8')
		# f = file(package_file(file_name))
		source = f.read()
		# sublime.status_message(source)
		ctx.eval(source)
		f.close()

	# expose some methods
	ctx.locals.log = js_log
	ctx.pyFile = File()

	return ctx
