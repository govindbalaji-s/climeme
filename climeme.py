from PIL import Image, ImageDraw, ImageFont
import sys
import argparse


parser = argparse.ArgumentParser(description = 'Obtain image path, text and optional formatting values')

# Positional arguments that specify the mandatory arguments (may or may not possess default values)
parser.add_argument('image_path', help = 'Provide the file path to the tempplate you would like to insert')
parser.add_argument('top_text', help = 'Provide the top text for the meme')
parser.add_argument('output', nargs = '?', default = 'meme',help = 'Obtain the output file name from the user (default name : meme)')

# Optional arguments that can format the meme to required specifications
parser.add_argument('--font-size', dest = 'font_size', default = 14, type = int)
parser.add_argument('--border-size', dest = 'border_size', default = -1, type = int)

args = parser.parse_args()

roboto_fonts = {"light": "fonts/Roboto/Roboto-Light.ttf",
                "medium": "fonts/Roboto/Roboto-Medium.ttf",
                "regular": "fonts/Roboto/Roboto-Regular.ttf",
                "bold": "fonts/Roboto/Roboto-Bold.ttf",
                } 

def add_top_border (image, border_height):
    """Returns image with top border added

    Args:
        image (Image): The Image object on which to add the top border
        border_height (float): Border height to be added
            above

    Returns:
        Image: The image with the top border added
    """

    ret_size = (image.size[0], image.size[1] + border_height)
    ret_image = Image.new('RGB', ret_size, (255, 255, 255))
    ret_image.paste (image, (0, border_height))
    return ret_image

def add_top_text (image, top_text):
    """Returns a copy of the image with the given top text added

    Font size is 14.
    The text given is wrapped if it won't fit on a single line.
    Appropriate height border is added.

    Args:
        image (Image): Input image
        top_text (str): The text that is to be added at the top

    Returns:
        Image: New image after addint the top text.
    """

    # font size * 4/3 ==? pixels ?
    font = ImageFont.truetype(roboto_fonts["medium"], size = args.font_size)

    wrapped_lines = wrap_text(top_text, font, image.size[0])
    final_text = "\n".join(wrapped_lines)

    # If the size provided by the user is smaller than the minimum requisite space, we override the user's request and provide the minimum space required
    border_height = max(len(wrapped_lines) * args.font_size * 4 // 3, args.border_size)
    
    image = add_top_border(image, border_height)

    posn = (0, 0)
    text_color = 'rgb(0, 0, 0)'
    draw = ImageDraw.Draw (image)
    draw.text(posn, final_text, fill=text_color, font=font)
    return image

# https://stackoverflow.com/a/43829282/1882121
def wrap_text (text, font, base_width):
    """Wraps given text into multiple lines to fit into the given width

    Breaks the given text into a list of lines, so that the text when
    rendered with font won't horizontally overflow beyond base_width.
    If possible, lines are broken after complete words.

    Args:
        text (str): The text which is to be wrapped
        font (ImageFont): The font with which the text is to be rendered
        base_width (int): The maximum width for a single line

    Returns:
        list: List of lines
    """

    line_width = 0
    lines = []
    string = ""
    for c in text:
        line_width += font.getsize(c)[0]
        string += c
        if line_width > base_width:
            s = string.rsplit(" ", 1)

            string = s[0]
            lines.append(string)

            try:
                string = s[1]
                line_width = len(string) * 5
            except:
                string = ""
                line_width = 0

    if string:
        lines.append(string)
    return lines
# Input format:
# arg1 - image path
# arg2 - top text

if __name__ == "__main__" :
    image = Image.open(args.image_path)
    image = add_top_text(image, args.top_text)
    image.save('{}.jpg'.format(args.output))
