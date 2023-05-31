# Retrival information form Vietnamese ID-Card
- link model detect corner : https://drive.google.com/drive/folders/1dDYQSWxR0BCAAebrdT4hqnNii4nYbIxT?usp=share_link
- link model detect info : https://drive.google.com/drive/folders/1dr5jj1dG-NKT3y4Zpax9SrcGf9QNXAr1?usp=share_link
- Problem: From a picture of an id-Card, extract its infomation
- Project contain 2 part:
  - Crop and detect: Crop a smaller image that contain all the ID_Card from the input image and detect region of infomation from croped image, 
    - Using Image Procesing(Crop_DIP): Aplly SIFT and RANSAC argorithm on input image and template image then detect by mapping cordinate.
    - Using DeepLearning(Crop_DL): Build DL model for both crop and detect task.
    - FOR THE SAKE OF PERSONAL INFOMATION SECURITY, THERE NO EXAMPLE IMAGE HERE
  - Extract infomation: extract information from detected area using DL
 
![image](https://github.com/leson207/ID_Card/assets/74070396/49c1b522-f427-4c9a-ba07-081118aff8f5)
![image](https://github.com/leson207/ID_Card/assets/74070396/a38d38ba-a4b5-40e9-a583-5bb5f32310ec)
![image](https://github.com/leson207/ID_Card/assets/74070396/78aba734-6dce-42dd-90b2-c158a6fdaf59)
![image](https://github.com/leson207/ID_Card/assets/74070396/bfe0231e-8864-4d4f-8783-97b158185def)
.............
