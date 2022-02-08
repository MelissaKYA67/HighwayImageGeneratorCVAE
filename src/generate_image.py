import os
import sys
import torch
import re
import cv2
import os, shutil
from src.CVAE import cVAE
from matplotlib import pyplot as plt


module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

net = cVAE((3, 192, 256), nclass=21, nhid=16, ncond=32)
checkpoint = torch.load("/home/guest/FYP/notebook/cVAE.pt", map_location=device)
net.load_state_dict(checkpoint["net"])
net.to(device)
net.eval()
print(net)


def sorted_alphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
    return sorted(data, key=alphanum_key)


def gen_img(label):
    with torch.no_grad():
        x = net.generate(label)
    plt.imshow(x.squeeze(0).cpu().numpy().transpose(1, 2, 0))
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('img.jpg', bbox_inches='tight', pad_inches=0)


def gen_img2(label, name):
    with torch.no_grad():
        x = net.generate(label)
    plt.imshow(x.squeeze(0).cpu().numpy().transpose(1, 2, 0))
    plt.axis('off')
    plt.tight_layout()
    plt.savefig("/home/guest/FYP/UI/videoimages/" + str(name) + ".jpg", bbox_inches='tight', pad_inches=0)


def delete_imgs():
    folder = "/home/guest/FYP/UI/videoimages"
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Fail to delete %s. Reason: %s' % (file_path, e))


def gen_vid(label, numimg, fps):
    for i in range(numimg):
        gen_img2(label, i)

    img_array = []
    path = "/home/guest/FYP/UI/videoimages"
    imgs = sorted_alphanumeric(os.listdir(path))

    for img_name in imgs:
        img = cv2.imread(path + "/" + img_name)
        height, width, channels = img.shape
        size = (width, height)
        img_array.append(img)

    out = cv2.VideoWriter("video.avi", cv2.VideoWriter_fourcc(*'DIVX'), fps, size)

    for m in range(len(img_array)):
        out.write(img_array[m])

    out.release()



