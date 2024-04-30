from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="CSZoiz8bSkl72koYkTY6"
)

result = CLIENT.infer("data/Apr27shot/IMG_5743 Large.jpeg", model_id="mahjongdetection-4avhe/1")

print(result)

# CLIENT.unload_model(model_id="mahjongdetection-4avhe/1")
