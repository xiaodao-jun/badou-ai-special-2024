import cv2
import numpy as np

def drawMatchesKnn_cv2(img1_gray,kp1,img2_gray,kp2,goodMctch):
    h1,w1 = img1_gray.shape[:2]
    h2,w2 = img2_gray.shape[:2]

    vis = np.zeros((max(h1,h2), w1 + w2, 3), np.uint8)
    vis[:h1, :w1] = img1_gray
    vis[:h2, w1:w1+w2] = img2_gray

    p1 = [kpp.queryIdx for kpp in goodMctch]
    p2 = [kpp.trainIdx for kpp in goodMctch]

    post1 = np.int32([kp1[pp].pt for pp in p1])
    post2 = np.int32([kp2[pp].pt for pp in p2]) + (w1, 0)

    for (x1, y1),(x2, y2) in zip(post1, post2):
        cv2.line(vis, (x1,y1), (x2,y2), (0,0,255))

    cv2.namedWindow("match",cv2.WINDOW_NORMAL)
    cv2.imshow("match", vis)

img1_gray = cv2.imread("iphone1.png")
img2_gray = cv2.imread("iphone2.png")

# sift = cv2.SIFT()
# 定义匹配规则
sift = cv2.xfeatures2d.SIFT_create()
# sift = cv2.SURF()

kp1, des1 = sift.detectAndCompute(img1_gray,None)
kp2, des2 = sift.detectAndCompute(img2_gray,None)

# BFmatcher with default parms
bf = cv2.BFMatcher(cv2.NORM_L2)   # NORM_L2 欧式距离匹配
# opencv中，knn是一种蛮力匹配，将待匹配图片的特征与目标图中的全部特征全量遍历，找出相似最高的前K个
matches = bf.knnMatch(des1, des2, k=2)

goodMatch = []
for m,n in matches:
    if m.distance < 0.5*n.distance:
        goodMatch.append(m)

# 执行函数
drawMatchesKnn_cv2(img1_gray,kp1,img2_gray,kp2,goodMatch[:5000])   # 前20

cv2.waitKey(0)
cv2.destroyAllWindows()