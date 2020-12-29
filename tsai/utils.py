# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/000_utils.ipynb (unless otherwise specified).

__all__ = ['totensor', 'toarray', 'toL', 'to3dtensor', 'to2dtensor', 'to1dtensor', 'to3darray', 'to2darray',
           'to1darray', 'to3d', 'to2d', 'to1d', 'to2dPlus', 'to3dPlus', 'to2dPlusTensor', 'to2dPlusArray',
           'to3dPlusTensor', 'to3dPlusArray', 'todtype', 'bytes2size', 'bytes2GB', 'delete_all_in_dir', 'reverse_dict',
           'is_tuple', 'itemify', 'isnone', 'exists', 'ifelse', 'is_not_close', 'test_not_close', 'test_type',
           'test_ok', 'test_not_ok', 'test_error', 'assert_fn', 'test_gt', 'test_ge', 'test_lt', 'test_le', 'stack',
           'stack_pad', 'match_seq_len', 'random_shuffle', 'cat2int', 'cycle_dl', 'cycle_dl_to_device', 'cache_memmap',
           'memmap2cache', 'get_func_defaults', 'get_idx_from_df_col_vals', 'get_sublist_idxs', 'flatten_list',
           'display_pd_df', 'ttest', 'tscore', 'ttest_tensor', 'pcc', 'scc', 'a', 'b', 'remove_fn', 'npsave', 'np_save',
           'permute_2D', 'random_normal', 'random_half_normal', 'random_normal_tensor', 'random_half_normal_tensor',
           'clip_outliers', 'default_dpi', 'get_plot_fig', 'fig2buf', 'plot_scatter', 'jointplot_scatter',
           'jointplot_kde', 'get_idxs', 'apply_cmap', 'torch_tile', 'to_tsfresh_df', 'pcorr', 'scorr', 'torch_diff',
           'get_outliers_IQR', 'get_percentile', 'torch_clamp', 'torch_slice_by_dim', 'concat', 'reduce_memory_usage',
           'cls_name', 'roll2d', 'roll3d', 'random_roll2d', 'random_roll3d']

# Cell
from .imports import *
from fastcore.test import *

# Cell
import inspect
import sklearn

# Cell
def totensor(o):
    if isinstance(o, torch.Tensor): return o
    elif isinstance(o, np.ndarray):  return torch.from_numpy(o)
    elif isinstance(o, (list, L)): return torch.tensor(o)
    assert False, f"Can't convert {type(o)} to torch.Tensor"


def toarray(o):
    if isinstance(o, np.ndarray): return o
    elif isinstance(o, torch.Tensor): return o.cpu().numpy()
    elif isinstance(o, (list, L)): return np.array(o)
    assert False, f"Can't convert {type(o)} to np.array"


def toL(o):
    if isinstance(o, L): return o
    elif isinstance(o, list): return L(o)
    elif isinstance(o, (np.ndarray, torch.Tensor)): return L(o.tolist())
    assert False, f'passed object needs to be of type L, list, np.ndarray or torch.Tensor but is {type(o)}'


def to3dtensor(o):
    o = totensor(o)
    if o.ndim == 3: return o
    elif o.ndim == 1: return o[None, None]
    elif o.ndim == 2: return o[:, None]
    assert False, f'Please, review input dimensions {o.ndim}'


def to2dtensor(o):
    o = totensor(o)
    if o.ndim == 2: return o
    elif o.ndim == 1: return o[None]
    elif o.ndim == 3: return o[0]
    assert False, f'Please, review input dimensions {o.ndim}'


def to1dtensor(o):
    o = totensor(o)
    if o.ndim == 1: return o
    elif o.ndim == 3: return o[0,0]
    if o.ndim == 2: return o[0]
    assert False, f'Please, review input dimensions {o.ndim}'


def to3darray(o):
    o = toarray(o)
    if o.ndim == 3: return o
    elif o.ndim == 1: return o[None, None]
    elif o.ndim == 2: return o[:, None]
    assert False, f'Please, review input dimensions {o.ndim}'


