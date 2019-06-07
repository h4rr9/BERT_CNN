from base.base_model import BaseModel
import tensorflow as tf
from utils.metrics import f1_score


class MRPCModel(BaseModel):
    def __init__(self, config):
        super(MRPCModel, self).__init__(config)
        self.build_base_model(max_seq_length=64)
        self.build_model()

    def build_model(self):

        preds = tf.keras.layers.Dense(
            units=1, activation='sigmoid')(self.base_out)

        self.model = tf.keras.models.Model(inputs=self.base_in, outputs=preds)

        self.model.compile(loss='binary_crossentropy',
                           optimizer=self.config.model.optimizer, metrics=['accuracy', f1_score])
