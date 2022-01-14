from PIL import Image

import glob

darkimgthreshold = 0.58
pxthreshold = 100
ddircty = "dark"
ldircty = "light"


import os
if not os.path.exists(ddircty):
    os.makedirs(ddircty)
if not os.path.exists(ldircty):
    os.makedirs(ldircty)

ftypes = [".jpg",".JPG",".png",".PNG",".bmp",".BMP"]
jpgs = []
for ftyp in ftypes:
    jpgs.extend(glob.glob("*"+ftyp))


print("Found images", jpgs)
lnimg = len(jpgs)
for i, pic_f in enumerate(jpgs):
    ofn = pic_f.split("/")[-1]
    with Image.open(pic_f) as im:
        pix = im.load()
        im.show()
        pbt=0 # pixels below threshold
        for y in range(im.size[1]):
            for x in range(im.size[0]):
                pxd = sum(pix[x,y])
                if pxd <= pxthreshold:
                    pbt += 1
        ltscore = pbt/(im.size[0]*im.size[1]);
        im.close()
        print("%sof%s, %s :: Dark px%% %.2f | "%(i, lnimg, ofn, ltscore), end='')
        if (ltscore > darkimgthreshold):
            print("+++ DARK BACKGROUND")
            fn = ddircty+"/"+ofn
            os.rename(pic_f, pic_f[:-(len(ofn))]+fn)
        else: 
            print("--- LIGHT BG")
            fn = ldircty+"/"+ofn
            os.rename(pic_f, pic_f[:-(len(ofn))]+fn)



                

