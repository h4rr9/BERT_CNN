from base.base_data_loader import BaseDataLoader, _DATA_PATH
from utils import data
import pandas as pd
import os


class SST2DataLoader(BaseDataLoader):

    def __init__(self, config):
        super(SST2DataLoader, self).__init__(config)

        train = pd.read_csv(os.path.join(
            _DATA_PATH, "SST-2", "train.tsv"), sep="\t")
        val = pd.read_csv(os.path.join(
            _DATA_PATH, "SST-2", "dev.tsv"), sep="\t")
        test = pd.read_csv(os.path.join(
            _DATA_PATH, "SST-2", "test.tsv"), sep="\t")

        train_examples = data.convert_text_to_example(train['sentence'].values)
        self.train_labels = data.process_label(train['label'].values)
        self.n_train = train.shape[0]

        val_examples = data.convert_text_to_example(val['sentence'].values)
        self.val_labels = data.process_label(val['label'].values)
        self.n_val = val.shape[0]

        test_examples = data.convert_text_to_example(test['sentence'].values)
        self.n_test = test.shape[0]

        tokenizer = data.create_tokenizer()

        self.train_dataset = data.convert_examples_to_features(
            tokenizer, train_examples, max_seq_length=64)
        self.val_dataset = data.convert_examples_to_features(
            tokenizer, val_examples, max_seq_length=64)
        self.test_dataset = data.convert_examples_to_features(
            tokenizer, test_examples, max_seq_length=64)

    def get_train_data(self):
        return self.train_dataset

    def get_train_label(self):
        return self.train_labels

    def get_val_data(self):
        return self.val_dataset

    def get_val_label(self):
        return self.val_labels

    def get_test_data(self):
        return self.test_dataset

    def get_train_count(self):
        return self.n_train

    def get_val_count(self):
        return self.n_val

    def get_test_count(self):
        return self.n_test
