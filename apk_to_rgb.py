
#REF: https://stackoverflow.com/questions/60193896/convert-file-into-grayscale-image
import numpy as np
import zipfile
import hashlib
import cv2
import pathlib
from concurrent.futures import ThreadPoolExecutor
from math import sqrt, ceil

def convert_apk_to_img(input_file, output_location, image_format):
    name = pathlib.Path(input_file).stem
    data = bytearray()
    with zipfile.ZipFile(input_file, 'r') as apkFile:
        for file in sorted(apkFile.namelist()):
            if file.endswith('.dex') or file == 'AndroidManifest.xml' or file == 'resources.arsc':
                data.extend(apkFile.read(file))

    if not output_location.endswith('/'):
        output_location += '/'
    
    type_suffix = '_GrayScale'
    data_len = len(data)
    d = np.frombuffer(data, dtype=np.uint8)
    img_size = int(ceil(sqrt(data_len))) 
    pad_len = img_size * img_size - data_len
    shape = (img_size, img_size)

    if image_format == "RGB":
        type_suffix = '_RGB'
        img_size = ceil(sqrt(ceil(data_len / 3)))
        pad_len = img_size * img_size * 3 - data_len
        shape = (img_size, img_size, 3)

    name += type_suffix
    output_filename = output_location + name + '.png'
    padded_d = np.hstack((d, np.zeros(pad_len, np.uint8)))
    im = np.reshape(padded_d, shape)
    cv2.imwrite(output_filename, im)
    print(f"Lưu ảnh thành công tại {output_filename}")

def convert_apks_to_imgs(input_location, output_location, image_format):
    apkFiles = [] 
    directory = pathlib.Path(input_location)
    for entry in directory.iterdir():
        if entry.is_file() and entry.name.endswith('.apk'):
            apkFiles.append(entry)
    with ThreadPoolExecutor() as pool:
        for file in apkFiles:
            pool.submit(convert_apk_to_img, file, output_location, image_format)
            print("Đang chuyển đổi file:", file)

# Chỉ định thư mục và định dạng
input_location = 'testcode/apk_file'
output_location = 'testcode/output'
image_format = 'RGB'  # hoặc 'RGB'

# Đảm bảo các thư mục tồn tại
pathlib.Path(output_location).mkdir(parents=True, exist_ok=True)

# Chuyển đổi APK thành hình ảnh
convert_apks_to_imgs(input_location, output_location, image_format)

# Hoặc, để chuyển đổi một file đơn lẻ:
convert_apk_to_img('testcode/com.burakkal.simpleiptv.apk', 'testcode/output', 'GrayScale')




