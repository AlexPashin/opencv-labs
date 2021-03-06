# Лабораторная работа № 2. Захват видео в библиотеке OpenCV.
#
# 1 При помощи функций библиотеки OpenCV захватить видеопоток с камеры устройства.
#
# 2. Осуществить запись видеопотока длиной 10 секунд в файл.
#
# 3. Применить операцию инвертирования (перемена каналов или замена на комплиментарные цвета: черный – белый,
# желтый – синий и т.д.) цветов к произвольному кадру из файла видео, а также непосредственно из видеопотока (
# отобразить захватываемый видеопоток в искаженных цветах).
#
# 4. Сохранить полученные изображения.
#
# 5. Вывести на экран полученные изображения, а также их представления по слоям (каналам).
#
# 6. Сформировать изображение из 9 слоев (или из разных 9 изображений в градациях серого).
#
# 7. Сохранить изображение.
#
# 8. Написать краткий отчет по проделанной работе с использованием Jupiter notebook

import cv2
import time
import numpy as np


def record_video(filename, duration):
    cv2.namedWindow("Recording...")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Cam is not available")
        return
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = 10
    image_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"XVID"), fps, image_size)

    i = 0
    while i < duration * fps:
        ret, frame = cap.read()
        r, g, b = cv2.split(frame)
        new_frame = cv2.merge((g, b, r))
        cv2.imshow("Recording...", new_frame)
        out.write(frame)
        time.sleep(1 / fps)
        i = i + 1
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyWindow("Recording...")
    cv2.imwrite(".\\..\\assets\\shot.jpg", new_frame)
    cv2.imshow("Shot", new_frame)
    cv2.waitKey(0)

    # b, g, r = cv2.split(new_frame)
    # rgb = np.concatenate((new_frame, cv2.merge((r, r, r))), axis=1)
    # rgb1 = np.concatenate((cv2.merge((g, g, g)), cv2.merge((b, b, b))), axis=1)
    # rgb = np.concatenate((rgb, rgb1), axis=0)
    # cv2.imwrite("orig_r_g_b.jpg", rgb)
    # cv2.imshow("Orig/Red/Green/Blue", rgb)
    # cv2.waitKey(0)
    b, g, r = cv2.split(new_frame)
    b1 = np.zeros(np.shape(new_frame), np.uint8)
    b1[:, :, 0] = b
    g1 = np.zeros(np.shape(new_frame), np.uint8)
    g1[:, :, 1] = g
    r1 = np.zeros(np.shape(new_frame), np.uint8)
    r1[:, :, 2] = r
    rgb = np.concatenate((new_frame, r1), axis=1)
    rgb1 = np.concatenate((g1, b1), axis=1)
    rgb = np.concatenate((rgb, rgb1), axis=0)
    cv2.imwrite(".\\..\\assets\\orig_r_g_b.jpg", rgb)
    cv2.imshow("Orig/Red/Green/Blue", rgb)
    cv2.waitKey(0)

    b, g, r = cv2.split(new_frame)
    img = cv2.merge((r, r, r)) + cv2.merge((b, b, b)) + cv2.merge((g, g, g)) + new_frame + r1 + g1 + b1 + r1 + new_frame
    cv2.imwrite(".\\..\\assets\\chaos.jpg", img)
    cv2.imshow("Chaos", img)
    cv2.waitKey(0)


record_video(".\\..\\assets\\record.avi", 10)
