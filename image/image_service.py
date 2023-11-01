import torch
from lavis.models import load_model_and_preprocess
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, vis_processors, _ = load_model_and_preprocess(name="blip_caption",
                                                     model_type="large_coco",
                                                     is_eval=True, device=device)

# setup device to use
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def process_image(raw_image):
    """
    To send image need to convert like that
        image_data = await file.read()
        image_pil = Image.open(BytesIO(image_data))
        result = process_image(image_pil.convert("RGB"))
    """
    image = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    result = model.generate({"image": image})
    return result
