import torch
import os
from .mainmodel1 import MainModel
from .utils import *
from skimage.color import rgb2lab
from PIL import Image
from torchvision import transforms
import numpy as np
from .resnet_unet import build_res_unet
from ...utilis.clear_directory import clear_directory
from ...config.model_paths import MODEL_PATHS

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def color_image(input_path, output_dir):
    net_G = build_res_unet()

    # Initialize the model and move it to the selected device
    model = MainModel(net_G = net_G)
    model = model.to(device)

    # Load the checkpoint
    checkpoint_path = MODEL_PATHS['color_model']
    checkpoint = torch.load(checkpoint_path, map_location=device)
    model.net_G.load_state_dict(checkpoint["model_G"])
    model.net_D.load_state_dict(checkpoint["model_D"])
    model.opt_G.load_state_dict(checkpoint["optimizer_G"])
    model.opt_D.load_state_dict(checkpoint["optimizer_D"])
    start_epoch = checkpoint["currentEpoch"] + 1
    print(f"Resuming training from epoch {start_epoch}.")

    # Define the transformation pipeline
    transform_pipeline = transforms.Compose([
        transforms.Resize((256, 256), Image.BICUBIC)
    ])
    
    # Load and transform the image
    img = Image.open(input_path).convert("RGB")
    img = transform_pipeline(img)

    # Convert the image to a numpy array and then to LAB color space
    img = np.array(img)
    img_lab = rgb2lab(img).astype("float32")  # Convert RGB to L*a*b

    # Convert LAB image to tensor
    to_tensor = transforms.ToTensor()
    img_lab = to_tensor(img_lab)

    # Separate L and ab channels and normalize them
    L = img_lab[[0], ...] / 50.0 - 1.0  # L channel normalized between -1 and 1
    ab = img_lab[[1, 2], ...] / 110.0   # ab channels normalized between -1 and 1

    # Add a batch dimension to L and move tensors to the same device as the model
    L = L.unsqueeze(0).to(device)
    ab = ab.unsqueeze(0).to(device)

    # Prepare data dictionary
    data = {'L': L, 'ab': ab}

    # Evaluate the model
    model.net_G.eval()
    with torch.no_grad():
        model.setup_input(data)
        model.forward()

    # Retrieve and process the output
    fake_color = model.fake_color.detach()
    fake_img = lab_to_rgb(L.cpu(), fake_color.cpu())  # Move tensors back to CPU for visualization

    # Convert numpy array to image (ensure it's in uint8 format)
    fake_img_np = (fake_img[0] * 255).astype(np.uint8)
    fake_img_pil = Image.fromarray(fake_img_np)

    # Save the image
    os.makedirs(output_dir, exist_ok=True)
    clear_directory(output_dir)
    os.makedirs(os.path.join(output_dir, "colored_image"), exist_ok=True)

    # Save the input image
    color_image_path = os.path.join(output_dir, "colored_image/colored_image.png")
    fake_img_pil.save(color_image_path)

    print(f"Image saved at {color_image_path}")

    return {
      'colored_image': os.path.normpath(color_image_path),
    }