def to2darray(o):
    o = toarray(o)
    if o.ndim == 2: return o
    elif o.ndim == 1: return o[None]
    elif o.ndim == 3: return o[0]
    assert False, f'Please, review input dimensions {o.ndim}'


def to1darray(o):
    o = toarray(o)
    if o.ndim == 1: return o
    elif o.ndim == 3: o = o[0,0]
    elif o.ndim == 2: o = o[0]
    assert False, f'Please, review input dimensions {o.ndim}'


def to3d(o):
    if o.ndim == 3: return o
    if isinstance(o, np.ndarray): return to3darray(o)
    if isinstance(o, torch.Tensor): return to3dtensor(o)


def to2d(o):
    if o.ndim == 2: return o
    if isinstance(o, np.ndarray): return to2darray(o)
    if isinstance(o, torch.Tensor): return to2dtensor(o)


def to1d(o):
    if o.ndim == 1: return o
    if isinstance(o, np.ndarray): return to1darray(o)
    if isinstance(o, torch.Tensor): return to1dtensor(o)


def to2dPlus(o):
    if o.ndim >= 2: return o
    if isinstance(o, np.ndarray): return to2darray(o)
    elif isinstance(o, torch.Tensor): return to2dtensor(o)


def to3dPlus(o):
    if o.ndim >= 3: return o
    if isinstance(o, np.ndarray): return to3darray(o)
    elif isinstance(o, torch.Tensor): return to3dtensor(o)


def to2dPlusTensor(o):
    return to2dPlus(totensor(o))


def to2dPlusArray(o):
    return to2dPlus(toarray(o))


def to3dPlusTensor(o):
    return to3dPlus(totensor(o))


def to3dPlusArray(o):
    return to3dPlus(toarray(o))


def todtype(dtype):
    def _to_type(o, dtype=dtype):
        if o.dtype == dtype: return o
        elif isinstance(o, torch.Tensor): o = o.to(dtype=dtype)
        elif isinstance(o, np.ndarray): o = o.astype(dtype)
        return o
    return _to_type

# Cell
def bytes2size(size_bytes):
    if size_bytes == 0: return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])

def bytes2GB(byts):
    return round(byts / math.pow(1024, 3), 2)

# Cell
def delete_all_in_dir(tgt_dir, exception=None):
    if exception is not None and len(L(exception)) > 1: exception = tuple(exception)
    for file in os.listdir(tgt_dir):
        if exception is not None and file.endswith(exception): continue
        file_path = os.path.join(tgt_dir, file)
        if os.path.isfile(file_path) or os.path.islink(file_path): os.unlink(file_path)
        elif os.path.isdir(file_path): shutil.rmtree(file_path)

# Cell
def reverse_dict(dictionary):
    return {v: k for k, v in dictionary.items()}

# Cell
def is_tuple(o): return isinstance(o, tuple)

# Cell
def itemify(*o, tup_id=None):
    o = [o_ for o_ in L(*o) if o_ is not None]
    items = L(o).zip()
    if tup_id is not None: return L([item[tup_id] for item in items])
    else: return items

# Cell
def isnone(o):
    return o is None

def exists(o): return o is not None

def ifelse(a, b, c):
    "`b` if `a` is True else `c`"
    return b if a else c

# Cell
def is_not_close(a, b, eps=1e-5):
    "Is `a` within `eps` of `b`"
    if hasattr(a, '__array__') or hasattr(b, '__array__'):
        return (abs(a - b) > eps).all()
    if isinstance(a, (Iterable, Generator)) or isinstance(b, (Iterable, Generator)):
        return is_not_close(np.array(a), np.array(b), eps=eps)
    return abs(a - b) > eps


def test_not_close(a, b, eps=1e-5):
    "`test` that `a` is within `eps` of `b`"
    test(a, b, partial(is_not_close, eps=eps), 'not_close')


def test_type(a, b):
    return test_eq(type(a), type(b))


