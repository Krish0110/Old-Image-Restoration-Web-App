import os
from glob import glob
import cv2
import numpy as np
import torch
from torchvision.transforms import ToTensor

from ...config.model_paths import MODEL_PATHS
from .models import pretrained_aot1
from ...utilis.clear_directory import clear_directory

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def postprocess(image):
    image = torch.clamp(image, -1.0, 1.0)
    image = (image + 1) / 2.0 * 255.0
    image = image.permute(1, 2, 0)
    image = image.cpu().detach().numpy().astype(np.uint8)
    return image

def demo(resized_input_dir, mask_input_dir, output_dir):
    clear_directory(output_dir)
    
    # load images
    img_list = []
    for ext in ["*.jpg", "*.png"]:
        img_list.extend(glob(os.path.join(resized_input_dir, ext)))
    img_list.sort()

    mask_list = []
    for ext in ["*.jpg", "*.png"]:
        mask_list.extend(glob(os.path.join(mask_input_dir, ext)))
    mask_list.sort()

    # Model and version
    model = pretrained_aot1.InpaintGenerator()
    model.load_state_dict(torch.load(MODEL_PATHS["aot_generator"], map_location="cpu"))
    model.eval()

    for fn, mn in zip(img_list, mask_list):
        filename = os.path.basename(fn).split(".")[0]
        # maskname = os.path.basename(mn).split(".")[0]
        orig_img = cv2.resize(cv2.imread(fn, cv2.IMREAD_COLOR), (512, 512))
        mask = cv2.resize(cv2.imread(mn, cv2.IMREAD_COLOR), (512, 512))
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        print("Mask datatype", mask.dtype, mask.shape, mask.size)
        img_tensor = (ToTensor()(orig_img) * 2.0 - 1.0).unsqueeze(0)

        print('Data Type of Mask(mask) : ',type(mask))

        mask_tensor = torch.tensor(mask).float().unsqueeze(0) / 255.0
        mask_tensor = mask_tensor.unsqueeze(0)
        print("Mask tensor datatype", mask_tensor.dtype, mask_tensor.shape, mask_tensor.size)
        masked_tensor = (img_tensor * (1 - mask_tensor).float()) + mask_tensor
        print("Mask tensor datatype", masked_tensor.dtype, masked_tensor.shape, masked_tensor.size)

        pred_tensor = model(masked_tensor, mask_tensor)
      
        comp_tensor = pred_tensor * mask_tensor + img_tensor * (1 - mask_tensor)

        pred_np = postprocess(pred_tensor[0])
        masked_np = postprocess(masked_tensor[0])
        comp_np = postprocess(comp_tensor[0])

        cv2.imshow("pred_images", comp_np)
        print("inpainting finish!")

        comp_image_path = os.path.join(output_dir, "image_comp.png")
        cv2.imwrite(os.path.join(output_dir, "image_masked.png"), masked_np)
        cv2.imwrite(os.path.join(output_dir, "image_pred.png"), pred_np)
        cv2.imwrite(comp_image_path, comp_np)
        cv2.imwrite(os.path.join(output_dir, "image_mask.png"), mask)

        print("inpainting finish!")

        return {
            'inpainted_image': os.path.normpath(comp_image_path)
        }


