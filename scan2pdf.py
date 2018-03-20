import argparse
import sys
from pathlib import Path

import imagesize
from fpdf import FPDF

parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', type=str, default='.',
                    help='Directory with input images.')
parser.add_argument('--output', type=str, default='document.pdf',
                    help='Output document')
parser.add_argument('--format', type=str, default='jpg',
                    help='Input image format that will be used as extension.')
parser.add_argument('--dpi', type=int, default=300,
                    help='DPI of input images.')
args = parser.parse_args()

A = {
    5: (5.8, 8.3),
    4: (8.3, 11.7),
}


def get_image_list(image_dir: str, extension: str):
    image_dir = Path(image_dir).resolve()
    images = map(str, image_dir.glob(f'*.{extension}'))
    return sorted(images)


def add_image(pdf: FPDF, image: str, dpi: int):
    w0, h0 = imagesize.get(image)

    if w0 < h0:
        orient = 'P'
    else:
        orient = 'L'

    keys = list(A.keys())
    keys.sort(key=lambda n: -n)

    for k in keys:
        w, h = A[k][0] * dpi, A[k][1] * dpi
        if orient == 'L':
            w, h = h, w
        fmt = f'A{k}'
        if w0 < w and h0 < h:
            break
    else:
        print(f'Image size is too big: {w0}×{h0} (for {w}×{h})')
        w0 = w

    pdf.add_page(orientation=orient, format=fmt)
    pdf.image(image, x=(w - w0) / 2 / dpi, y=(h - h0) / 2 / dpi, w=w0 / dpi)


def main():
    images = get_image_list(args.input_dir, args.format)

    if len(images) == 0:
        sys.exit('No images were found')

    pdf = FPDF(unit='in')
    pdf.set_font('helvetica')

    for image in images:
        print(image)
        add_image(pdf, image, args.dpi)

    print('Writing', args.output)
    pdf.output(args.output, 'F')


if __name__ == '__main__':
    main()