def test_ok(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
        e = 0
    except:
        e = 1
        pass
    test_eq(e, 0)

def test_not_ok(f, *args, **kwargs):
    try:
        f(*args, **kwargs)
        e = 0
    except:
        e = 1
        pass
    test_eq(e, 1)

def test_error(error, f, *args, **kwargs):
    try: f(*args, **kwargs)
    except Exception as e:
        test_eq(str(e), error)

# Cell
def assert_fn(*args, **kwargs): assert False, 'assertion test'
test_error('assertion test', assert_fn, 35, a=3)

# Cell
def test_gt(a,b):
    "`test` that `a>b`"
    test(a,b,gt,'>')

def test_ge(a,b):
    "`test` that `a>=b`"
    test(a,b,ge,'>')

def test_lt(a,b):
    "`test` that `a>b`"
    test(a,b,lt,'<')

def test_le(a,b):
    "`test` that `a>b`"
    test(a,b,le,'<=')

# Cell
def stack(o, axis=0, retain=True):
    if isinstance(o[0], torch.Tensor):
        return retain_type(torch.stack(tuple(o), dim=axis),  o[0]) if retain else torch.stack(tuple(o), dim=axis)
    else:
        return retain_type(np.stack(o, axis), o[0]) if retain else np.stack(o, axis)

def stack_pad(l):
    def resize(row, size):
        new = np.array(row)
        new.resize(size)
        return new
    row_length = max(l, key=len).__len__()
    mat = np.array([resize(row, row_length) for row in l])
    return mat

# Cell
def match_seq_len(*arrays):
    max_len = stack([x.shape[-1] for x in arrays]).max()
    return [np.pad(x, pad_width=((0,0), (0,0), (max_len - x.shape[-1], 0)), mode='constant', constant_values=0) for x in arrays]

# Cell
def random_shuffle(o, random_state=None):
    res = sklearn.utils.shuffle(o, random_state=random_state)
    if isinstance(o, L): return L(list(res))
    return res

# Cell
def cat2int(o):
    cat = Categorize()
    cat.setup(o)
    return stack(TfmdLists(o, cat)[:])

# Cell
def cycle_dl(dl):
    for _ in dl: _

def cycle_dl_to_device(dl):
    for bs in dl: [b.to(default_device()) for b in bs]

# Cell
def cache_memmap(o, slice_len=1000, verbose=False):
    start = 0
    slice_len = 1000
    for i in range(len(o) // 1000 + 1):
        o[start:start + slice_len]
        start += slice_len
        if verbose and i % 10 == 0: print(i)

memmap2cache =  cache_memmap

# Cell
def get_func_defaults(f):
    fa = inspect.getfullargspec(f)
    if fa.defaults is None: return dict(zip(fa.args, [''] * (len(fa.args))))
    else: return dict(zip(fa.args, [''] * (len(fa.args) - len(fa.defaults)) + list(fa.defaults)))

# Cell
def get_idx_from_df_col_vals(df, col, val_list):
    return [df[df[col] == val].index[0] for val in val_list]

# Cell
def get_sublist_idxs(aList, bList):
    "Get idxs that when applied to aList will return bList. aList must contain all values in bList"
    sorted_aList = aList[np.argsort(aList)]
    return np.argsort(aList)[np.searchsorted(sorted_aList, bList)]

# Cell
def flatten_list(l):
    return [item for sublist in l for item in sublist]

# Cell
def display_pd_df(df, max_rows:Union[bool, int]=False, max_columns:Union[bool, int]=False):
    if max_rows:
        old_max_rows = pd.get_option('display.max_rows')
        if max_rows is not True and isinstance(max_rows, Integral): pd.set_option('display.max_rows', max_rows)
        else: pd.set_option('display.max_rows', df.shape[0])
    if max_columns:
        old_max_columns = pd.get_option('display.max_columns')
        if max_columns is not True and isinstance(max_columns, Integral): pd.set_option('display.max_columns', max_columns)
        else: pd.set_option('display.max_columns', df.shape[1])
    display(df)
    if max_rows: pd.set_option('display.max_rows', old_max_rows)
    if max_columns: pd.set_option('display.max_columns', old_max_columns)

# Cell
def ttest(data1, data2, equal_var=False):
    "Calculates t-statistic and p-value based on 2 sample distributions"
    t_stat, p_value = scipy.stats.ttest_ind(data1, data2, equal_var=equal_var)
    return t_stat, np.sign(t_stat) * p_value

def tscore(o):
    if o.std() == 0: return 0
    else: return np.sqrt(len(o)) * o.mean() / o.std()

# Cell
def ttest_tensor(a, b):
    "differentiable pytorch function equivalent to scipy.stats.ttest_ind with equal_var=False"
    # calculate standard errors
    se1, se2 = torch.std(a)/np.sqrt(len(a)), torch.std(b)/np.sqrt(len(b))
    # standard error on the difference between the samples
    sed = torch.sqrt(se1**2.0 + se2**2.0)
    # calculate the t statistic
    t_stat = (torch.mean(a) - torch.mean(b)) / sed
    return t_stat

# Cell

#export
from scipy.stats import pearsonr, spearmanr

def pcc(a, b):
    return pearsonr(a, b)[0]

def scc(a, b):
    return spearmanr(a, b)[0]

a = np.random.normal(0.5, 1, 100)
b = np.random.normal(0.15, .5, 100)
pcc(a, b), scc(a, b)

# Cell
def remove_fn(fn, verbose=False):
    "Removes a file (fn) if exists"
    try:
        os.remove(fn)
        pv(f'{fn} file removed', verbose)
    except OSError:
        pv(f'{fn} does not exist', verbose)
        pass

# Cell
def npsave(array_fn, array, verbose=True):
    remove_fn(array_fn, verbose)
    pv(f'saving {array_fn}...', verbose)
    np.save(array_fn, array)
    pv(f'...{array_fn} saved', verbose)

np_save = npsave

# Cell
def permute_2D(array, axis=None):
    "Permute rows or columns in an array. This can be used, for example, in feature permutation"
    if axis == 0: return array[np.random.randn(*array.shape).argsort(axis=0), np.arange(array.shape[-1])[None, :]]
    elif axis == 1 or axis == -1: return array[np.arange(len(array))[:,None], np.random.randn(*array.shape).argsort(axis=1)]
    return array[np.random.randn(*array.shape).argsort(axis=0), np.random.randn(*array.shape).argsort(axis=1)]

# Cell
def random_normal():
    "Returns a number between -1 and 1 with a normal distribution"
    while True:
        o = np.random.normal(loc=0., scale=1/3)
        if abs(o) <= 1: break
    return o

def random_half_normal():
    "Returns a number between 0 and 1 with a half-normal distribution"
    while True:
        o = abs(np.random.normal(loc=0., scale=1/3))
        if o <= 1: break
    return o

def random_normal_tensor(shape=1, device=None):
    "Returns a tensor of a predefined shape between -1 and 1 with a normal distribution"
    return torch.empty(shape, device=device).normal_(mean=0, std=1/3).clamp_(-1, 1)

def random_half_normal_tensor(shape=1, device=None):
    "Returns a tensor of a predefined shape between 0 and 1 with a half-normal distribution"
    return abs(torch.empty(shape, device=device).normal_(mean=0, std=1/3)).clamp_(0, 1)

# Cell
def clip_outliers(o):
    Q1, Q3 = np.percentile(o, [25, 75])
    IQR = Q3 - Q1
    if isinstance(o, (np.ndarray, pd.core.series.Series)):
        return np.clip(o, Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)
    elif isinstance(o, torch.Tensor):
        return torch.clamp(o, Q1 - 1.5 * IQR, Q3 + 1.5 * IQR)

# Cell
from matplotlib.backends.backend_agg import FigureCanvasAgg

def default_dpi():
    DPI = plt.gcf().get_dpi()
    plt.close()
    return int(DPI)

def get_plot_fig(size=None, dpi=default_dpi()):
    fig = plt.figure(figsize=(size / dpi, size / dpi), dpi=dpi, frameon=False) if size else plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    config = plt.gcf()
    plt.close('all')
    return config

def fig2buf(fig):
    canvas = FigureCanvasAgg(fig)
    fig.canvas.draw()
    return np.asarray(canvas.buffer_rgba())[..., :3]

# Cell
def plot_scatter(x, y, deg=1):
    linreg = sp.stats.linregress(x, y)
    plt.scatter(x, y, label=f'R2:{linreg.rvalue:.2f}', color='lime', edgecolor='black', alpha=.5)
    plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, deg))(np.unique(x)), color='r')
    plt.legend(loc='best')
    plt.show()

