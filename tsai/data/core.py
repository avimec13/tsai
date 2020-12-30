# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/002_data.core.ipynb (unless otherwise specified).

__all__ = ['NumpyTensor', 'ToNumpyTensor', 'TSTensor', 'ToTSTensor', 'ToFloat', 'ToInt', 'TSClassification',
           'TSMultiLabelClassification', 'TSRegression', 'TSForecasting', 'NumpyTensorBlock', 'TSTensorBlock',
           'TorchDataset', 'NumpyDataset', 'TSDataset', 'NumpyDatasets', 'TSDatasets', 'add_ds', 'get_subset_dset',
           'NumpyDataLoader', 'show_tuple', 'TSDataLoader', 'NumpyDataLoaders', 'TSDataLoaders', 'get_ts_dls',
           'get_subset_dl', 'get_tsimage_dls']

# Cell
from ..imports import *
from ..utils import *
from .external import *
from .validation import *

# Cell
from matplotlib.ticker import PercentFormatter
import matplotlib.colors as mcolors

# Cell
class NumpyTensor(TensorBase):
    "Returns a `tensor` with subclass `NumpyTensor` that has a show method"

    def __new__(cls, o, **kwargs):
        if isinstance(o, (list, L)): o = stack(o)
        res = cast(tensor(o), cls)
        for k,v in kwargs.items(): setattr(res, k, v)
        return res

    @property
    def data(self): return cast(self, Tensor).data

    def __repr__(self):
        if self.numel() == 1: return f'{self}'
        else: return f'NumpyTensor(shape:{tuple(self.shape)})'


    def show(self, ax=None, ctx=None, title=None, title_color='black', **kwargs):
        if self.ndim == 0: return str(self)
        elif self.ndim != 2: self = type(self)(to2d(self))
        self = self.detach().cpu().numpy()
        ax = ifnone(ax, ctx)
        if ax is None: fig, ax = plt.subplots(**kwargs)
        ax.plot(self.T)
        ax.axis(xmin=0, xmax=self.shape[-1] - 1)
        ax.set_title(title, weight='bold', color=title_color)
        plt.tight_layout()
        return ax


class ToNumpyTensor(Transform):
    "Transforms an object into NumpyTensor"
    def encodes(self, o): return NumpyTensor(o)

# Cell
class TSTensor(NumpyTensor):
    '''Returns a `tensor` with subclass `TSTensor` that has a show method'''

    @property
    def vars(self):
        if self.ndim >=4: return self.shape[-3]
        else: return self.shape[-2]

    @property
    def len(self): return self.shape[-1]

    def __repr__(self):
        if self.numel() == 1: return f'{self}'
        elif self.ndim >= 3:
            return f'TSTensor(samples:{self.shape[-3]}, vars:{self.shape[-2]}, len:{self.shape[-1]})'
        elif self.ndim == 2:
            return f'TSTensor(vars:{self.shape[-2]}, len:{self.shape[-1]})'
        elif self.ndim == 1:
            return f'TSTensor(len:{self.shape[-1]})'


class ToTSTensor(Transform):
    "Transforms an object into TSTensor"
    def encodes(self, o): return TSTensor(o)

# Cell
class ToFloat(Transform):
    "Transforms an object dtype to float"
    def encodes(self, o:torch.Tensor): return o.float()
    def encodes(self, o): return o.astype(np.float32)
    def decodes(self, o): return TitledFloat(o) if o.ndim==0 else TitledTuple(o_.item() for o_ in o)


class ToInt(Transform):
    "Transforms an object dtype to int"
    def encodes(self, o:torch.Tensor): return o.long()
    def encodes(self, o): return o.astype(np.float32).astype(np.int64)
    def decodes(self, o): return TitledFloat(o) if o.ndim==0 else TitledTuple(o_.item() for o_ in o)


TSClassification = Categorize
TSMultiLabelClassification = MultiCategorize
TSRegression = ToFloat
TSForecasting = ToFloat

# Cell
class NumpyTensorBlock():
    def __init__(self, type_tfms=None, item_tfms=None, batch_tfms=None, dl_type=None, dls_kwargs=None):
        self.type_tfms  =                 L(type_tfms)
        self.item_tfms  = ToNumpyTensor + L(item_tfms)
        self.batch_tfms =                 L(batch_tfms)
        self.dl_type,self.dls_kwargs = dl_type,({} if dls_kwargs is None else dls_kwargs)

