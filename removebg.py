import PIL.Image
import rembg
import cv2

input_image = 'uploads/aa.jpg' # input file
output_image = 'uploads/no_bg_duck.jpg' # output file

class RemoveBG():
    def remove_background():
        img = cv2.imread(input_image) # reading image file
        img_out = rembg.remove(img) # removing background

        cv2.imwrite(output_image, img_out)

        out_pil = PIL.Image.fromarray(img_out)
        bgr = PIL.Image.new('RGB', out_pil.size, (255, 255, 255))
        bgr.paste(out_pil, (0,0), out_pil)
        bgr.save('w_'+output_image)