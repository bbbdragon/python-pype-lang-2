import numpy as np
from pype2 import pypeify,p,_
from pype2.helpers import zip_dct,dct_keys,dct_values
from pype2 import ep
from numba import njit,jit

'''
This is a series of operations for numpy.  Will document later.
'''

def agg_sum(m):

    indices=m[:,0].argsort()
    m[:,0]=m[indices,0]
    m[:,1:]=m[indices,1:]
    uniqueKeys=np.unique(m[:,0],return_counts=True)
    cumSum=np.cumsum(uniqueKeys[1])[:-1]
    splitValues=np.split(m[:,1:],cumSum)
    sm=np.array([np.sum(l,axis=0) for l in splitValues])
    
    return sm,uniqueKeys[0],uniqueKeys[1]


def build_mat(y,X):

    m=np.zeros([y.shape[0],X.shape[1]+1])
    m[:,0]=y
    m[:,1:]=X

    return m


@njit
def shuffle(m):

    np.random.shuffle(m)

    return m


def aggregate_by_first_column(m):

    indices=m[:,0].argsort()
    m[:,0]=m[indices,0]
    m[:,1]=m[indices,1]
    uniqueKeys=np.unique(m[:,0],return_counts=True)
    cumSum=np.cumsum(uniqueKeys[1])[:-1]
    splitValues=np.split(m[:,1],cumSum)

    return splitValues,uniqueKeys[0],uniqueKeys[1]


def aggregate_by_key(m,padVal=0,pad=True):
    '''
    This is a helper which takes an array with two columns.  It is the numpy
    equivalent of grouping represented by tup_ls_dct in pype.
    The first column is the key, and the second column is the value.  We 
    perform the following operations on this:
    1) Sort the keys of m, getting their indices.
    2) Reorder the keys and values of m accordingly.
    3) Find the unique keys and their counts, stored in uniqueKeys[1].
    4) The np.split function takes an array, and splits it according to
       the counts of the unique elements.  So, take the first x elements,
       put it in one part of the list, then take the next y elements, append
       it to the list, etc.
    5) In the resulting list of arrays, we find the maximum length.
    6) We pad these arrays with zeros if they're shorter than the maximum
       length.
    7) Then, we convert this into a matrix, whose i-th row represents the
       i-th key, and whose j-th column represents the j-th value with that
       key.  
    8) We return the matrix and the unique keys.
    We do this rather than json-style grouping for performance reasons, as 
    many people have complained about using pure json-style aggregation.
    Thanks to: https://stackoverflow.com/questions/38013778/is-there-any-numpy-group-by-function
    '''
    indices=m[:,0].argsort()
    m[:,0]=m[indices,0]
    m[:,1]=m[indices,1]
    uniqueKeys=np.unique(m[:,0],return_counts=True)
    splitValues=np.split(m[:, 1], 
                         np.cumsum(uniqueKeys[1])[:-1])

    if pad:

        maxLen=np.max([a.shape[0] for a in splitValues])
        aggregatedValues=[np.lib.pad(a,
                                     (0,maxLen-a.shape[0]),
                                     'constant',
                                     constant_values=(padVal,padVal))\
                          for a in splitValues]
        aggregatedValues=np.array(aggregatedValues)

    else: 
        
        aggregatedValues=splitValues

    return aggregatedValues,uniqueKeys[0],uniqueKeys[1]


def sorted_aggregate_by_key(m,padVal=0,pad=True):

    aggregatedValues,uniqueKeys,uniqueCounts=aggregate_by_key(m,padVal,pad)

    aggregatedValues.sort(axis=1)

    return aggregatedValues,uniqueKeys,uniqueCounts


def aggregate_jsons_by_key(ls,key):

    uniqueVals=np.unique([js[key] for js in ls])
    indexToKeyMap={k:i for (i,k) in enumerate(uniqueVals)}
    m=np.array([(indexToKeyMap(js[key]),i) for (i,js) in enumerate(ls)])
    aggregatedValues,keys,uniqueKeys=aggregate_by_key(m,False)

    return {k:[ls[index] for index in l] \
            for (k,l) in zip(uniqueVals,aggregatedValues)}
    

def np_int_array(x):

    return np.array(x,dtype=np.int32)


def sum_by_row(x):

    return np.sum(x,axis=1)


def sum_by_column(x):

    return np.sum(x,axis=0)


def vector_copy_matrix(shape,vector):

    z=np.zeros(shape)
    z[:,:]=vector

    return z


def trans(m):

    return m.T


def square_ones_tri(rows,k=0):

    return np.triu(np.ones([rows,rows]),k)


def zero_below(x,thresh=0):

    x[x < thresh]=0

    return x


def zero_above(x,thresh=0):

    x[x > thresh]=0

    return x


def cap_at(x,thresh=0):

    x[x > thresh]=thresh

    return x
    

# This is a hack for pype's lack of support of complex indexes.
@njit
def np_rows_from(a,colStart=0):

    return a[:,colStart:]


@njit
def np_rows_to(a,colEnd):

    return a[:,:colEnd]


def num_rows(a):

    return a.shape[0]


def num_cols(a):

    return a.shape[1]


def nonzero_indices(m):

    lastCol=m.shape[1]-1
    colStart=(m[0,:]!=0).argmax(axis=0)
    rowEnd=(m[:,lastCol]!=0).argmax(axis=0)
    rowEnd+=np.count_nonzero(m[rowEnd:,lastCol]>0)

    return rowEnd,colStart


def add_upper_right_corner(m1,m2):

    m1Rows=m1.shape[0]
    m2Rows=m2.shape[0]
    m1Cols=m1.shape[1]
    m2Cols=m2.shape[1]
    m1[:m2Rows,m1Cols-m2Cols:]+=m2

    return m1


