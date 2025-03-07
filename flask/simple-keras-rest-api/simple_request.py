# USAGE
# python simple_request.py

# import the necessary packages
import requests

# initialize the Keras REST API endpoint URL along with the input
# image path
KERAS_REST_API_URL = "http://164.125.34.170:8080/predict"
IMAGE_PATH = "dog.jpg"

# load the input image and construct the payload for the request
image = open(IMAGE_PATH, "rb").read()
payload = {"image": image}

# submit the request
# r = requests.post(KERAS_REST_API_URL, files=payload).json()
r = requests.post(KERAS_REST_API_URL)
print(r)
# ensure the request was sucessful
# if r["success"]:
if r == "good":
    print("haha")
	# loop over the predictions and display them
# 	for (i, result) in enumerate(r["predictions"]):
# 		print("{}. {}: {:.4f}".format(i + 1, result["label"],
# 			result["probability"]))

# otherwise, the request failed
else:
	print("Request failed")