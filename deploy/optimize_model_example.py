import os

import tensorflow as tf

saved_model_dir = os.path.abspath(os.path.join(os.getcwd(),
                                            "train/model_output/fandom/model_v001"))
converter = tf.lite.TFLiteConverter.from_saved_model(
    saved_model_dir)

converter.optimizations = [
    tf.lite.Optimize.DEFAULT
    # tf.lite.Optimize.OPTIMIZE_FOR_LATENCY,
   # tf.lite.Optimize.OPTIMIZE_FOR_SIZE
]
tflite_model = converter.convert()


saved_lite_model_dir = os.path.abspath(os.path.join(os.getcwd(),
                                            "train/model_output/fandom/model_v001.tflite"))
with open(saved_lite_model_dir, "wb") as f:
    f.write(tflite_model)