def off_diagonal(ln,offset=0):

    numOnes=ln-offset
    ones=np.ones(numOnes)

    return np.diag(ones,offset)


def off_diagonal_fill(a,offset=0):

    return np.diag(a,offset)


def ones_filter(ln,offset=1):

    return square_ones_tri(ln) - square_ones_tri(ln,offset)


def log_with_zero(m):

    return zero_below(np.log(m))


def val_sum(dct):

    return np.sum([v for (k,v) in dct.items()])


def by_indices(a,tuples):

    return [a[tup] for tup in tuples]


from pype.helpers import dct_values

def array_from_vals(dct):

    return np.array(dct_values(dct))


def row_sum(array):

    return np.sum(array,axis=1)


@njit
def col_sum(array):

    return np.sum(array,axis=0)


def divide_by_row_sum(array):

    array+=L

    # print(f'{array} is array')
    # print(f'{row_sum(array)} is row_sum')
    # print(f'{(array.T/row_sum(array)).T} is divide by row_sum')

    return (array.T/row_sum(array)).T


def unique_in_order(a):

    vals,indices=np.unique(a,return_index=True)
    
    return a[np.sort(indices)]


def unique_row_elements(array):

    return np.unique(array,axis=1)





def count_nonzeros_in_rows(array):

    return np.count_nonzero(array,axis=1)



def enumerate_array(array,rev=False):

    m=np.zeros([array.shape[0],2])
    rng=np.arange(m.shape[0],dtype=np.int32)
    rangeColumn,arrayColumn=(1,0) if rev else (0,1)
    m[:,rangeColumn]=rng
    m[:,arrayColumn]=array

    return m


def enumerate_array_rev(array):

    m=np.zeros([array.shape[0],2],dtype=np.int32)

    m[:,1]=np.arange(m.shape[0])
    m[:,0]=array

    return m


def unique_indices(array):

    array.sort()

    return [(array == i).nonzero()[0][0] for i in np.unique(array)]


def sort_by_row(array):

    array.sort(axis=1)

    return array


def unique_counts(array):

    uniqueElements,counts=np.unique(array,return_counts=True)

    return counts


def unique_row_counts(array,padVal=0,pad=True):

    counts=[unique_counts(row) for row in array]

    '''
    if any([c.shape[0] < array.shape[1] for c in counts]):

        print(f'{array} is array')
        print(f'{counts} is counts') 
        print('='*30)
    '''

    return counts
    
     

def unique_sorted_counts(array):

    array.sort()

    return unique_counts(array)


def sort_array(array):

    array.sort()

    return array


def from_mat(mat,i,j):
    '''
    Placeholder for when we can fix the indexing with numpy arrays.
    '''
    return mat[i,j]


@pypeify()
def prob_vec(a):
    
    return p( a,
              _+L,
              _/np.sum)


@pypeify()
def count_prob_array(ls,discount=0):

    return p( ls,
              np.array,
              unique_counts,
              _-discount,
              _+L,
              _/np.sum)


from pype2 import _0

@pypeify()
def weighted_count_prob_array(ls=[[1,0.5],[2,0.3]],
                              discount=0):

    return p( ls,
              np.array,
              aggregate_by_key,
              _0,
              row_sum,
              _-discount,
              _+L,
              _/np.sum,
           )


@pypeify()
def weighted_count_prob_diag(ls=[[1,0.5],[2,0.3]],
                             discount=0):

    ((weighted_count_prob_array,_,discount),
     np.diag)


def count_prob_diag(ls,discount=0):

    return np.diag(count_prob_array(ls,discount))


def row_median(m,pad=False):

    vals,uniqueKeys,uniqueCounts=aggregate_by_key(m,0,False)

    return vals


def filter_array(m,threshold=0):
    '''
    This sets anything above the threshold to 1.
    '''
    m=np.array(m)

    np.place(m,m>threshold,1)

    return m


def softplus(x):

    return np.log(1+np.exp(-np.abs(x))) + np.maximum(x,0)



@pypeify()
def prob_dct(valDct):

    return p( valDct,
              (zip_dct,dct_keys,
                       ep(dct_values,
                          np.array,
                          prob_vec,
                         )),
            )  


def median_std(a):

    a=np.array(a)
    a=np.abs(a - np.median(a))

    return np.median(a)
    
    
def np_max(a):

    return np.nan_to_num(np.max(a))


def np_median(a):

    return np.nan_to_num(np.median(a))


def np_mean(a):

    return np.nan_to_num(np.mean(a))


def np_std(a):

    return np.nan_to_num(np.std(a))


def np_log(a):

    return np.nan_to_num(np.log(a))


def rows_div(rows,a):

    a=a.flatten()

    return rows/a

L=1e-100


# def to_1d(a):

    
def to_np_int(a):

    return a.astype(np.int32)


def col_argmax(a):

    return np.argmax(a,axis=0)


def row_argmax(a):

    return np.argmax(a,axis=1)




@njit
def k_fold_filter(m,filterBegin,filterEnd):

    # print(f'{filterBegin} is filterBegin')
    # print(f'{filterEnd} is filterEnd')
    # print(f'{m} is m')

    testing=m[filterBegin:filterEnd,:]
    stackBegin=m[:filterBegin,:]
    stackEnd=m[filterEnd:,:]

    if stackBegin.shape[0] > 0 and stackEnd.shape[0] > 0:

        training=np.concatenate((stackBegin,stackEnd),axis=0)

    elif stackEnd.shape[0] > 0:

        training=stackEnd

    elif stackBegin.shape[0] > 0:

        training=stackBegin

    return training,testing



@njit
def np_set(a,i,v):

    a[i]=v

    return a
