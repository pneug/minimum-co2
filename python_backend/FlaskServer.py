import numpy as np
from flask import Flask, jsonify, send_file
from flask_cors import CORS, cross_origin
from RoofData import get_roof_data
from PIL import Image
import os

app = Flask(__name__)
CORS(app, support_credentials=True)

curr_id = 0

# received_ids = []


def get_segmented_img_name(id):
    return "./segmented/" + str(id) + ".png"


@app.route("/address/<address>/<price_kwh>")
@cross_origin(supports_credentials=True)
def get_info(address, price_kwh):
    print("Price for kwh:", price_kwh)
    data_dict = get_roof_data(address)

    global curr_id
    img = Image.fromarray(data_dict["segmented_img"])
    # remove segmented_img from the data
    del data_dict["segmented_img"]
    img_name = get_segmented_img_name(curr_id)
    # check if image with img_name already exists
    if os.path.isfile(img_name):
        os.remove(img_name)
    img.save(img_name)

    data_dict["id"] = curr_id
    curr_id += 1
    return jsonify(data_dict)


@app.route("/get-by-id/<id>")
@cross_origin(supports_credentials=True)
def load_segmentation_img(id):
    # global received_ids
    # received_ids.append(id)
    return send_file(get_segmented_img_name(id), 'image/png')
