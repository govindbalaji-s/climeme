from PIL import Image, ImageDraw, ImageFont
import sys

roboto_fonts = {"light": "fonts/Roboto/Roboto-Light.ttf",
                "medium": "fonts/Roboto/Roboto-Medium.ttf",
                "regular": "fonts/Roboto/Roboto-Regular.ttf",
                "bold": "fonts/Roboto/Roboto-Bold.ttf",
                } 

def add_top_border (image, white_space):
    """Returns image with top border added

    Args:
        image (Image): The Image object on which to add the top border
        white_space (float): Fraction of original height to be added
            above

    Returns:
        Image: The image with the top border added
    """

    ret_size = (image.size[0], int(image.size[1] * (1 + white_space)))
    ret_image = Image.new('RGB', ret_size, (255, 255, 255))
    ret_image.paste (image, (0, int(white_space * image.size[1])))
    return ret_image

def add_top_text (image, top_text):
    image = add_top_border(image, .20)
    # font size * 4/3 ==? pixels ?
    font_size = int(.20 * image.size[1] * 0.75 * 0.5)
    draw = ImageDraw.Draw (image)
    font = ImageFont.truetype(roboto_fonts["medium"], size = font_size)
    posn = (0, 0)
    text_color = 'rgb(0, 0, 0)'
    draw.text(posn, top_text, fill=text_color, font=font)
    return image


# Input format:
# arg1 - image path
# arg2 - top text

if __name__ == "__main__" :
    image = Image.open(sys.argv[1])
    image = add_top_text(image, sys.argv[2])
    image.save('meme.jpg')
