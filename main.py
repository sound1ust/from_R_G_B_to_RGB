from skimage.io import imread
from skimage import img_as_float
from numpy import roll


# a correlation for color channels
def correlation(channel, g, axis):
    crl = 0
    for i in range(-15, 15):
        test = roll(channel, i, axis=axis)
        c = (test * g).sum()
        if c > crl:
            crl = c
            num = i
    return num


# test comment 1
def align(img, g_coord):
    img = img_as_float(img)
    shape = img.shape
    pers = (shape[0] * 9 // 100, shape[1] * 8 // 100)

    b = img[0 + pers[0]: shape[0] // 3 - pers[0], 0 + pers[0]: shape[1] - pers[0]]
    g = img[shape[0] // 3 + pers[0]: shape[0] // 3 * 2 - pers[0], 0 + pers[0]: shape[1] - pers[0]]
    r = img[shape[0] // 3 * 2 + pers[0]: shape[0] // 3 * 3 - pers[0], 0 + pers[0]: shape[1] - pers[0]]

    row_g, col_g = g_coord

    br, bc = correlation(b, g, 0), correlation(b, g, 1)
    b1 = roll(b, br, axis=0)
    b1 = roll(b1, bc, axis=1)
    row_b, col_b = row_g - br - shape[0] // 3, col_g - bc

    rr, rc = correlation(r, g, 0), correlation(r, g, 1)
    r1 = roll(r, br + 8, axis=0)
    r1 = roll(r1, bc + 1, axis=1)
    row_r, col_r = row_g - rr + shape[0] // 3, col_g - rc

    return (row_b, col_b), (row_r, col_r)


print(align(imread("Content/00.png"), (508, 237)))  # (153, 237), (858, 238)
print(align(imread("Content/01.png"), (483, 218)))  # (145, 219), (817, 218)
print(align(imread("Content/02.png"), (557, 141)))  # (204, 143), (908, 140)
print(align(imread("Content/03.png"), (627, 179)))  # (243, 179), (1010, 176)
print(align(imread("Content/04.png"), (540, 96)))  # (154, 95), (922, 94)
print(align(imread("Content/05.png"), (641, 369)))  # (258, 372), (1021, 368)
print(align(imread("Content/06.png"), (527, 196)))  # (144, 198), (908, 193)
print(align(imread("Content/07.png"), (430, 140)))  # (82, 140), (777, 141)
print(align(imread("Content/08.png"), (502, 254)))  # (123, 259), (880, 25)
print(align(imread("Content/09.png"), (493, 238)))  # (114, 240), (871, 235)
