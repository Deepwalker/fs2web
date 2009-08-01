# coding: utf-8

class superdict(dict):
    """Translates dictionary keys to instance attributes"""
    def __setattr__(self, k, v):
        dict.__setitem__(self, k, v)

    def __delattr__(self, k):
	dict.__delitem__(self, k)

    def __getattribute__(self, k):
	try: return dict.__getitem__(self, k)
	except KeyError: return dict.__getattribute__(self, k)

