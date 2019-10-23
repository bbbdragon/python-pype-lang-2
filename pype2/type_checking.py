from collections import defaultdict
import numpy as np
'''
These are just functions to check types of objects.
'''
def is_tuple(x): return isinstance(x,tuple)
def is_dict(x): return isinstance(x,dict)
is_dict=lambda x: isinstance(x,dict)
is_ddict=lambda x: isinstance(x,defaultdict)
is_list=lambda x: isinstance(x,list)
is_mapping=lambda x: isinstance(x,dict)
is_bool=lambda x: isinstance(x,bool)
is_object=lambda x: isinstance(x,object)
is_string=lambda x: isinstance(x,str)
is_set=lambda x: isinstance(x,set)
is_int=lambda x: isinstance(x,int)
is_slice=lambda x: isinstance(x,slice)
is_iterable=lambda x: isinstance(x,Iterable)
is_mapping=lambda x: isinstance(x,Mapping)
is_hashable=lambda x: isinstance(x,Hashable)
is_ndarray=lambda x: isinstance(x,np.ndarray)
is_sequence=lambda x: isinstance(x,Sequence) or is_ndarray(x)
is_container=lambda x: isinstance(x,Container)
is_float=lambda x: isinstance(x,float)
is_integer=lambda x: isinstance(x,int)
is_callable=lambda x: callable(x)
key=lambda x: tup[0]
val=lambda x: tup[1]
slc=lambda ls,start,stop: ls[start:stop]

