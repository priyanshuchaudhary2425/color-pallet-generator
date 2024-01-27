from flask import Flask, render_template
from PIL import Image
import base64
from io import BytesIO
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField
import colorgram
import numpy as np

app = Flask(__name__)
app.config['SECRET_KEY'] = '35eb906ff292569f68a5e20834ffe492f7de22b7688d1ef3'
Bootstrap(app)


class UploadFileForm(FlaskForm):
    file = FileField("upload file", validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField("Submit")


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    image_data = None
    msg = None
    image = None
    colors = []
    message = None

    if form.validate_on_submit():
        file = form.file.data
        image = Image.open(file)
        image_data = image_to_base64(image)
        colors = extract_colors(image)
        msg = "File uploaded successfully."

    convert_colors = convert_color(colors, "HEX")

    return render_template("index.html", form=form, image_data=image_data,
                           msg=msg, image=image, colors=convert_colors, message=message )


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format=image.format)
    encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return encoded_image


def extract_colors(image):
    colors = colorgram.extract(image, number_of_colors=100)
    return colors


def convert_color(colors, code_choice):
    convert_colors = []
    for color in colors:
        rgb = color.rgb
        if code_choice == 'HEX':
            hex_code = rgb_to_hex(rgb)
            convert_colors.append(hex_code)
        else:
            convert_colors.append(rgb)
    return convert_colors


def rgb_to_hex(rgb):
    r, g, b = rgb
    hex_code = "#%02x%02x%02x" % (r, g, b)
    return hex_code


if __name__ == '__main__':
    app.run(debug=True)