class TSTensorBlock():
    def __init__(self, type_tfms=None, item_tfms=None, batch_tfms=None, dl_type=None, dls_kwargs=None):
        self.type_tfms  =              L(type_tfms)
        self.item_tfms  = ToTSTensor + L(item_tfms)
        self.batch_tfms =              L(batch_tfms)
        self.dl_type,self.dls_kwargs = dl_type,({} if dls_kwargs is None else dls_kwargs)

# Cell
class TorchDataset():
    def __init__(self, X, y=None): self.X, self.y = X, y
    def __getitem__(self, idx): return (self.X[idx],) if self.y is None else (self.X[idx], self.y[idx])
    def __len__(self): return len(self.X)


class NumpyDataset():
    def __init__(self, X, y=None, types=None): self.X, self.y, self.types = X, y, types
    def __getitem__(self, idx):
        if self.types is None: return (self.X[idx], self.y[idx]) if self.y is not None else (self.X[idx])
        else: return (self.types[0](self.X[idx]), self.types[1](self.y[idx])) if self.y is not None else (self.types[0](self.X[idx]))
    def __len__(self): return len(self.X)
    @property
    def c(self): return 0 if self.y is None else 1 if isinstance(self.y[0], float) else len(np.unique(self.y))


class TSDataset():
    def __init__(self, X, y=None, types=None, sel_vars=None, sel_steps=None):
        self.X, self.y, self.types = to3darray(X), y, types
        self.sel_vars = ifnone(sel_vars, slice(None))
        self.sel_steps = ifnone(sel_steps,slice(None))
    def __getitem__(self, idx):
        if self.types is None: return (self.X[idx, self.sel_vars, self.sel_steps], self.y[idx]) if self.y is not None else (self.X[idx])
        else:
            return (self.types[0](self.X[idx, self.sel_vars, self.sel_steps]), self.types[1](self.y[idx])) if self.y is not None \
            else (self.types[0](self.X[idx]))
    def __len__(self): return len(self.X)
    @property
    def c(self): return 0 if self.y is None else 1 if isinstance(self.y[0], float) else len(np.unique(self.y))
    @property
    def vars(self):
        if self[0][0].ndim >=4: return self[0][0].shape[-3]
        return self[0][0].shape[-2]
    @property
    def len(self): return self[0][0].shape[-1]

