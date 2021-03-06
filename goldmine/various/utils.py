import numpy as np
import autograd
import os
import logging
import sys
import inspect
import torch


def check_random_state(random_state, use_autograd=False):
    if random_state is None or isinstance(random_state, int):
        if use_autograd:
            return autograd.numpy.random.RandomState(random_state)
        return np.random.RandomState(random_state)
    else:
        return random_state


def general_init(debug=False):
    logging.basicConfig(format='%(asctime)s  %(message)s', datefmt='%H:%M')

    if debug:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    logging.info('')
    logging.info('------------------------------------------------------------')
    logging.info('|                                                          |')
    logging.info('|  goldmine                                                |')
    logging.info('|                                                          |')
    logging.info('|              Experiments with simulator-based inference  |')
    logging.info('|                                                          |')
    logging.info('------------------------------------------------------------')
    logging.info('')

    logging.info('Hi! How are you today?')

    np.seterr(divide='ignore', invalid='ignore')

    np.set_printoptions(formatter={'float_kind': lambda x: "%.4f" % x})


def create_missing_folders(base_dir, simulator_name, inference_name=None):
    required_subfolders = ['thetas/' + simulator_name,
                           'samples/' + simulator_name]
    if inference_name is not None:
        required_subfolders += ['models/' + simulator_name + '/' + inference_name,
                                'results/' + simulator_name + '/' + inference_name]

    for subfolder in required_subfolders:
        folder = base_dir + '/goldmine/data/' + subfolder

        if not os.path.exists(folder):
            logging.info('Folder %s does not exist, will be created', folder)
            os.makedirs(folder)

        elif not os.path.isdir(folder):
            raise OSError('Path {} exists, but is no folder!'.format(folder))


def shuffle(*arrays):
    """ Shuffles multiple arrays simultaneously"""

    permutation = None
    n_samples = None
    shuffled_arrays = []

    for i, a in enumerate(arrays):
        if a is None:
            shuffled_arrays.append(a)
            continue

        if permutation is None:
            n_samples = a.shape[0]
            permutation = np.random.permutation(n_samples)

        if a.shape[0] != n_samples:
            logging.error('Mismatched shapes in shuffle:')
            for arr in arrays:
                if arr is None:
                    logging.info('  None')
                else:
                    logging.info('  Array with shape %s', arr.shape)
            raise RuntimeError('Mismatched shapes in shuffle')

        shuffled_a = a[permutation]
        shuffled_arrays.append(shuffled_a)

    return shuffled_arrays


def load_and_check(filename, warning_threshold=1.e9, min_value=- np.exp(25.), max_value=np.exp(25.)):
    data = np.load(filename)

    if not (np.issubdtype(data.dtype, np.floating) or np.issubdtype(data.dtype, np.integer)):
        data = data.astype(np.float)

    n_nans = np.sum(np.isnan(data))
    n_infs = np.sum(np.isinf(data))
    n_finite = np.sum(np.isfinite(data))

    if n_nans + n_infs > 0:
        logging.warning('Warning: file %s contains %s NaNs and %s Infs, compared to %s finite numbers!',
                        filename, n_nans, n_infs, n_finite)

    if n_infs > 0 and max_value is not None:
        logging.info('Replacing %s  infinite values in file %s with %s', n_infs, filename, max_value)
        data[np.isinf(data)] = max_value

    smallest = np.nanmin(data)
    largest = np.nanmax(data)

    if np.abs(smallest) > warning_threshold or np.abs(largest) > warning_threshold:
        logging.warning('Warning: file %s has some very large numbers, rangin from %s to %s',
                        filename, smallest, largest)

    if max_value is not None and np.sum(data > max_value) > 0:
        logging.info('Replacing %s large values in file %s with %s', np.sum(data > max_value), filename, max_value)
        data[data > max_value] = max_value

    if min_value is not None and np.sum(data < min_value) > 0:
        logging.info('Replacing %s small values in file %s with %s', np.sum(data < min_value), filename, min_value)
        data[data < min_value] = min_value

    return data


def get_activation_function(activation_name):
    if activation_name == 'relu':
        return torch.relu
    elif activation_name == 'tanh':
        return torch.tanh
    elif activation_name == 'sigmoid':
        return torch.sigmoid
    else:
        raise ValueError('Activation function %s unknown', activation_name)


def discretize(data, discretization):
    for c in range(data.shape[1]):
        if discretization[c] is None or discretization[c] <= 0.:
            continue
        assert discretization[c] > 0.

        data[:, c] = np.round(data[:, c] / discretization[c], 0) * discretization[c]

    return data


def get_size(obj, seen=None):
    """ Recursively finds size of objects in bytes, from https://github.com/bosswissam/pysize/blob/master/pysize.py """
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if hasattr(obj, '__dict__'):
        for cls in obj.__class__.__mro__:
            if '__dict__' in cls.__dict__:
                d = cls.__dict__['__dict__']
                if inspect.isgetsetdescriptor(d) or inspect.ismemberdescriptor(d):
                    size += get_size(obj.__dict__, seen)
                break
    if isinstance(obj, dict):
        size += sum((get_size(v, seen) for v in obj.values()))
        size += sum((get_size(k, seen) for k in obj.keys()))
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum((get_size(i, seen) for i in obj))

    if hasattr(obj, '__slots__'):  # can have __slots__ with __dict__
        size += sum(get_size(getattr(obj, s), seen) for s in obj.__slots__ if hasattr(obj, s))

    return float(size)


def check_for_nans_in_parameters(model, check_gradients=True):
    for param in model.parameters():
        if torch.any(torch.isnan(param)):
            return True

        if check_gradients and torch.any(torch.isnan(param.grad)):
            return True

    return False


def expand_array_2d(array, n_copies):
    if len(array.shape) == 1 or (len(array.shape) == 2 and array.shape[0] == 1):
        array = array.reshape((1, -1))
        array = np.broadcast_to(array, (n_copies, array.shape[1]))

    return array
