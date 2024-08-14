import PIL.Image
import rembg
import cv2
import PIL

input = 'uploads/aa.jpg' # input file
output = 'uploads/no_bg_duck.jpg' # output file


img = cv2.imread(input) # reading image file
img_out = rembg.remove(img) # removing background

cv2.imwrite(output, img_out)

out_pil = PIL.Image.fromarray(img_out)
bgr = PIL.Image.new('RGB', out_pil.size, (255, 255, 255))
bgr.paste(out_pil, (0,0), out_pil)
bgr.save('w_'+output)