# Cell
import seaborn as sns
def jointplot_scatter(x,y,**kwargs):
    sns.jointplot(x, y, kind='scatter', **kwargs)
    plt.show()

def jointplot_kde(x,y,**kwargs):
    sns.jointplot(x, y, kind='kde', **kwargs)
    plt.show()

# Cell
def get_idxs(o, aList): return array([o.tolist().index(v) for v in aList])

# Cell
def apply_cmap(o, cmap):
    o = toarray(o)
    out = plt.get_cmap(cmap)(o)[..., :3]
    out = tensor(out).squeeze(1)
    return out.permute(0, 3, 1, 2)

# Cell
def torch_tile(a, n_tile, dim=0):
    init_dim = a.size(dim)
    repeat_idx = [1] * a.dim()
    repeat_idx[dim] = n_tile
    a = a.repeat(*(repeat_idx))
    order_index = torch.cat([init_dim * torch.arange(n_tile) + i for i in range(init_dim)]).to(device=a.device)
    return torch.index_select(a, dim, order_index)

# Cell
def to_tsfresh_df(ts):
    r"""Prepares a time series (Tensor/ np.ndarray) to be used as a tsfresh dataset to allow feature extraction"""
    ts = to3d(ts)
    if isinstance(ts, np.ndarray):
        ids = np.repeat(np.arange(len(ts)), ts.shape[-1]).reshape(-1,1)
        joint_ts =  ts.transpose(0,2,1).reshape(-1, ts.shape[1])
        cols = ['id'] + np.arange(ts.shape[1]).tolist()
        df = pd.DataFrame(np.concatenate([ids, joint_ts], axis=1), columns=cols)
    elif isinstance(ts, torch.Tensor):
        ids = torch_tile(torch.arange(len(ts)), ts.shape[-1]).reshape(-1,1)
        joint_ts =  ts.transpose(1,2).reshape(-1, ts.shape[1])
        cols = ['id']+np.arange(ts.shape[1]).tolist()
        df = pd.DataFrame(torch.cat([ids, joint_ts], dim=1).numpy(), columns=cols)
    df['id'] = df['id'].astype(int)
    df.reset_index(drop=True, inplace=True)
    return df

