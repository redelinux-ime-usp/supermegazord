# -*- coding: utf-8 -*-

# Group: Fornece a classe Group, que representa a um grupo da rede 
# Autor: Henrique Gemignani Passos Lima (henriquelima)
# Escrito em: 2012-11-29

if __name__ == "__main__":
	print "Esse módulo não deve ser executado diretamente."
	quit()
	
cache = {}

class Group:
	def __init__(self, gid, name, members):
		self.gid = int(gid)
		self.name = name
		self.members = members
		if gid not in cache:
			cache[gid] = self
		
	def __repr__(self):
		return 'Group({0},"{1}",{2})'.format(self.gid, self.name, self.members)
		
	def __str__(self):
		return "Group[{1}; gid {0}]".format(self.gid, self.name)

def from_ldap(ldapdata):
	try:
		if 'memberUid' in ldapdata:
			members = ldapdata['memberUid']
		else:
			members = []
		return Group(ldapdata['gidNumber'][0], ldapdata['cn'][0], members)
	except:
		return None

def from_gid(gid):
	if gid in cache: return cache[gid]
	import ldapwrap
	return from_ldap(ldapwrap.find_group_by_gid(gid))
