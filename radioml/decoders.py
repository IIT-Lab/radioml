import numpy as np
from tensorflow.keras.models import load_model
from commpy.channelcoding import viterbi_decode

class Decoder(object):
    def __init__(self):
        pass
    def decode(self, inputs):
        pass

class ViterbiDecoder(Decoder):
    def __init__(self, trellis, tb_depth=15, decoding_type='hard'):
        super(ViterbiDecoder, self).__init__()
        self.trellis = trellis
        self.tb_depth = tb_depth
        self.decoding_type= decoding_type
    
    def decode(self, inputs):
        return viterbi_decode(inputs, self.trellis, self.tb_depth, self.decoding_type)


class NeuralDecoder(Decoder):
    def __init__(self, model_path, block_length):
        super(NeuralDecoder, self).__init__()
        self.model = load_model(model_path, compile=False)
        self.block_length = block_length

    def decode(self, inputs):
        predictions =  self.model.predict(self._preprocess_fn(inputs))
        return  np.squeeze(predictions, -1).round()
    
    def _preprocess_fn(self, inputs):
        outputs = inputs.reshape((-1, 2))[:self.block_length, :]
        return np.expand_dims(outputs, 0) if outputs.ndim == 2 else outputs