# Cell
from scipy.stats import skew, kurtosis

def pcorr(a, b):
    return scipy.stats.pearsonr(a, b)

def scorr(a, b):
    corr = scipy.stats.spearmanr(a, b)
    return corr[0], corr[1]

# Cell
def torch_diff(t, lag=1, pad=True):
    import torch.nn.functional as F
    diff = t[..., lag:] - t[..., :-lag]
    if pad: return F.pad(diff, (lag,0))
    else: return diff

# Cell
def get_outliers_IQR(o, axis=None):
    if isinstance(o, torch.Tensor): o = o.detach().cpu().numpy()
    Q1 = np.percentile(o, 25, axis=axis, keepdims=axis is not None)
    Q3 = np.percentile(o, 75, axis=axis, keepdims=axis is not None)
    IQR = Q3 - Q1
    max, min = Q1 - 1.5 * IQR, Q3 + 1.5 * IQR
    return Q1 - 1.5 * IQR, Q3 + 1.5 * IQR

def get_percentile(o, percentile, axis=None):
    if isinstance(o, torch.Tensor): o = o.detach().cpu().numpy()
    return np.percentile(o, percentile, axis=axis, keepdims=axis is not None)

def torch_clamp(o, min=None, max=None):
    r"""Clamp torch.Tensor using 1 or multiple dimensions"""
    if min is not None: o = torch.max(o, min)
    if max is not None: o = torch.min(o, max)
    return o

# Cell
def torch_slice_by_dim(t, index, dim=-1, **kwargs):
    if not isinstance(index, torch.Tensor): index = torch.Tensor(index)
    assert t.ndim == index.ndim, "t and index must have the same ndim"
    index = index.long()
    return torch.gather(t, dim, index, **kwargs)

