import numpy as np

hsv_map = np.zeros((180, 256, 3), np.uint8)

h, s = np.indices(hsv_map.shape[:2])

hsv_map[:, :, 0] = h
hsv_map[:, :, 1] = s
hsv_map[:, :, 2] = 255
print h

print  s