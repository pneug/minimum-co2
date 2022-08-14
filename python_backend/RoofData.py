# retrieve an image of a location from the web using mapbox
# https://docs.mapbox.com/api/maps/#static-image
import requests
from PIL import Image
import numpy as np
import io
import cv2
from CostCalculator import kosten_normal, kosten_mit, kosten_anschaffung
import roof_sun

mapbox_token = "pk.eyJ1Ijoid3VzZWxtYXBzIiwiYSI6ImNqdTVpc2VibDA4c3E0NXFyMmEycHE3dXUifQ.Wy3_Ou1KrVRkIH1UGb_R3Q"


address = "Bahnhofweg 20, 82284 Grafrath"


def getMeterPerPixel(lat):
    meter_per_pixel_table = [0.299, 0.281, 0.229, 0.149, 0.052]
    abs_lat = abs(lat)
    if abs_lat == 0:
        return meter_per_pixel_table[0]
    elif abs_lat < 20:
        return meter_per_pixel_table[0] * (20-abs_lat) / 20 + meter_per_pixel_table[1] * abs_lat / 20
    elif abs_lat < 40:
        return meter_per_pixel_table[1] * (40-abs_lat) / 20 + meter_per_pixel_table[2] * (abs_lat - 20) / 20
    elif abs_lat < 60:
        return meter_per_pixel_table[2] * (60-abs_lat) / 20 + meter_per_pixel_table[3] * (abs_lat - 40) / 20
    else:
        return meter_per_pixel_table[3] * (80-abs_lat) / 20 + meter_per_pixel_table[4] * (abs_lat - 60) / 20


def loadImage(map_style, long, lat, zoom, res_x, res_y):
    mapbox_url = "https://api.mapbox.com/styles/v1/mapbox/" + map_style + "/static/{},{},{}/{}x{}?access_token={}".format(
        long,
        lat,
        zoom,
        res_x,
        res_y,
        mapbox_token)
    print("Trying to get ", mapbox_url)
    img = requests.get(mapbox_url)

    # store img as np array
    bytes_im = io.BytesIO(img.content)
    img_arr = cv2.cvtColor(np.array(Image.open(bytes_im)), cv2.COLOR_RGB2BGR)
    return img_arr[:, :, ::-1]


