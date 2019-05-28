from base.base_data_loader import BaseDataLoader, _DATA_PATH
from utils import data
import pandas as pd
import os


class QNLIDataLoader(BaseDataLoader):

    def __init__(self, config):
        super(QNLIDataLoader, self).__init__(config)

        train = pd.read_csv(os.path.join(
            _DATA_PATH, "QNLI", "train.tsv"), sep="\t")
        val = pd.read_csv(os.path.join(
            _DATA_PATH, "QNLI", "dev.tsv"), sep="\t")
        test = pd.read_csv(os.path.join(
            _DATA_PATH, "QNLI", "test.tsv"), sep="\t")

        train['sentences'] = train['question'] + ' ||| ' + train['sentence']
        test['sentences'] = test['question'] + ' ||| ' + test['sentence']
        val['sentences'] = val['question'] + ' ||| ' + val['sentence']

        train_examples = data.convert_text_to_example(train['sentences'].values)
        train_labels = train['label'].values
        self.n_train = train.shape[0]

        val_examples = data.convert_text_to_example(val['sentences'].values)
        val_labels = val['label'].values
        self.n_val = val.shape[0]

        test_examples = data.convert_text_to_example(test['sentences'].values)
        self.n_test = test.shape[0]

        tokenizer = data.create_tokenizer()

        train_features = data.convert_examples_to_features(
            tokenizer, train_examples, max_seq_length=128)
        val_features = data.convert_examples_to_features(
            tokenizer, val_examples, max_seq_length=128)
        test_features = data.convert_examples_to_features(
            tokenizer, test_examples, max_seq_length=128)

        self.train_dataset = data.create_dataset(
            train_features, train_labels, batch_size=self.batch_size, is_training=True)
        self.val_dataset = data.create_dataset(
            val_features, val_labels, batch_size=self.batch_size, is_training=False)
        self.test_dataset = data.create_dataset(
            test_features, batch_size=self.batch_size, is_training=False)

    def get_train_data(self):
        return self.train_dataset

    def get_val_data(self):
        return self.val_dataset

    def get_test_data(self):
        return self.test_dataset

    def get_train_count(self):
        return self.n_train

    def get_val_count(self):
        return self.n_val

    def get_test_count(self):
        return self.n_test
