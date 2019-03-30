import re
import zlib
import cv2
import io
from scapy.all import *
from scapy.layers.inet import TCP
from PIL import Image

pictures_directory = "/root/PycharmProjects/BHP3/Chapter4/pictures"
faces_directory = "/home/vagrant/pic_carver/faces"
pcap_file = "arper.pcap"


def face_detect(path, file_name):
    img = cv2.imread(path)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    print("1 ok")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    # highlight the faces in the image
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)

    cv2.imwrite("%s/%s-%s" % (faces_directory, pcap_file, file_name), img)

    return True


def get_http_headers(http_payload):
    headers = None
    try:
        # split the headers off if it is HTTP traffic
        # print(http_payload[:http_payload.index("\r\n\r\n") + 2])
        # print(type(http_payload))
        # print(http_payload)
        # print(http_payload.index("\r\n"))
        headers_raw = http_payload[2:http_payload.index("\\r\\n\\r\\n") + 2]

        # print(headers_raw)
        # break out the headers
        header_list = re.findall(r"(?P<name>.*?): (?P<value>.*?)\\r\\n", headers_raw)
        headers = dict(header_list)
        print(headers)
        # print(type(headers))

    except:
        print("get headers error")
    return headers


def extract_image(headers, http_payload):
    image = None
    image_type = None

    try:
        if "image" in headers["Content-Type"]:
            # grab the image type and image body
            image_type = headers["Content-Type"].split("/")[1]

            image = http_payload[http_payload.index("\\r\\n\\r\\n") + 4:]

            # if we detect compression decompress the image
            try:
                if "Content-Encoding" in headers.keys():
                    if headers["Content-Encoding"] == "gzip":
                        image = zlib.decompress(image, 16 + zlib.MAX_WBITS)
                    elif headers["Content-Encoding"] == "deflate":
                        image = zlib.decompress(image)

            except:
                print("encoding error")
    except:
        print("extract error")

    return image, image_type


def http_assembler(pcap_file):
    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:
        http_payload = ""
        for packet in sessions[session]:
            # print(packet)
            try:
                # print(packet[TCP].dport)
                # if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                # reassemble the stream
                # if packet.haslayer(TCP):
                # print("got a tcp!")
                http_payload += str(packet[TCP].payload)

            except:
                # print("tcp error")
                pass
        # print(http_payload)
        if len(http_payload) > 1:
            headers = get_http_headers(http_payload)

        if headers is None:
            continue

        image, image_type = extract_image(headers, http_payload)

        if image is not None and image_type is not None:
            # store the image
            file_name = "{}-pic_carver_{}.{}".format(pcap_file, carved_images, image_type)


            fd = open("{}/{}".format(pictures_directory, file_name), "wb")

            image_byte = io.BytesIO(image.encode())
            roi_img = Image.open(image_byte)
            img_byte = io.BytesIO()
            roi_img.save(img_byte, format='PNG')
            img_byte = img_byte.getvalue()
            fd.write(img_byte)
            fd.close()

            carved_images += 1

            # now attempt face detection
            try:
                result = face_detect("%s/%s" % (pictures_directory, file_name), file_name)

                if result is True:
                    faces_detected += 1
            except:
                print("detect error")
    return carved_images, faces_detected


carved_images, faces_detected = http_assembler(pcap_file)

print("Extracted: {} images".format(carved_images))
print("Detected: {} faces".format(faces_detected))