# Cell
@delegates(Datasets.__init__)
class NumpyDatasets(Datasets):
    "A dataset that creates tuples from X (and y) and applies `tfms` of type item_tfms"
    _xtype, _ytype = NumpyTensor, None # Expected X and y output types (must have a show method)
    def __init__(self, X=None, y=None, items=None, tfms=None, tls=None, n_inp=None, dl_type=None, inplace=True, **kwargs):
        self.inplace = inplace
        if tls is None:
            X = itemify(X, tup_id=0)
            y = itemify(y, tup_id=0) if y is not None else y
            items = tuple((X,)) if y is None else tuple((X,y))
            self.tfms = L(ifnone(tfms,[None]*len(ifnone(tls,items))))
        self.tls = L(tls if tls else [TfmdLists(item, t, **kwargs) for item,t in zip(items,self.tfms)])
        self.n_inp = (1 if len(self.tls)==1 else len(self.tls)-1) if n_inp is None else n_inp
        if 'split' in kwargs: self.split_idxs = kwargs['split']
        elif 'splits' in kwargs:  self.split_idxs = kwargs['splits']
        else: self.split_idxs = L(np.arange(len(self.tls[0]) if len(self.tls[0]) > 0 else len(self.tls)).tolist())
        if len(self.tls[0]) > 0:
            self.types = L([ifnone(_typ, type(tl[0]) if isinstance(tl[0], torch.Tensor) else tensor) for tl,_typ in zip(self.tls, [self._xtype, self._ytype])])
            self.ptls = L([tl if not self.inplace else tl[:] if type(tl[0]).__name__ == 'memmap' else tensor(stack(tl[:])) for tl in self.tls])

    def __getitem__(self, it):
        return tuple([typ(ptl[it]) for i,(ptl,typ) in enumerate(zip(self.ptls,self.types))])

    def subset(self, i): return type(self)(tls=L(tl.subset(i) for tl in self.tls), n_inp=self.n_inp, inplace=self.inplace, tfms=self.tfms,
                                          split=L(self.splits[i]) if self.splits is not None else None)

    def _new(self, X, *args, y=None, **kwargs):
        items = tuple((X,)) if y is None else tuple((X, y))
        return super()._new(items, tfms=self.tfms, do_setup=False, **kwargs)

    def show_at(self, idx, **kwargs):
        self.show(self[idx], **kwargs)
        plt.show()

    @delegates(plt.subplots)
    def show_dist(self, figsize=None, color=None, **kwargs):
        if self.c == 0:
            print('\nunlabeled dataset.\n')
            return
        _y = self.ptls[1].flatten().detach().cpu().numpy()
        if color == "random": color = random_shuffle(L(mcolors.CSS4_COLORS.keys()))
        elif color is None: color = ['m', 'orange', 'darkblue', 'lightgray']
        figsize = ifnone(figsize, (8, 6))
        fig = plt.figure(figsize=figsize, **kwargs)
        ax = plt.axes()
        ax.set_axisbelow(True)
        plt.grid(color='gainsboro', linewidth=.1)
        plt.title('Target distribution', fontweight='bold')
        if self.cat:
            data = np.unique(_y, return_counts=True)[1]
            data = data / np.sum(data)
            plt.bar(self.vocab, data, color=color, edgecolor='black')
            plt.xticks(self.vocab)
        else:
            data = _y
            weights=np.ones(len(data)) / len(data)
            plt.hist(data, bins=min(len(_y) // 2, 100), weights=weights, color='violet', edgecolor='black')
        plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
        plt.show()

    @property
    def items(self): return tuple([tl.items for tl in self.tls])
    @items.setter
    def items(self, vs):
        for tl,c in zip(self.tls, vs): tl.items = v

    @property
    def cat(self):
        try:
            if isinstance(self[0][-1].item(), Integral): return True
            else: return False
        except: pass
        try:
            if isinstance(self[0][-1][-1].item(), Integral): return True
            else: return False
        except: pass
        return False

    @property
    def c(self):
        if len(self.ptls) == 1: return 0
        elif not self.cat:
            if self.ptls[1][0].ndim == 0: return 1
            return len(self.ptls[1][0])
        return len(np.unique(self.ptls[1]))

    @property
    def d(self):
        if self.cat or self.c == 0: return None
        elif self.ptls[1][0].ndim <= 1: return None
        else: return len(self.ptls[1][0][0])


    @property
    def loss_func(self):
        return MSELossFlat() if not self.cat else CrossEntropyLossFlat()


@delegates(NumpyDatasets.__init__)
class TSDatasets(NumpyDatasets):
    "A dataset that creates tuples from X (and y) and applies `item_tfms`"
    _xtype, _ytype = TSTensor, None # Expected X and y output types (torch.Tensor - default - or subclass)
    def __init__(self, X=None, y=None, items=None, sel_vars=None, sel_steps=None, tfms=None, tls=None, n_inp=None, dl_type=None,
                 inplace=True, **kwargs):
        self.inplace = inplace
        if tls is None:
            X = itemify(to3darray(X), tup_id=0)
            y = itemify(y, tup_id=0) if y is not None else y
            items = tuple((X,)) if y is None else tuple((X,y))
            self.tfms = L(ifnone(tfms,[None]*len(ifnone(tls,items))))
        self.sel_vars = ifnone(sel_vars, slice(None))
        self.sel_steps = ifnone(sel_steps,slice(None))
        self.tls = L(tls if tls else [TfmdLists(item, t, **kwargs) for item,t in zip(items,self.tfms)])
        self.n_inp = (1 if len(self.tls)==1 else len(self.tls)-1) if n_inp is None else n_inp
        if 'split' in kwargs: self.split_idxs = kwargs['split']
        elif 'splits' in kwargs:  self.split_idxs = kwargs['splits']
        else: self.split_idxs = L(np.arange(len(self.tls[0]) if len(self.tls[0]) > 0 else len(self.tls)).tolist())
        if len(self.tls[0]) > 0:
            self.types = L([ifnone(_typ, type(tl[0]) if isinstance(tl[0], torch.Tensor) else tensor) for tl,_typ in zip(self.tls, [self._xtype, self._ytype])])
            self.ptls = L([tl if not self.inplace else tl[:] if type(tl[0]).__name__ == 'memmap' else tensor(stack(tl[:])) for tl in self.tls])

    def __getitem__(self, it):
        return tuple([typ(ptl[it])[...,self.sel_vars, self.sel_steps] if i==0 else typ(ptl[it]) for i,(ptl,typ) in enumerate(zip(self.ptls,self.types))])

    def subset(self, i): return type(self)(tls=L(tl.subset(i) for tl in self.tls), n_inp=self.n_inp, inplace=self.inplace, tfms=self.tfms,
                                           sel_vars=self.sel_vars, sel_steps=self.sel_steps, split=L(self.splits[i]) if self.splits is not None else None)
    @property
    def vars(self):
        if self[0][0].ndim >=4: return self[0][0].shape[-3]
        return self[0][0].shape[-2]
    @property
    def len(self): return self[0][0].shape[-1]


def add_ds(dsets, X, y=None, inplace=True):
    "Create test datasets from X (and y) using validation transforms of `dsets`"
    items = tuple((X,)) if y is None else tuple((X, y))
    with_labels = False if y is None else True
    if isinstance(dsets, (Datasets, NumpyDatasets, TSDatasets)):
        tls = dsets.tls if with_labels else dsets.tls[:dsets.n_inp]
        new_tls = L([tl._new(item, split_idx=1) for tl,item in zip(tls, items)])
        if isinstance(dsets, TSDatasets):
            return TSDatasets(tls=new_tls, n_inp=dsets.n_inp, inplace=inplace, tfms=dsets.tfms,
                              sel_vars=dsets.sel_vars, sel_steps=dsets.sel_steps)
        elif isinstance(dsets, NumpyDatasets):
            return NumpyDatasets(tls=new_tls, n_inp=dsets.n_inp, inplace=inplace, tfms=dsets.tfms)
        elif isinstance(dsets, Datasets): return Datasets(tls=new_tls)
    elif isinstance(dsets, TfmdLists):
        new_tl = dsets._new(items, split_idx=1)
        return new_tl
    else: raise Exception(f"This method requires using the fastai library to assemble your data.Expected a `Datasets` or a `TfmdLists` but got {dsets.__class__.__name__}")

@patch
def add_dataset(self:NumpyDatasets, X, y=None, inplace=True):
    return add_ds(self, X, y=y, inplace=inplace)

@patch
def add_test(self:NumpyDatasets, X, y=None, inplace=True):
    return add_ds(self, X, y=y, inplace=inplace)

@patch
def add_unlabeled(self:NumpyDatasets, X, inplace=True):
    return add_ds(self, X, y=None, inplace=inplace)

def get_subset_dset(dset, idxs):
    if isinstance(dset, TabularPandas):
        new_dset =  dset.iloc[idxs]
        new_dset.items.reset_index(drop=True, inplace=True)
        return new_dset
    items = tuple([L(item)[idxs] for item in dset.items])
    if isinstance(dset, (Datasets, NumpyDatasets, TSDatasets)):
        new_tls = L([tl._new(item, split_idx=dset.split_idx) for tl,item in zip(dset.tls, items)])
        if isinstance(dset, TSDatasets):
            return TSDatasets(tls=new_tls, n_inp=dset.n_inp, inplace=dset.inplace, tfms=dset.tfms, sel_vars=dset.sel_vars, sel_steps=dset.sel_steps)
        elif isinstance(dset, NumpyDatasets):
            return NumpyDatasets(tls=new_tls, n_inp=dset.n_inp, inplace=inplace, tfms=dset.tfms)
        elif isinstance(dset, Datasets): return Datasets(tls=new_tls)
    elif isinstance(dset, TfmdLists):
        return dset._new(items, split_idx=dset.split_idx)
    else: raise Exception(f"Expected a `Datasets`, `TfmdLists` of `TabularPandas` dataset but got {dset.__class__.__name__}")

# Cell
_batch_tfms = ('after_item','before_batch','after_batch')

@delegates(TfmdDL.__init__)
class NumpyDataLoader(TfmdDL):
    idxs = None
    do_item = noops # create batch returns indices
    def __init__(self, dataset, bs=64, shuffle=True, drop_last=True, num_workers=None, verbose=False, do_setup=True, batch_tfms=None, **kwargs):
        '''batch_tfms == after_batch (either can be used)'''
        if num_workers is None: num_workers = min(16, defaults.cpus)
        for nm in _batch_tfms:
            if nm == 'after_batch':
                if batch_tfms is not None: kwargs[nm] = Pipeline(batch_tfms if isinstance(batch_tfms, list) else [batch_tfms])
                else: kwargs[nm] = Pipeline(kwargs.get(nm,None))
            else: kwargs[nm] = Pipeline(kwargs.get(nm,None))
        bs = min(bs, len(dataset))
        super().__init__(dataset, bs=bs, shuffle=shuffle, drop_last=drop_last, num_workers=num_workers, **kwargs)
        if do_setup:
            for nm in _batch_tfms:
                pv(f"Setting up {nm}: {kwargs[nm]}", verbose)
                kwargs[nm].setup(self)

    def create_batch(self, b):
        it = b if self.shuffle else slice(b[0], b[0] + self.bs)
        self.idxs = L(b)
        if hasattr(self, "split_idxs"): self.input_idxs = self.split_idxs[it]
        return self.dataset[it]

    def create_item(self, s): return s

    def get_idxs(self):
        idxs = Inf.count if self.indexed else Inf.nones
        if self.n is not None: idxs = list(range(len(self.dataset)))
        if self.shuffle: idxs = self.shuffle_fn(idxs)
        return idxs

    def unique_batch(self, max_n=9):
        old_bs = self.bs
        self.bs = 1
        old_get_idxs = self.get_idxs
        self.get_idxs = lambda: Inf.zeros
        out_len = len(self.items)
        types = self.dataset.types
        x, y = [], []
        for _ in range(max_n):
            out = self.one_batch()
            if out_len == 2:
                x.extend(out[0])
                y.extend(out[1])
            else:
                x.extend(out)
        b = (types[0](stack(x)), types[1](stack(y))) if out_len == 2 else (types[0](stack(x)), )
        self.bs = old_bs
        self.get_idxs = old_get_idxs
        return b


    @delegates(plt.subplots)
    def show_batch(self, b=None, ctxs=None, max_n=9, nrows=3, ncols=3, figsize=None, unique=False, sharex=True, sharey=False, **kwargs):
        if unique:
            b = self.unique_batch(max_n=max_n)
            sharex, sharey = True, True
        elif b is None: b = self.one_batch()
        db = self.decode_batch(b, max_n=max_n)
        ncols = min(ncols, math.ceil(len(db) / ncols))
        nrows = min(nrows, math.ceil(len(db) / ncols))
        max_n = min(max_n, len(db), nrows*ncols)
        if figsize is None: figsize = (ncols*6, math.ceil(max_n/ncols)*4)
        if ctxs is None: ctxs = get_grid(max_n, nrows=nrows, ncols=ncols, figsize=figsize, sharex=sharex, sharey=sharey, **kwargs)
        for i,ctx in enumerate(ctxs): show_tuple(db[i], ctx=ctx)

    @delegates(plt.subplots)
    def show_results(self, b, preds, ctxs=None, max_n=9, nrows=3, ncols=3, figsize=None, **kwargs):
        t = self.decode_batch(b, max_n=max_n)
        p = self.decode_batch((b[0],preds), max_n=max_n)
        if figsize is None: figsize = (ncols*6, max_n//ncols*4)
        if ctxs is None: ctxs = get_grid(min(len(t), nrows*ncols), nrows=None, ncols=ncols, figsize=figsize, **kwargs)
        for i,ctx in enumerate(ctxs):
            title = f'True: {t[i][1]}\nPred: {p[i][1]}'
            color = 'green' if t[i][1] == p[i][1] else 'red'
            t[i][0].show(ctx=ctx, title=title, title_color=color)

    @delegates(plt.subplots)
    def show_dist(self, figsize=None, **kwargs): self.dataset.show_dist(figsize=figsize, **kwargs)


    @property
    def c(self): return self.dataset.c

    @property
    def d(self): return self.dataset.d

    @property
    def cat(self): return self.dataset.cat

    @property
    def cws(self):
        if self.cat:
            counts = torch.unique(self.ptls[1].detach().cpu().flatten(), return_counts=True, sorted=True)[-1]
            iw = (counts.sum() / counts)
            return (iw / iw.sum()).to(self.device)
        else: return None


@delegates(plt.subplots)
def show_tuple(tup, **kwargs):
    "Display a timeseries plot from a decoded tuple"
    tup[0].show(title='unlabeled' if len(tup) == 1 else str(tup[1]), **kwargs)

class TSDataLoader(NumpyDataLoader):
    @property
    def vars(self):
        b = self.one_batch()
        x = b[0] if isinstance(b, tuple) else b
        if x.ndim >=4: return x.shape[-3]
        return x.shape[-2]
    @property
    def len(self): return self.dataset[0][0].shape[-1]

# Cell
_batch_tfms = ('after_item','before_batch','after_batch')

class NumpyDataLoaders(DataLoaders):
    _xblock = NumpyTensorBlock
    _dl_type = NumpyDataLoader
    def __init__(self, *loaders, path='.', device=None):
        self.loaders, self.path = list(loaders), Path(path)
        self.device = ifnone(device, default_device())

    def new_dl(self, x, y=None):
        if x.ndim == 1: x = [to2d(x)]
        elif x.ndim ==2 and not is_listy(x): x = [x]
        if y is not None and not is_listy(y) and not isinstance(y, (np.ndarray, torch.Tensor)): y = [y]
        return self.valid.new(self.valid.dataset.add_dataset(x, y=y))

    @delegates(plt.subplots)
    def show_dist(self, figsize=None, **kwargs): self.dataset.show_dist(figsize=figsize, **kwargs)

    def decoder(self, o):
        if isinstance(o, tuple): return self.decode(o)
        if o.ndim <= 1: return self.decodes(o)
        else: return L([self.decodes(oi) for oi in o])


    @classmethod
    @delegates(DataLoaders.from_dblock)
    def from_numpy(cls, X, y=None, splitter=None, valid_pct=0.2, seed=0, item_tfms=None, batch_tfms=None, **kwargs):
        "Create timeseries dataloaders from arrays (X and y, unless unlabeled)"
        if splitter is None: splitter = RandomSplitter(valid_pct=valid_pct, seed=seed)
        getters = [ItemGetter(0), ItemGetter(1)] if y is not None else [ItemGetter(0)]
        dblock = DataBlock(blocks=(cls._xblock, CategoryBlock),
                           getters=getters,
                           splitter=splitter,
                           item_tfms=item_tfms,
                           batch_tfms=batch_tfms)

        source = itemify(X) if y is None else itemify(X,y)
        return cls.from_dblock(dblock, source, **kwargs)

    @classmethod
    def from_dsets(cls, *ds, path='.', bs=64, num_workers=None, batch_tfms=None, device=None, shuffle_train=True, **kwargs):
        device = ifnone(device, default_device())
        if batch_tfms is not None and not isinstance(batch_tfms, list): batch_tfms = [batch_tfms]
        default = (shuffle_train,) + (False,) * (len(ds)-1)
        defaults = {'shuffle': default, 'drop_last': default}
        kwargs = merge(defaults, {k: tuplify(v, match=ds) for k,v in kwargs.items()})
        kwargs = [{k: v[i] for k,v in kwargs.items()} for i in range_of(ds)]
        if not is_listy(bs): bs = [bs]
        if len(bs) != len(ds): bs = bs * len(ds)
        loaders = [cls._dl_type(d, bs=b, num_workers=num_workers, batch_tfms=batch_tfms, **k) for d,k,b in zip(ds, kwargs, bs)]
        return cls(*loaders, path=path, device=device)


class TSDataLoaders(NumpyDataLoaders):
    _xblock = TSTensorBlock
    _dl_type = TSDataLoader


def get_ts_dls(X, y=None, splits=None, sel_vars=None, sel_steps=None, tfms=None, inplace=True,
            path='.', bs=64, batch_tfms=None, num_workers=0, device=None, shuffle_train=True, **kwargs):
    dsets = TSDatasets(X, y, splits=splits, sel_vars=sel_vars, sel_steps=sel_steps, tfms=tfms, inplace=inplace, **kwargs)
    dls   = TSDataLoaders.from_dsets(dsets.train, dsets.valid, path=path, bs=bs, batch_tfms=batch_tfms, num_workers=num_workers,
                                     device=device, shuffle_train=shuffle_train, **kwargs)
    return dls

get_tsimage_dls = get_ts_dls

def get_subset_dl(dl, idx):
    subset_dset = get_subset_dset(dl.dataset, idx)
    return dl.new(subset_dset)