import os
import torch
from .model_architecture_swin import SwinTransformerSys
from PIL import Image
import torchvision.transforms as transforms
import numpy as np
import torch.nn as nn
import cv2

import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

from ...config.model_paths import MODEL_PATHS
from ...utilis.clear_directory import clear_directory

# Ensure the device is correctly set
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize the model architecture (must match the trained model)
swin_model = SwinTransformerSys(
    img_size=512, 
    patch_size=4, 
    in_chans=3, 
    num_classes=1,  # Set to 1 since it's binary segmentation
    embed_dim=96, 
    depths=[2, 2, 2, 2], 
    depths_decoder=[1, 2, 2, 2],
    num_heads=[3, 6, 12, 24], 
    window_size=8, 
    mlp_ratio=4., 
    qkv_bias=True, 
    drop_rate=0., 
    attn_drop_rate=0., 
    drop_path_rate=0.1, 
    norm_layer=nn.LayerNorm, 
    ape=False, 
    patch_norm=True, 
    use_checkpoint=False, 
    final_upsample="expand_first"
).to(device)

# Load the trained weights
model_path = MODEL_PATHS["swin_model"]
swin_model.load_state_dict(torch.load(model_path, map_location=device))

# Move model to the device and set it to evaluation mode
swin_model.to(device)
swin_model.eval()

#processing the input image
def preprocess_image(image_path):
  transform = transforms.Compose([
    transforms.Resize((512, 512)),
    transforms.ToTensor(),
    transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))  # Normalize only image
  ])

  input_image = Image.open(image_path).convert("RGB")  # Ensure 3 channels
  input_image_tensor = transform(input_image).unsqueeze(0)  # Add batch dimension
  return input_image_tensor.to(device)

def postprocess_image(predicted_mask):
  # Enhancing the predicted mask
  threshold = 0.1  # Adjust threshold if needed
  binary_mask = (predicted_mask >= threshold).astype(np.uint8) * 255

  # Apply morphological operations to enhance mask
  kernel_size = 4  # Increase kernel size for thicker, more connected mask
  kernel = np.ones((kernel_size, kernel_size), np.uint8)

  # Step 1: Dilation (Thicker lines)
  dilated_mask = cv2.dilate(binary_mask, kernel, iterations=2)

  # Step 2: Closing (Fill small gaps)
  closed_mask = cv2.morphologyEx(dilated_mask, cv2.MORPH_CLOSE, kernel, iterations=2)

  # Step 3: Gaussian blur (Smoothen edges)
  smoothed_mask = cv2.GaussianBlur(closed_mask, (7, 7), 0)

  # Step 4: Bilateral filtering (Preserve edges while smoothening)
  filtered = cv2.bilateralFilter(smoothed_mask, d=9, sigmaColor=75, sigmaSpace=75)

  # 5. Re-binarize to 0 or 255
  _, final_mask = cv2.threshold(filtered, 127, 255, cv2.THRESH_BINARY)

  # === NEW: Fill enclosed areas in the mask ===
  contours, _ = cv2.findContours(final_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
  filled_mask = np.zeros_like(final_mask)

  for contour in contours:
      # Fill each closed contour in white
      cv2.drawContours(filled_mask, [contour], -1, 255, thickness=cv2.FILLED)

  # Merge the filled regions back into final_mask
  final_mask = cv2.bitwise_or(final_mask, filled_mask)

  # 6. Single channel, uint8
  if len(final_mask.shape) == 3:
      final_mask = cv2.cvtColor(final_mask, cv2.COLOR_BGR2GRAY)
  final_mask = final_mask.astype(np.uint8)
  return final_mask, binary_mask
   
def generate_binary_mask(input_image):
   # Perform inference
  with torch.no_grad():
    output_mask = swin_model(input_image)

  # Convert output to binary mask
  predicted_mask = torch.sigmoid(output_mask).cpu().squeeze().numpy()
  return predicted_mask
   
def run_swin_model(image_path, output_dir):
  os.makedirs(output_dir, exist_ok=True)
  clear_directory(output_dir)
  os.makedirs(os.path.join(output_dir, "resized_swin_image"), exist_ok=True)
  os.makedirs(os.path.join(output_dir, "final_output_masks"), exist_ok=True)
  os.makedirs(os.path.join(output_dir, "binary_masks"), exist_ok=True)

  #pre-process the image
  input_image_tensor = preprocess_image(image_path)
  predicted_mask =  generate_binary_mask(input_image_tensor)
  final_mask, binary_mask = postprocess_image(predicted_mask)

  #saving the resized input image
  # Convert the input tensor back to an image for visualization
  input_img_np = input_image_tensor.cpu().squeeze().permute(1, 2, 0).numpy()  # Convert to (H, W, C)
  input_img_np = (input_img_np * 0.5) + 0.5  # Undo normalization

  # Ensure values are in the range [0,1] before scaling
  input_img_np = np.clip(input_img_np, 0, 1)

  # Convert from [0,1] range to [0,255] and to uint8
  input_img_np_255 = (input_img_np * 255).astype(np.uint8)

  # Convert NumPy array to a PIL image
  input_image_pil = Image.fromarray(input_img_np_255)

  # Save the input image
  resized_input_path = os.path.join(output_dir, "resized_swin_image/input_image.png")
  input_image_pil.save(resized_input_path)  # Change path as needed

  # Save the improved mask
  final_mask_image = Image.fromarray(final_mask)
  final_mask_path = os.path.join(output_dir, "final_output_masks/cleaned_mask.png")
  final_mask_image.save(final_mask_path)

  #Save the binary mask
  binary_mask_image = Image.fromarray(binary_mask)
  binary_mask_path = os.path.join(output_dir, "binary_masks/binary_mask.png")
  binary_mask_image.save(binary_mask_path)

  #while returning our cleaned_mask is returend as binary mask in place of detected binary mask which is just stored
  return {
      'resized_input': os.path.normpath(resized_input_path),
      'binary_mask': os.path.normpath(final_mask_path),
  }



