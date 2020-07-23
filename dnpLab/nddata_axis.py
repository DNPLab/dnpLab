from __future__ import division
from collections.abc import MutableMapping
from collections import OrderedDict
import numpy as np

class nddata_axis(object):
    '''
    '''

    def __init__(self, dim, *args):
        '''

        Args:
            dim (str): name of dimension
        '''

        self.dim = dim
        if len(args) == 0:
            self.__start = None
            self.__stop = None
            self.__step = None

        if len(args) == 1:
            coord = args[0]
            if isinstance(coord, np.ndarray):
                self._axis = coord
                try:
                    self.reduce()
                except:
                    self._type = 'ndarray'
            elif isinstance(coord, slice):
                self.__start = coord.start
                self.__stop = coord.stop
                self.__step = coord.step
            elif isinstance(coord, (int,float)):
                self.__start = None
                self.__stop = coord
                self.__step = None
            else:
                raise ValueError('coord not understood')
        if len(args) == 2:
            start = args[0]
            stop = args[1]
            if isinstance(start, (int, float)) and isinstance(stop, (int,float)):
                self.__start = start
                self.__stop = stop
                self.__step = None
            else:
                raise TypeError('coord not understood')
        if len(args) == 3:
            start = args[0]
            stop = args[1]
            step = args[2]
            if isinstance(start, (int,float)) and isinstance(stop, (int, float)) and isinstance(step, (int, float)):
                self.__start = start
                self.__stop = stop
                self.__step = step
            else:
                raise TypeError('coord not understood')
    
    def reduce(self):
        '''
        '''

        if hasattr(self, '_array'):
            start = self._array[0]
            step = self._array[1] - self._array[0]
            stop = self._array[-1] + step

            if np.allclose(self._array, np.r_[slice(start,stop,step)]):
                self.start = start
                self.stop = stop
                self.step = step
            else:
                raise ValueError('Array must have evenly spaced values to be reduced')
        else:
            raise ValueError('No array to reduce')

    @property
    def dim(self):
        return self.__dim

    @dim.setter
    def dim(self, dim):
        '''
        '''

        if isinstance(dim, str):
            self.__dim = dim
        else:
            raise TypeError('dim must be type str not %s'%str(type(dim)))

    @property
    def start(self):
        '''
        '''
        return self.__start

    @start.setter
    def start(self, b):
        '''
        '''
        if isinstance(b, (int, float)):
            self.__start = b

    @property
    def stop(self):
        '''
        '''
        return self.__stop

    @stop.setter
    def stop(self, b):
        '''
        '''
        if isinstance(b, (int, float)):
            self.__stop = b

    @property
    def step(self):
        '''
        '''
        return self.__step

    @step.setter
    def step(self, b):
        '''
        '''
        if isinstance(b, (int, float)):
            self.__step = b

    @property
    def array(self):
        '''Return axes as numpy array
        '''

        # Fast method
#        try:
#            return self._array
#        except:
#            self._array = np.r_[slice(self.start, self.stop, self.step)]
#            return self._array
        # 2nd Attempt at fast method
        if hasattr(self, '_array'):
            return self._array
        else:
            self._array = np.r_[slice(self.start, self.stop, self.step)]
            return self._array

#        # Slow method, 56 times slower
#        return np.r_[slice(self.start, self.stop, self.step)]

    @array.setter
    def array(self, b):
        '''
        '''
        if isinstance(b, np.ndarray):
            self._array = b
        else:
            raise TypeError('array type must be numpy.ndarray')
           

    @array.deleter
    def array(self):
        del self._array

    def slice(self, *args):
        '''
        '''
        return self.array[slice(*args)]

    def __getitem__(self, x):
        '''
        '''
        return self.array[x] # Faster by 10% if array is stored in object 
#        return self.start + self.step * x

    def _del_array(self):
        '''
        '''
        del self._array


    @property
    def size(self):
        '''
        '''
        return self.array.size # 3 times faster when array is stored in object
#        return max(int((self.stop - self.start) / self.step),0) # Take max for case when direction is reversed
    def __repr__(self):
        return 'nddata_axis(\'{}\', {})'.format(self.dim,self.array)

    def __str__(self):
        return '\'{}\':{}'.format(self.dim,str(self.array))
    
    def __add__(self, b):
        start = self.start + b
        stop = self.stop + b
        step = self.step

        if hasattr(self, '_array'):
            del self.array

        return nddata_axis(self.dim, slice(start, stop, step))

    __radd__ = __add__

    def __sub__(self, b):
        start = self.start - b
        stop = self.stop - b
        step = self.step

        if hasattr(self, '_array'):
            del self.array

        return nddata_axis(self.dim, slice(start, stop, step))

    def __rsub__(self, b):
        # switch start and stop
        start = b - self.stop
        stop = b - self.start 
        step = self.step

        if hasattr(self, '_array'):
            del self.array

        return nddata_axis(self.dim, slice(start, stop, step))

    def __mul__(self, b):
        start = b * self.start
        stop = b * self.stop
        step = b * self.step

        if hasattr(self, '_array'):
            del self.array

        return nddata_axis(self.dim, slice(start, stop, step))

    __rmul__ = __mul__

    def __truediv__(self, b):
        start = self.start / b
        stop = self.stop / b
        step = self.step / b

        if hasattr(self, '_array'):
            del self.array

        return nddata_axis(self.dim, slice(start, stop, step))

    def __rtruediv__(self, b):
        start = b / self.start
        stop = b / self.stop
        step = b / self.step

        if hasattr(self, '_array'):
            del self.array

        return nddata_axis(self.dim, slice(start, stop, step))

    def __array__(self):
        return self.array

    def __len__(self):
        return len(self.array)

class nddata_axis_collection(MutableMapping):

    def __init__(self, *args, **kwargs):
        self.store = OrderedDict()
        for arg in args:
            self.__setitem__(arg)

    def __getitem__(self, key):
        return self.store[key]

    def __setitem__(self, value):
        if not isinstance(value, nddata_axis):
            raise TypeError('argument must be type nddata_axis not %s'%str(type(b)))

        self.store[value.dim] = value

    def __delitem__(self, key):
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __repr__(self):
        return 'nddata_axis_collection({})'.format(self.store)

    def __str__(self):
        return '{}'.format(self.store)

    def index(self, key):
        return list(self.store).index(key)

    @property
    def coords(self):
        return [coord.array for coord in self.store.values()]

if __name__ == '__main__':

    coord = nddata_axis('x',slice(0,10,1))

    a = nddata_axis('x',slice(0,1,1e-3))

    d = nddata_axis_collection(*[a])
