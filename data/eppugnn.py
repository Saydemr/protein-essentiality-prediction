import os.path as osp
import os
from typing import Callable, Optional

import torch
import numpy as np
from sklearn.model_selection import ShuffleSplit
from typing import Tuple

from torch_geometric.data import InMemoryDataset, download_url
from torch_geometric.io import read_npz


class Eppugnn(InMemoryDataset):
    url = 'https://github.com/Saydemr/EPPuGNN/raw/main/data/'
    splits_url = 'https://github.com/Saydemr/EPPuGNN/raw/main/splits/'

    def __init__(self, root: str, name: str,
                 custom_split: Tuple[float, float] = None,
                 split_no : int = 0,
                 transform: Optional[Callable] = None,
                 pre_transform: Optional[Callable] = None):
        self.name = name.lower()
        self.custom_split = custom_split
        self.split_no = split_no
        assert self.name in ['dm', 'mm', 'hs', 'sc']
        super().__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])


    @property
    def raw_dir(self) -> str:
        return osp.join(self.root, self.name, 'raw')

    @property
    def processed_dir(self) -> str:
        return osp.join(self.root, self.name, 'processed')

    @property
    def raw_file_names(self) -> str:
        return f'{self.name.lower()}-data.npz'

    @property
    def processed_file_names(self) -> str:
        return 'data.pt'

    def download(self):
        download_url(self.url + self.raw_file_names, self.raw_dir)
        if self.custom_split is None:
            for i in range(1):
                download_url(self.splits_url + "eppugnn_splits_" + self.name + "_0.6_0.2_"+ str(i) + ".npz", self.raw_dir)


    def process(self):
        data = read_npz(self.raw_paths[0])
        if self.custom_split is not None:
            labels = data.y
            train_percentage, val_percentage = self.custom_split
            second_split_percentage = train_percentage / (train_percentage + val_percentage)

            train_and_val_index, test_index = next(ShuffleSplit(n_splits=1, train_size=train_percentage + val_percentage).split(np.empty_like(labels), labels))
            test_mask = np.zeros_like(labels)
            test_mask[test_index] = 1

            train_index, val_index = next(ShuffleSplit(n_splits=1, train_size=second_split_percentage).split(np.empty_like(labels[train_and_val_index]), labels[train_and_val_index]))
            train_index = train_and_val_index[train_index]
            val_index = train_and_val_index[val_index]
            train_mask = np.zeros_like(labels)
            train_mask[train_index] = 1
            val_mask = np.zeros_like(labels)
            val_mask[val_index] = 1

            data.train_mask = torch.from_numpy(train_mask).to(torch.bool)
            data.val_mask = torch.from_numpy(val_mask).to(torch.bool)
            data.test_mask = torch.from_numpy(test_mask).to(torch.bool)

            np.savez(f"{self.raw_dir}/eppugnn_splits_{self.name}_{train_percentage}_{val_percentage}_custom.npz", train_mask=train_mask, val_mask=val_mask, test_mask=test_mask)

        else:
            split = np.load(self.raw_dir + "/eppugnn_splits_" + self.name + "_0.6_0.2_"+ str(self.split_no) + ".npz")
            data.train_mask = torch.tensor(split['train_mask']).to(torch.bool)
            data.val_mask = torch.tensor(split['val_mask']).to(torch.bool)
            data.test_mask = torch.tensor(split['test_mask']).to(torch.bool)
            print("Split loaded")
            print("Train: ", data.train_mask.sum().item())
            print("Val: ", data.val_mask.sum().item())
            print("Test: ", data.test_mask.sum().item())

        data = data if self.pre_transform is None else self.pre_transform(data)
        torch.save(self.collate([data]), self.processed_paths[0])

    def update_split(self, split_no):
        self.split_no = split_no
        self.process()
        

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}-{self.name.upper()}'
