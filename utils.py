import cv2
import numpy as np
import skimage.exposure
import requests
import os
from PIL import Image
import random
def characterNames(man_count, woman_count):
    man_names = ["James", "John", "Michael", "David", "Robert", "William", "Richard", "Charles", "Joseph", "Thomas", "Daniel", "Christopher", "Matthew", "Anthony", "Mark", "Donald", "George", "Kenneth", "Steven", "Edward", "Brian", "Ronald", "Kevin", "Jason", "Jeffrey", "Timothy", "Paul", "Larry", "Gregory", "Frank", "Scott", "Eric", "Stephen", "Andrew", "Dennis", "Peter", "Gary", "Ryan", "Terry", "Jose", "Russell", "Bruce", "Alan", "Gerald", "Henry", "Samuel", "Lawrence", "Douglas", "Carl", "Willie"]
    woman_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen", "Nancy", "Lisa", "Betty", "Dorothy", "Sandra", "Ashley", "Kimberly", "Donna", "Emily", "Michelle", "Carol", "Amanda", "Melissa", "Deborah", "Stephanie", "Rebecca", "Laura", "Sharon", "Cynthia", "Kathleen", "Amy", "Shirley", "Angela", "Helen", "Anna", "Brenda", "Pamela", "Nicole", "Ruth", "Katherine", "Samantha", "Christine", "Evelyn", "Maria", "Diane", "Frances", "Joyce", "Julie", "Janet", "Grace"]
    man = man_names[:man_count]
    woman = woman_names[:woman_count]
    return man, woman

def removeBackground(input_dir):

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(input_dir, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'dBFg4eA7wAkpuVRKa1pcaqKw'},
    )
    if response.status_code == requests.codes.ok:
        with open('output.png', 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

    img = cv2.imread('output.png', cv2.IMREAD_UNCHANGED)

    origin = cv2.imread(input_dir, cv2.IMREAD_UNCHANGED)
    width, height, _ = origin.shape

    # extract only bgr channels
    bgr = img[:, :, 0:3]

    # extract alpha channel
    a = img[:, :, 3]

    # erode alpha channel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1,1))
    ae = cv2.morphologyEx(a, cv2.MORPH_ERODE, kernel)

    # compute outline mask as difference
    omask = a - ae
    omask[omask>0] = 255

    # create blue mask
    lower=(135,100,0)
    upper=(185,160,150)
    bmask = cv2.inRange(bgr, lower, upper)

    # mask as product of omask and bmask
    mask = cv2.bitwise_and(omask, bmask)
    imask = 255 - mask

    # create desaturated bgr image
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    hsv[:,:,1] = 0
    bgrd = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # blend bgr, bgrd using mask
    bgr_imask = cv2.bitwise_and(bgr, bgr, mask=imask)
    bgrd_mask = cv2.bitwise_and(bgrd, bgrd, mask=mask)
    bgr_new = cv2.add(bgr_imask, bgrd_mask)

    # blur alpha channel
    ab = cv2.GaussianBlur(ae, (0,0), sigmaX=1, sigmaY=1, borderType = cv2.BORDER_DEFAULT)

    # stretch values to 0
    aa = skimage.exposure.rescale_intensity(ab, in_range=(200,255), out_range=(0,255))

    # replace alpha channel in bgr_new with new alpha channel
    out = bgr_new.copy()
    out = cv2.cvtColor(out, cv2.COLOR_BGR2BGRA)
    out[:, :, 3] = aa

    # resize output images
    dim = (height, width)
    out = cv2.resize(out, dim, interpolation = cv2.INTER_AREA)
    aa = cv2.resize(aa, dim, interpolation=cv2.INTER_AREA)

    # save mask and output
    # mask_dir = 'mask_' + input_dir
    # result_dir = 'result_' + input_dir
    # cv2.imwrite(mask_dir, aa)
    # cv2.imwrite(result_dir, out)

    # return the value
    os.remove('output.png')
    return out

def imageCompose(back, characters):
    background = Image.open(back)
    length = len(characters) + 1
    side = background.width // length
    for (i, character) in enumerate(characters):
        overlay = Image.open(character)

        # Resize overlay image if needed
        # overlay = overlay.resize((overlay.width, overlay.height), Image.ANTIALIAS)

        # Position the overlay image
        position = (side * (i + 1) - overlay.width // 2, background.height - overlay.height - 50)  # coordinates where you want to paste

        # Overlay images
        background.paste(overlay, position, overlay)  # The third argument is for transparency

    # Save or display the result
    background.save("output_image.png")
    return background
if __name__ == '__main__':
    # cv2.imwrite('res.png', removeBackground('image/1.png'))
    # for i in range(1, 4):
    #     res = removeBackground(f'image/{i}.png')
    #     res = cv2.resize(res, (res.shape[1] // 4, res.shape[0] // 4), interpolation = cv2.INTER_AREA)
    #     cv2.imwrite(f'character/{i}.png', res)
    imageCompose('image/back.png', ['character/1.png', 'character/3.png'])