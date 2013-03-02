# -*- coding: utf-8 -*-

# Account: Fornece a classe Account, que representa a conta de um usuário da rede 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-03-12

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()

import collections
Script = collections.namedtuple("Script", "name path extension run description")

def get_data_from_script(fullpath, ext):
	if ext == '.py':
		l = {}
		execfile(fullpath, {}, l)
		return (
			l['main'] if ('main' in l) else "Missing function 'main'.",
			str(l['description']()) if ('description' in l) else None
		)
	else:
		return ("Unknown extension: '%s'" % ext, None)

def search_scripts(module):
	import supermegazord, os, os.path
	scripts = {}
	d = os.path.dirname(supermegazord.__file__) + ("/scripts/%s/" % module)
	for f in [ f for f in os.listdir(d) if os.path.isfile(os.path.join(d,f)) ]:
		fullpath = os.path.join(d,f)
		name, ext = os.path.splitext(f)
		if name in scripts:
			raise Exception("More than one script with name '{0}' detected.".format(name))
		main, description = get_data_from_script(fullpath, ext)
		if not main or isinstance(main, str):
			raise Exception("Invalid script: '{0}': {1}".format(f, str(main)))
		if not description:
			description = "Missing description for '{0}': {1}".format(name,
				"Add a function 'description'" if (ext == '.py') else "Add a --description argument")
		scripts[name] = Script(name, fullpath, ext, main, description)
	return scripts
