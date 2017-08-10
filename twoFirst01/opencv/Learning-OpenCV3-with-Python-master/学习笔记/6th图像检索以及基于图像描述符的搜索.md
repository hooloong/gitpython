# 6th 图像检索以及基于图像描述符的搜索
OpenCV可以检测图像的主要特征，然后提取这些特征，使其成为图像描述符。

6.1 特征检测算法
==========
1. Harris：用于检测角点
2. FAST：角点
3. SIFT：用于检测斑点
4. SURF：斑点
5. BRIEF：斑点
6. ORB：带方向的FAST算法与具有旋转不变性的BRIEF算法
7. 暴力匹配
8. 基于FLANN的匹配法

6.1.1 特征的定义
-----------
特征就是有意义的图像区域，具有独特性和易于识别性，角点和高密度区域是
很好的特征。边缘可以将图像分为两个区域，斑点与周围有很大的区别，是有
意义的特征
### 检测角点
使用cornerHarris来识别角点
``` python
dst = cv2.cornerHarris(gray, 2, 23, 0.04)    #调用cornerHarris函数，
```
第三个参数限定了Sobel算子的中孔，参数定义了角点检测的敏感度，取值介于
3和31之间；第二个参数设定标记记号的大小
### 6.1.2 使用DoG和SIFT进行特征提取与描述
DoG(Difference of Gaussians)对同一图像使用不同的高斯滤波器得到的结果  
SIFT(Scale-Invariant Feature Transform)并不检测关键点，而是通过特征
向量描述关键点周围的区域情况

``` python
sift = cv2.xfeatures2d.SIFT_create()
keypoints, decriptor = sift.detectAndCompute(gray, None)
img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints,
                        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS,
                        color=(51, 163, 236))
```
SIFT对象使用DoG检测关键点，并对关键点周围的区域计算特征向量，这里主要
进行两个操作：*检测和计算*，操作返回*关键点和描述符*。

drawKeypoints函数传入标志值4(cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
代码对图像的每个关键点绘制圆圈和方向

**关键点剖析**
- pt 表示坐标
- size 表示直径
- angle 特征的方向
- response 关键点的强度
- octave 特征所在金字塔层级
- class_id 关键点id

### 使用快速Hessian算法和SURF来提取和检测特征
``` python
def fd(algorithm):
    if algorithm == 'SIFT':
        return cv2.xfeatures2d.SIFT_create()
    if algorithm == 'SURF':
        return cv2.xfeatures2d.SURF_create(float(sys.argv[3]) if
                                           len(sys.argv) == 4 else 4000)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
fd_alg = fd(alg)
keypoints, descriptor = fd_alg.detectAndCompute(gray, None)

img = cv2.drawKeypoints(image=img, outImage=img, keypoints=keypoints, flags=4, color=(51, 163, 236))
```
### 基于ORB的特征检测和特征匹配
