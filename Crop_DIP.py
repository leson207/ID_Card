import matplotlib.pyplot as plt
import numpy as np
import cv2

rgb_l = cv2.cvtColor(cv2.imread("cccd.jpg"), cv2.COLOR_BGR2RGB)
gray_l = cv2.cvtColor(rgb_l, cv2.COLOR_RGB2GRAY)
rgb_r = cv2.cvtColor(cv2.imread("template.png"), cv2.COLOR_BGR2RGB)
gray_r = cv2.cvtColor(rgb_r, cv2.COLOR_RGB2GRAY)

feature_extractor = cv2.SIFT_create()
kp_l, desc_l = feature_extractor.detectAndCompute(gray_l, None)
kp_r, desc_r = feature_extractor.detectAndCompute(gray_r, None)
test = cv2.drawKeypoints(rgb_l, kp_l, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

bf = cv2.BFMatcher()
matches = bf.knnMatch(desc_l, desc_r, k=2)

good_and_second_good_match_list = []
for m in matches:
    if m[0].distance / m[1].distance < 0.5:
        good_and_second_good_match_list.append(m)
good_match_arr = np.asarray(good_and_second_good_match_list)[:, 0]

im_matches = cv2.drawMatchesKnn(rgb_l, kp_l, rgb_r, kp_r,
                                good_and_second_good_match_list[0:30], None,
                                flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

good_kp_l = np.array([kp_l[m.queryIdx].pt for m in good_match_arr])
good_kp_r = np.array([kp_r[m.trainIdx].pt for m in good_match_arr])
H, masked = cv2.findHomography(good_kp_r, good_kp_l, cv2.RANSAC, 5.0)

h2, w2 = rgb_r.shape[:2]
corners = np.float32([[0, 0], [w2, 0], [w2, h2], [0, h2]]).reshape(-1, 1, 2)
matched_corners = cv2.perspectiveTransform(corners, H)

pts2_ = abs(matched_corners)
[x_min, y_min] = np.int32(matched_corners.min(axis=0).ravel() - 0.5)
[x_max, y_max] = np.int32(matched_corners.max(axis=0).ravel() + 0.5)
print(x_min, x_max, y_min, y_max)

cropped_img = rgb_l[y_min:y_max, x_min:x_max]

crop_corners = np.float32([[x_min, y_min], [x_max, y_min], [x_max, y_max], [x_min, y_max]]).reshape(-1, 1, 2)

corner_id = -1
dist = 100000
for i in range(0, 4):
    if np.linalg.norm(crop_corners[i] - matched_corners[0]) < dist:
        dist = np.linalg.norm(crop_corners[i] - matched_corners[0])
        corner_id = i
for i in range(4 - corner_id):
    cropped_img = cv2.rotate(cropped_img, cv2.ROTATE_90_CLOCKWISE)
    crop_corners = [crop_corners[-1]] + crop_corners[:-1]

plt.imshow(cropped_img)
plt.show()

cropped_img = cv2.cvtColor(np.array(cropped_img), cv2.COLOR_BGR2RGB)
cv2.imwrite("crop.jpg", cropped_img)
