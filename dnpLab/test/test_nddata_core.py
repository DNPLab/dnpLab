import unittest
from numpy.testing import assert_array_equal
from dnpLab.core import nddata
import numpy as np
import random

test_dims = ['x', 'y', 'z', 'p', 'q', 'r']

class dnpLab_nddata_core_tester(unittest.TestCase):
    def setUp(self):
        self.dims = test_dims
        random.sample(test_dims, random.randint(1,len(test_dims)))

    def test_nddata_core_init(self):
        for ix in range(1000):
            random_dims = random.sample(test_dims, random.randint(1,len(test_dims)))

            random_coords = [np.r_[0:random.randint(1,6)] for dim in random_dims]
            shape = [coord.size for coord in random_coords]

            random_values = np.random.randn(*shape)
            data = nddata.nddata_core(random_values, random_dims, random_coords)
            self.assertTrue(data._self_consistent())
            assert_array_equal(data.values, random_values)
            for ix, dim in enumerate(random_dims):
                assert_array_equal(data.coords[dim], random_coords[ix])
            self.assertListEqual(data.dims, random_dims)

    def test_nddata_core_add(self):
        for ix in range(1000):
            random_coords = [np.r_[0:random.randint(1,6)] for dim in test_dims]

            random_axis = list(zip(test_dims, random_coords))

            random_axis1 = random.sample(random_axis, 3)
            random_axis2 = random.sample(random_axis, 3)

            dims1 = [axis[0] for axis in random_axis1]
            coords1 = [axis[1] for axis in random_axis1]
            shape1 = [coord.size for coord in coords1]
            values1 = np.random.randn(*shape1)
            data1 = nddata.nddata_core(values1, dims1, coords1)

            dims2 = [axis[0] for axis in random_axis2]
            coords2 = [axis[1] for axis in random_axis2]
            shape2 = [coord.size for coord in coords2]
            values2 = np.random.randn(*shape2)
            data2 = nddata.nddata_core(values2, dims2, coords2)

            data = data1 + data2

            self.assertTrue(data._self_consistent())
            assert_array_equal((data1+1).values, values1+1)
            assert_array_equal((data1+1.).values, values1+1.)
            assert_array_equal((data1+1.j).values, values1+1.j)

    def test_nddata_core_math_operators(self):
        for ix in range(1000):
            random_coords = [np.r_[0:random.randint(1,6)] for dim in test_dims]

            random_axis = list(zip(test_dims, random_coords))

            random_axis = random.sample(random_axis, 3)

            dims = [axis[0] for axis in random_axis]
            coords = [axis[1] for axis in random_axis]
            shape = [coord.size for coord in coords]
            values = np.random.randn(*shape)
            data = nddata.nddata_core(values, dims, coords)

            random_array = np.random.randn(*shape)

            #__add__
            assert_array_equal((data+1).values, values+1)
            assert_array_equal((data+1.).values, values+1.)
            assert_array_equal((data+1.j).values, values+1.j)
            assert_array_equal((data+random_array).values, values+random_array)

            #__sub__
            assert_array_equal((data-1).values, values-1)
            assert_array_equal((data-1.).values, values-1.)
            assert_array_equal((data-1.j).values, values-1.j)
            assert_array_equal((data-random_array).values, values-random_array)

            #__mult__
            assert_array_equal((data*1).values, values*1)
            assert_array_equal((data*1.).values, values*1.)
            assert_array_equal((data*1.j).values, values*1.j)
            assert_array_equal((data*random_array).values, values*random_array)

            #__truediv__
            assert_array_equal((data/1).values, values/1)
            assert_array_equal((data/1.).values, values/1.)
            assert_array_equal((data/1.j).values, values/1.j)
            assert_array_equal((data/random_array).values, values/random_array)

            #__radd__
            assert_array_equal((1+data).values, 1+values)
            assert_array_equal((1.+data).values, 1.+values)
            assert_array_equal((1.j+data).values, 1.j+values)
            assert_array_equal((random_array+data).values, random_array+values)

            #__rsub__
            assert_array_equal((1-data).values, 1-values)
            assert_array_equal((1.-data).values, 1.-values)
            assert_array_equal((1.j-data).values, 1.j-values)
            assert_array_equal((random_array-data).values, random_array-values)

            #__rmult__
            assert_array_equal((1*data).values, 1*values)
            assert_array_equal((1.*data).values, 1.*values)
            assert_array_equal((1.j*data).values, 1.j*values)
            assert_array_equal((random_array*data).values, random_array*values)

            #__rtruediv__
            assert_array_equal((1/data).values, 1/values)
            assert_array_equal((1./data).values, 1./values)
            assert_array_equal((1.j/data).values, 1.j/values)
            assert_array_equal((random_array/data).values, random_array/values)


if __name__ == '__main__':
    pass
