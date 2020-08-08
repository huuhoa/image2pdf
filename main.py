#!env python3

import os
import img2pdf


def extract_order(filename: str):
    import re

    pattern = re.compile(r'\((\d+)\)')
    m = re.findall(pattern, filename)
    value = 0
    if m is not None:
        value = int(m[0])
    else:
        print('Something wrong with file name %s' % filename)
        exit(1)
    return value


def get_image_list(src: str):
    imgs = []
    for r, _, f in os.walk(src):
        for fname in f:
            if not fname.endswith(".png"):
                continue
            imgs.append(os.path.join(r, fname))
    imgs.sort()

    return imgs


def convert_image(src: str, dest: str):
    import subprocess

    imgs = get_image_list(src)
    first = extract_order(imgs[0])
    last = extract_order(imgs[-1])
    print('Extracting first pages ...')
    cmd = ["magick", "%s/Screenshot (%%d).png[%d-%d]" % (src, first, last), "-crop", "1090x1378+2110+90", "-background",
           "white", "-alpha", "remove", "-alpha", "off", "%s/page%%03d_1.png" % dest]
    print(cmd)
    subprocess.call(cmd)
    print('Done')

    print('Extracting second pages ...')
    cmd = ["magick", "%s/Screenshot (%%d).png[%d-%d]" % (src, first, last), "-crop", "1090x1378+3200+90", "-background",
           "white", "-alpha", "remove", "-alpha", "off", "%s/page%%03d_2.png" % dest]
    print(cmd)
    subprocess.call(cmd)
    print('Done')


def convert_pdf(src: str, dest: str):
    with open(dest, "wb") as fpdf:
        print("converting ...")
        imgs = get_image_list(src)
        fpdf.write(img2pdf.convert(imgs))


def removedirs(path):
    import subprocess
    cmd = ['rm', '-rf', path]
    subprocess.call(cmd)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('input', type=str, help='input folder contains all images')
    parser.add_argument('output', type=str, help='output pdf file')
    args = parser.parse_args()
    book_name = args.output
    working_dir = args.input

    temp_dir = os.path.join(working_dir, '..', 'temp')
    os.makedirs(temp_dir, exist_ok=True)
    convert_image(working_dir, temp_dir)
    convert_pdf(temp_dir, book_name)
    removedirs(temp_dir)
