# Road Accident Detection From Surveillance Videos 
BKU Team 2018

An implementation and a modified version of **Real-world Anomaly Detection in Surveillance Videos** ([Sultani, Waqas and Chen][realworld]) on **Road_Accident dataset**.
![videos](/WebApp/staticfiles/images/roadaccident.png)

![demo](/WebApp/media/gifs/demo.gif)
## Dataset

Road accident dataset consists of 796 videos under *.mp4 format (330 normal, 366 abnormal, 100 testing). 
  - Dataset link: updating
  - C3D Extractor: **Learning Spatiotemporal Features with 3D Convolutional Networks** ([Du Tran et al.][c3d]).
  - Extract C3D feature of video using Google Colab ([this jupyter notebook](https://github.com/dolongbien/HumanBehaviorBKU/blob/master/C3D/C3DV0.ipynb))

Follow the instruction in the notebook to extract video feature. 

## Training

Check this notebook [Train_Test_Code](https://github.com/dolongbien/HumanBehaviorBKU/blob/master/TrainTest_Code.ipynb) to see the documentation as well as training/testing process.
* Keras 1.1.0
* Theano 0.9.0
* Python 3

## Visualize the results

Django web application. See [WebApp](https://github.com/dolongbien/HumanBehaviorBKU/tree/master/WebApp) directory for more details.

### File structure

| File/Directory | Decscription |
| ------ | ------ |
| [C3D][c3dfolder] | Extract C3D video feature |
| [Scripts][scripts] |Python, Matlab ultility scripts |
| [Temporal Annotation][annotation] | Groudtruth annotation of testing videos |
| [Makefile.config][makefile] |Configuration file to build C3D Caffe model|
| [Train/Test Code][traintestcode] | Jupyter notebook for Traning/Testing process |

If you find any bug, or have some questions, feel free to contact any of these: Bien Do (dolongbien1205@gmail.com), Hoai Do (1511093@hcmut.edu.vn), Dat Nguyen (1510700@hcmut.edu.vn).

## References

[1] W. Sultani, C. Chen, and M. Shah, “Real-world anomaly detection in surveillance videos,” in The IEEE Conference on
Computer Vision and Pattern Recognition (CVPR), Jun. 2018.

[2] D. Tran, L. Bourdev, R. Fergus, et al., “Learning spatiotemporal features with 3d convolutional networks,” in The IEEE
International Conference on Computer Vision (ICCV), Dec. 2015 .



   [realworld]: <https://arxiv.org/pdf/1801.04264.pdf>
   [c3d]: <https://arxiv.org/pdf/1412.0767.pdf>
   [c3dfolder]: <https://github.com/dolongbien/HumanBehaviorBKU/tree/master/C3D>
   [scripts]: <https://github.com/dolongbien/HumanBehaviorBKU/tree/master/Scripts>
   [annotation]: <https://github.com/dolongbien/HumanBehaviorBKU/tree/master/Temporal_Annotations>
   [makefile]: <https://github.com/dolongbien/HumanBehaviorBKU/blob/master/Makefile.config>
   [traintestcode]: <https://github.com/markdown-it/markdown-it>
