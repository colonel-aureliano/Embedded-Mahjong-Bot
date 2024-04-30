from inference_sdk import InferenceHTTPClient, InferenceConfiguration

def model():
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key="CSZoiz8bSkl72koYkTY6"
    )

    custom_configuration = InferenceConfiguration(confidence_threshold=0.3)

    # result = CLIENT.infer("data/Apr27shot/IMG_5743 Large.jpeg", model_id="mahjongdetection-4avhe/1")

    def to_return(file):
        with CLIENT.use_configuration(custom_configuration): 
            return CLIENT.infer(file, model_id="mahjongdetection-4avhe/1")

    return to_return

# print(result)

