import tensorflow as tf

graph_def_file = "C:/Users/patyc/Documents/GitHub/trekking/trekking-nn/testing/inference_graphs/ssd_mobilenet_v1_coco_melfm/frozen_inference_graph.pb"
input_arrays = ["input"]
output_arrays = ["MobilenetV1/Predictions/Softmax"]

converter = tf.lite.TFLiteConverter.from_frozen_graph(
  graph_def_file, input_arrays, output_arrays)
tflite_model = converter.convert()
open("converted_model.tflite", "wb").write(tflite_model)