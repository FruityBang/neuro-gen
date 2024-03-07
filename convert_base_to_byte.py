import base64
import sys
import os
import cv2
import numpy


#base64image = open('image.png', 'r').read()
#byteimage = base64.b64decode(base64image)
#bytefile = open('byteimage.png', 'wb')
#bytefile.write(byteimage)

bytefile = open('byteimage.png', 'rb').read()
#bytef = "byteimage.png"
#
#back = base64.b64encode(bytefile).decode('utf-8')
#
#base64image2 = open('image2.png', 'w')
#base64image2.write(back)

#f = 'iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAAGUlEQVR4nGIRb3jNgA0wYRUdtBKAAAAA//8zJwGVxBUAfAAAAABJRU5ErkJggg=='
#b = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x08\x00\x00\x00\x08\x08\x02\x00\x00\x00Km)\xdc\x00\x00\x00\x19IDATx\x9cb\x11ox\xcd\x80\r0a\x15\x1d\xb4\x12\x80\x00\x00\x00\xff\xff3'\x01\x95\xc4\x15\x00|\x00\x00\x00\x00IEND\xaeB`\x82"

print('{:.2f}'.format(sys.getsizeof(bytefile) / 1024))

image = numpy.frombuffer(bytefile, numpy.uint8)
image_next = cv2.imdecode(image, cv2.IMREAD_COLOR)
print('{:.2f}'.format(sys.getsizeof(image_next) / 1024))

encode_params = [int(cv2.IMWRITE_JPEG_QUALITY), 1]

rest, image_pre_final = cv2.imencode('.png', image_next, encode_params)
image_final = image_pre_final.tobytes()

print('{:.2f}'.format(sys.getsizeof(image_final) / 1024))

