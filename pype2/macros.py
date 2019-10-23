from pype2.fargs import embedded_pype,concat,l,append,dissoc,d,merge,_

##########
# MACROS #
##########

def ep(*fArgs):

    return [embedded_pype,*fArgs]


def iff(condition,fArg):

    return {condition:fArg,
            'else':_}


def ift(condition,fArg):

    return {condition:fArg,
            'else':False}
    

def ifp(*fArgs):
    
    return {_:ep(*fArgs),
            'else':_}


def iffp(*fArgs):
    
    return {_:ep(*fArgs),
            'else':False}


def db(*fArgs):

    return [d,*fArgs]


def dbp(*fArgs):

    return [d,fArgs[0],_p(*fArgs[1:])]


def select(*fArgs):

    return {fArg:_[fArg] for fArg in fArgs}


def a(*fArgs):

    return [assoc,*fArgs]

def ap(*fArgs):

    return [assoc,fArgs[0],ep(*fArgs[1:])]


def m(fArg):

    return [merge,fArg]


def d(*fArgs):

    return [dissoc,*fArgs]


def tup(*fArgs):

    return [l,*fArgs]


def app(*fArgs):

    return [append,*fArgs]


def c(*fArgs):

    return [concat,*fArgs]