def get_roof_data(address):
    res_x, res_y = 512, 512
    mid_x, mid_y = res_x // 2, res_y // 2
    mid = np.array([mid_x, mid_y])
    zoom = 18
    # meter_per_pixel = 156543.03392 * 2**(zoom-1) / res_x

    # get the gps location of the address
    address_json = requests.get(
        "https://api.mapbox.com/geocoding/v5/mapbox.places/" + address + ".json?access_token=pk.eyJ1Ijoid3VzZWxtYXBzIiwiYSI6ImNqdTVpc2VibDA4c3E0NXFyMmEycHE3dXUifQ.Wy3_Ou1KrVRkIH1UGb_R3Q").json()
    print(address_json)
    long, lat = address_json["features"][0]["center"]
    print(lat, long)

    img_arr = loadImage("streets-v11", long, lat, zoom, res_x, res_y)
    # img_arr = loadImage("satellite-v9", long, lat, zoom, res_x, res_y)
    # satellite_img = loadImage("satellite-v11", long, lat, zoom, res_x, res_y)
    satellite_img = loadImage("satellite-v9", long, lat, zoom, res_x, res_y)

    pil_image = Image.fromarray(img_arr)
    # pil_image.show()

    # get the intensity of the pixel in the middle of the image
    intensity = img_arr[mid_x, mid_y]
    # get the intensity of the pixels in the middle of the image
    intensity_arr = np.mean(img_arr[mid_x-15:mid_x+15, mid_y-15:mid_y+15]) # , axis=(0, 1)
    print("intensity", intensity_arr)

    # get greyscale image of img_arr
    img_grey = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)

    # set every pixel to 0 that has not the same intensity as the pixel in the middle
    img_arr_mask = img_grey.copy()
    print("diff ", img_grey - intensity_arr)
    img_arr_mask[img_arr_mask - intensity_arr > 3] = 0

    """
    # segment the house in the middle of the image by masking everything around it with the same color
    # this is done by creating a mask with the same color as the house and then subtracting the mask from the image
    mask = np.zeros(img_arr.shape[:2], np.uint8)
    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)
    rect = (0, 0, res_x - 1, res_y - 1)
    # rect = (50, 50, 450, 450)
    # rect = (mid_x-10, mid_y-10, 20, 20)
    cv2.grabCut(img_arr, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    # mask2 = mask
    img_arr_mask = img_arr * mask2[:, :, np.newaxis]
    
    mask3 = mask2
    mask3[mask3 == cv2.GC_BGD] = 0 #certain background is black
    mask3[mask3 == cv2.GC_PR_BGD] = 63 #possible background is dark grey
    mask3[mask3 == cv2.GC_FGD] = 255  #foreground is white
    mask3[mask3 == cv2.GC_PR_FGD] = 192 #possible foreground is light grey
    
    pil_image = Image.fromarray(mask3)
    pil_image.show()
    """

    # erode for 2 iterations to simulate the border area that can't be used
    # img_arr_mask = cv2.erode(img_arr_mask, None, iterations=3)

    # get greyscale image of img_arr
    # img_grey = cv2.cvtColor(img_arr_mask, cv2.COLOR_BGR2GRAY)

    img_grey = img_arr_mask

    bin_mask = img_grey > 0

    pil_image = Image.fromarray(img_grey)
    # pil_image.show()

    print(bin_mask.shape)

    # get every object in the image that is seperated by black pixels
    objects = cv2.connectedComponentsWithStats(img_grey)

    # add the grey image

    print(objects[1])
    #mid_stack = mid.repeat(len(objects[3][1:])).reshape(-1, 2)
    #print(mid_stack)
    #print(objects[3][1:] - mid_stack)
    #obj_in_middle = np.argmin(np.linalg.norm(objects[3][1:] - mid_stack, axis=1))
    obj_in_middle = objects[1][mid_y][mid_x]
    print("Mid: ", obj_in_middle, objects[3][obj_in_middle])
    pix_area = objects[2][obj_in_middle][4]
    meter_per_pixel = getMeterPerPixel(lat)
    m_area = meter_per_pixel * meter_per_pixel * pix_area
    print("Area:", pix_area, m_area, meter_per_pixel)

    co2_per_kwh = 485  # in g/kWh, Quelle https://www.umweltbundesamt.de/en/press/pressinformation/co2-emissions-per-kilowatt-hour-of-electricity-in
    # load the solar intensityy (GIS) data from solargis.com
    # solar_intensity = pd.read_csv("https://solargis.com/data/solar_intensity.csv")

    # kwh_per_m2

    # set img_arr to half its previous value where img_arr_mask is not 0
    satellite_img[objects[1] == obj_in_middle] = satellite_img[objects[1] == obj_in_middle] / 2
    img_grey[objects[1] != obj_in_middle] = 0

    # convert img_grey to img with only r channel
    mask_red = cv2.cvtColor(img_grey, cv2.COLOR_GRAY2RGB)
    mask_red[mask_red > 0] = 255 / 2
    # set bg channels to 0
    mask_red[:, :, :2] = 0

    pil_image = Image.fromarray(satellite_img + mask_red)
    # pil_image.show()

    avg_life = 25
    kwh_per_m2 = 0.2
    kwh_per_year = m_area * kwh_per_m2
    mwh_per_life = kwh_per_year * avg_life

    data_dict = {
        "segmented_img": satellite_img + mask_red,
        "area": int(m_area),
        "kwh_per_year": int(kwh_per_year),
        "mwh_per_life": round(mwh_per_life / 1000, 2),
        "co2_per_year": int(kwh_per_year * co2_per_kwh / 1000),
        "co2_per_life": int(mwh_per_life * co2_per_kwh / 1000),
        "initial_cost": round(kosten_anschaffung(m_area), 2),

    }

    return data_dict


if __name__ == "__main__":
    get_roof_data(address)
