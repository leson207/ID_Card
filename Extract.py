import tensorflow as tf
import cv2
from PIL import Image
import numpy as np

from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

from Crop_DL import load_labels_map, process_output

config = Cfg.load_config_from_name('vgg_transformer')
config['weights'] = 'transformerocr.pth'
config['cnn']['pretrained'] = False
config['device'] = 'cpu'
config['predictor']['beamsearch'] = False
detector = Predictor(config)

#######################################################################################################

model2 = tf.saved_model.load("info/saved_model")
label_maps = load_labels_map('label_map_1.pbtxt')

image_path = "crop.jpg"

detect_fn = model2.signatures['serving_default']
img = cv2.imread(image_path)
img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
input_tensor = tf.convert_to_tensor(img)
input_tensor = input_tensor[tf.newaxis, ...]
results = detect_fn(input_tensor)

targetSize = {'w': 0, 'h': 0}
targetSize['h'] = img.shape[0]
targetSize['w'] = img.shape[1]

output = process_output('text', results, 0.5, targetSize, label_maps)
img = cv2.imread(image_path)
results_str = ""

#####id
arr = np.array(output['id'])
ima = img[int(arr[0][1]):int(arr[0][3]), int(arr[0][0]):int(arr[0][2])]
cv2.imwrite('test_id.jpg', ima)
ima = 'test_id.jpg'
ima = Image.open(ima)
s = "id: " + detector.predict(ima)
results_str = results_str + s + "\n"

#####name
arr = np.array(output['name'])
arr = sorted(arr, key=lambda x: [x[0]])
arr = np.array(arr)
leng = arr.shape[0]
s1 = "name: "
for i in range(0, leng):
    ima = img[int(arr[i][1]):int(arr[i][3]), int(arr[i][0]):int(arr[i][2])]
    cv2.imwrite('test_name' + str(i + 1) + '.jpg', ima)
    path = 'test_name' + str(i + 1) + '.jpg'
    ima = Image.open(path)
    s = detector.predict(ima)
    s1 = s1 + s + " "
results_str = results_str + s1 + "\n"

#####dob
arr = np.array(output['dob'])
ima = img[int(arr[0][1]):int(arr[0][3]), int(arr[0][0]):int(arr[0][2])]
cv2.imwrite('test_dob.jpg', ima)
ima = 'test_dob.jpg'
ima = Image.open(ima)
s = "dob: " + detector.predict(ima)
results_str = results_str + s + "\n"

#####sex
arr = np.array(output['sex'])
ima = img[int(arr[0][1]):int(arr[0][3]), int(arr[0][0]):int(arr[0][2])]
cv2.imwrite('test_sex.jpg', ima)
ima = 'test_sex.jpg'
ima = Image.open(ima)
s = "sex: " + detector.predict(ima)
results_str = results_str + s + "\n"

####date
arr = np.array(output['date'])
ima = img[int(arr[0][1]):int(arr[0][3]), int(arr[0][0]):int(arr[0][2])]
cv2.imwrite('test_date.jpg', ima)
ima = 'test_date.jpg'
ima = Image.open(ima)
s = "date: " + detector.predict(ima)
results_str = results_str + s + "\n"

####nati
arr = np.array(output['nati'])
ima = img[int(arr[0][1]):int(arr[0][3]), int(arr[0][0]):int(arr[0][2])]
cv2.imwrite('test_nati.jpg', ima)
ima = 'test_nati.jpg'
ima = Image.open(ima)
s = "nati: " + detector.predict(ima)
results_str = results_str + s + "\n"

#####res
arr = np.array(output['pla'])
arr = sorted(arr, key=lambda x: [x[0]])
arr = np.array(arr)
leng = arr.shape[0]
s1 = "pla: "
for i in range(0, leng):
    ima = img[int(arr[i][1]):int(arr[i][3]), int(arr[i][0]):int(arr[i][2])]
    cv2.imwrite('test_pla' + str(i + 1) + '.jpg', ima)
    path = 'test_pla' + str(i + 1) + '.jpg'
    ima = Image.open(path)
    s = detector.predict(ima)
    s1 = s1 + s + " "
results_str = results_str + s1 + "\n"

####res
arr = np.array(output['res'])
leng = arr.shape[0]
arr = sorted(arr, key=lambda x: [x[1]])
arr = np.array(arr)
Max = arr[leng - 1][1]
boxes = []
i = 0
count = 0
s1 = "res: "
while i < leng - count:
    if (Max - arr[i][1] >= 4):
        boxes.append([arr[i][0], arr[i][1], arr[i][2], arr[i][3]])
        arr = np.delete(arr, (i), axis=0)
        count += 1
    i += 1

boxes = np.array(boxes)
leng = boxes.shape[0]

for i in range(0, leng):
    ima = img[int(boxes[i][1]):int(boxes[i][3]), int(boxes[i][0]):int(boxes[i][2])]
    cv2.imwrite('test_res' + str(i + 1) + '.jpg', ima)
    path = 'test_res' + str(i + 1) + '.jpg'
    ima = Image.open(path)
    s = detector.predict(ima)
    s1 = s1 + s + " "

arr = sorted(arr, key=lambda x: [x[0]])
arr = np.array(arr)
i = leng
leng = arr.shape[0]

for j in range(0, leng):
    ima = img[int(arr[j][1]):int(arr[j][3]), int(arr[j][0]):int(arr[j][2])]
    cv2.imwrite('test_res' + str(j + i + 1) + '.jpg', ima)
    path = 'test_res' + str(j + i + 1) + '.jpg'
    ima = Image.open(path)
    s = detector.predict(ima)
    s1 = s1 + s + " "
results_str = results_str + s1 + "\n"

print(results_str)
