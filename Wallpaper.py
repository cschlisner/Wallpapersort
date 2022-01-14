from PIL import Image, ImageStat
import os
import glob
import argparse


parser = argparse.ArgumentParser()
parser.add_argument(
	"dir",
	help="image directory to sort"
)
parser.add_argument(
	"-t", "--threshold",
	metavar="pixValueThreshold",
	help="use the specified value to determine dark/light images (R+B+G)",
	required=False
)
args = parser.parse_args()

pxthreshold = 175 if args.threshold is None else float(args.threshold)
ddircty = args.dir+"/dark"
ldircty = args.dir+"/light"

if not os.path.exists(ddircty):
    os.makedirs(ddircty)
if not os.path.exists(ldircty):
    os.makedirs(ldircty)

ftypes = [".jpg",".JPG",".png",".PNG",".bmp",".BMP"]
jpgs = []
for ftyp in ftypes:
    jpgs.extend(glob.glob(args.dir+"/*"+ftyp))


print("Found images", jpgs)
lnimg = len(jpgs)
for i, pic_f in enumerate(jpgs):
    ofn = pic_f.split(args.dir)[-1]

    try:
        with Image.open(pic_f) as im:
            try: 
                pix = im.load()
            except Exception as e:
                print("COULD NOT LOAD %s -- %s"%(pic_f, e))
                continue

            stat = ImageStat.Stat(im)
            ltscore = sum(stat.mean)
            print("%s of %s >> %s :: mean brightness %.2f | "%(i, lnimg, ofn, ltscore), end='')
            if (ltscore <  pxthreshold):
                print("--- DARK BG")
                fn = ddircty+"/"+ofn
                os.rename(pic_f, fn)
            else: 
                print("--- LIGHT BG")
                fn = ldircty+"/"+ofn
                os.rename(pic_f, fn)
    except Exception as e:
            continue



                