# Cell
def concat(*ls, dim=0):
    "Concatenate tensors, arrays, lists, or tuples by a dimension"
    if not len(ls): return []
    it = ls[0]
    if isinstance(it, torch.Tensor): return torch.cat(ls, dim=dim)
    elif isinstance(it, np.ndarray): return np.concatenate(ls, axis=dim)
    else:
        res = np.concatenate(ls, axis=dim).tolist()
        return retain_type(res, typ=type(it))

# Cell
def reduce_memory_usage(df):

    start_memory = df.memory_usage().sum() / 1024**2
    print(f"Memory usage of dataframe is {start_memory} MB")

    for col in df.columns:
        col_type = df[col].dtype

        if col_type != 'object':
            c_min = df[col].min()
            c_max = df[col].max()

            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)

            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    pass
        else:
            df[col] = df[col].astype('category')

    end_memory = df.memory_usage().sum() / 1024**2
    print(f"Memory usage of dataframe after reduction {end_memory} MB")
    print(f"Reduced by {100 * (start_memory - end_memory) / start_memory} % ")
    return df

# Cell
def cls_name(o): return o.__class__.__name__

# Cell

# This solution is based on https://stackoverflow.com/questions/20360675/roll-rows-of-a-matrix-independently
def roll2d(o, roll1=None, roll2=None):
    r"""Rolls a 2D object on the indicated axis"""
    assert o.ndim == 2, "roll2D can only be applied to 2d objects"
    axis1, axis2 = np.ogrid[:o.shape[0], :o.shape[1]]
    if roll1 is not None:
        axis1 = axis1 - roll1.reshape(-1, 1)
    if roll2 is not None:
        axis2 = axis2 - roll2.reshape(-1, 1)
    return o[axis1, axis2]


# This solution is based on https://stackoverflow.com/questions/20360675/roll-rows-of-a-matrix-independently
def roll3d(o, roll1=None, roll2=None, roll3=None):
    r"""Rolls a 3D object on the indicated axis"""
    assert o.ndim == 3, "roll3D can only be applied to 3d objects"
    axis1, axis2, axis2 = np.ogrid[:o.shape[0], :o.shape[1], :o.shape[2]]
    if roll1 is not None:
        axis1 = axis1 - roll1.reshape(-1, 1)
    if roll2 is not None:
        axis2 = axis2 - roll2.reshape(-1, 1)
    if roll3 is not None:
        axis3 = axis3 - roll3.reshape(-1, 1)
    return o[axis1, axis2, axis3]


# This solution is based on https://stackoverflow.com/questions/20360675/roll-rows-of-a-matrix-independently
def random_roll2d(o, axis=()):
    r"""Rolls a 2D object on the indicated axis"""
    axis1, axis2 = np.ogrid[:o.shape[0], :o.shape[1]]
    if 0 in axis:
        roll1 = np.random.randint(0, o.shape[0], o.shape[0]).reshape(-1, 1)
        axis1 = axis1 - roll1
    if 1 in axis:
        roll2 = np.random.randint(0, o.shape[1], o.shape[0]).reshape(-1, 1)
        axis2 = axis2 - roll2
    return o[axis1, axis2]


# This solution is based on https://stackoverflow.com/questions/20360675/roll-rows-of-a-matrix-independently
def random_roll3d(o, axis=()):
    r"""Rolls a 3D object on the indicated axis"""
    axis1, axis2, axis3 = np.ogrid[:o.shape[0], :o.shape[1], :o.shape[2]]
    if 0 in axis:
        roll1 = np.random.randint(0, o.shape[0], o.shape[0]).reshape(-1, 1, 1)
        axis1 = axis1 - roll1
    if 1 in axis:
        roll2 = np.random.randint(0, o.shape[1], o.shape[0]).reshape(-1, 1, 1)
        axis2 = axis2 - roll2
    if 2 in axis:
        roll3 = np.random.randint(0, o.shape[2], o.shape[0]).reshape(-1, 1, 1)
        axis3 = axis3 - roll3
    return o[axis1, axis2, axis3]