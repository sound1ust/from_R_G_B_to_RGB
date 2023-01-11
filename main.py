from skimage.io import imread, imsave
from skimage import img_as_float, img_as_ubyte
from numpy import roll, dstack
from os import walk


# channel offset relative to the "g"
def correlation(channel, g, axis):
    maximum, offset = 0, 0

    for i in range(-15, 15):
        test = roll(channel, i, axis=axis)
        c = (test * g).sum()

        if c > maximum:
            maximum = c
            offset = i

        return offset


# it slices image to 3 pieces (r, g, b) then cut all borders from them (basically 5% of one picture sizes)
# then finds the most right offset of r and b channels and combine them all to one colored picture
def align(img, percentage=5):
    img = img_as_float(img)
    shape = img.shape
    perc = (shape[0] * percentage // 100, shape[1] * percentage // 100)

    b = img[0 + perc[0]: shape[0] // 3 - perc[0], 0 + perc[0]: shape[1] - perc[0]]
    g = img[shape[0] // 3 + perc[0]: shape[0] // 3 * 2 - perc[0], 0 + perc[0]: shape[1] - perc[0]]
    r = img[shape[0] // 3 * 2 + perc[0]: shape[0] // 3 * 3 - perc[0], 0 + perc[0]: shape[1] - perc[0]]

#    imsave("Result/r.png", img_as_ubyte(r))
#    imsave("Result/g.png", img_as_ubyte(g))
#    imsave("Result/b.png", img_as_ubyte(b))

    b_row, b_col = correlation(b, g, 0), correlation(b, g, 1)
    roll(b, b_row, axis=0)
    roll(b, b_col, axis=1)

    r_row, r_col = correlation(r, g, 0), correlation(r, g, 1)
    roll(r, r_row, axis=0)
    roll(r, r_col, axis=1)

    r = img_as_ubyte(r)
    g = img_as_ubyte(g)
    b = img_as_ubyte(b)

    imsave(f"Result/{file}", dstack((r, g, b)))


for root, dirs, files in walk("Content"):
    global file

    for file in sorted(files):
        align(imread(f"Content/{file}"))

