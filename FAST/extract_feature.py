# -*- coding: utf-8 -*-
import numpy as np
import cv2
import sys
import pdb

def circle16(i, j):
    return [(i-3, j), (i-3, j+1), (i-2, j+2), (i-1, j+3), 
            # 5
            (i, j+3), (i+1, j+3), (i+2, j+2), (i+3, j+1),
            # 9
            (i+3, j), (i+3, j-1), (i+2, j-2), (i+1, j-2),
            # 13
            (i, j-3), (i-1, j-3), (i-2, j-2), (i-3, j-1)]

def save(filepath, pi):
    import pickle
    f = open(filepath, 'wb')
    pickle.dump(pi, f)
    f.close()

def FAST(pi_list, center, delta):
    pi_len    = len(pi_list)
    diff      = []

    for i in range(pi_len):
        if int(pi_list[i]) - center > delta:
            diff.append(1)
        elif int(pi_list[i]) - center < -delta:
            diff.append(-1)
        else:
            diff.append(0)

    # 快速测试 
    if abs(diff[0] + diff[4] + diff[8] + diff[12]) < 3:
        # 如果上下左右的和的绝对值小于3，一定不存在连续的12个点同时比中心点更暗或者更亮
        return False
    
    # 由于是环形，拷贝一份，看有没有连续的值
    diff.extend(diff[:])
    repeat = 0
    for i in range(len(diff)):
        if repeat >= 12:
            return True
        elif diff[i] == diff[i-1] and diff[i] != 0:
            repeat = repeat+1
        else:
            repeat = 0
    return False 

def main():
    if len(sys.argv) < 5:
        sys.exit('usage: python extract_feature.py (filename) (delta) (output_image_path) (output_feature_file)')
    m = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    draw = cv2.imread(sys.argv[1])
    if len(m) == 0:
        sys.exit('image not exist!')

    delta = int(sys.argv[2])
    shape = m.shape

    train_data = []
    for i in range(3, shape[0] - 3):
        for j in range(3, shape[1] - 3):
            # go read FAST algorithm test
            pi_list = [m[x][y] for (x, y) in circle16(i, j)]
            if FAST(pi_list, m[i][j], delta):
                pi_list.append(True)
                cv2.circle(draw, (j, i), 4, (0, 255, 255), 2)
            else:
                pi_list.append(False)

            train_data.append(pi_list)
    cv2.imwrite(sys.argv[3], draw)
    save(sys.argv[4], train_data)

if __name__ == '__main__':
    main()
