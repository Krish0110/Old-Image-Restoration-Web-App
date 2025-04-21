from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import base64
from io import BytesIO
from PIL import Image

from .modelPipelines.inpaintAotModel.aot_demo import demo
from .modelPipelines.loadDamageDetection.load_model_swin import run_swin_model
from .modelPipelines.addColorModel.demo3 import color_image
from .utilis.save_or_overwrite_file import save_or_overwrite_file
from .utilis.clear_directory import clear_directory
from .utilis.run_gfp_pipeline import run_gfp_pipeline

# Create your views here.
@csrf_exempt
def detect_damage(request):
  if request.method == 'POST' and request.FILES['image']:
    uploaded_image = request.FILES['image']

    # Save the uploaded image to a directory
    image_name = uploaded_image.name
    image_path = os.path.join('uploaded_images', image_name)

    clear_directory('uploaded_images')
    # Save or overwrite the uploaded image
    save_or_overwrite_file(uploaded_image, image_path)

    # Call the `run_swin_model` function
    output_dir = os.path.join('output_images', image_name.split('.')[0])  # Output folder for this specific image

    output_paths = run_swin_model(image_path, output_dir)
    print("Output paths:", output_paths)

    # Load the output images
    def encode_image_to_base64(path):
      print(f"Trying to encode image at: {path}")
      print("File exists:", os.path.exists(path))
      if not os.path.exists(path):
          return None  # Or raise a more descriptive error
      with Image.open(path) as img:
          buffered = BytesIO()
          img.save(buffered, format="PNG")
          img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
          return img_base64

    resized_input_b64 = encode_image_to_base64(output_paths['resized_input'])
    binary_mask_b64 = encode_image_to_base64(output_paths['binary_mask'])

    print("Encoded resized input:", resized_input_b64[:100])  # only show first 100 chars
    print("Encoded binary mask:", binary_mask_b64[:100])

    # Return the paths of the processed images as JSON
    return JsonResponse({
      'resized_input': resized_input_b64,
      'binary_mask': binary_mask_b64
    })
  
  return JsonResponse({"error": "Invalid request or no image uploaded."}, status=400)

@csrf_exempt
def inpaint_image(request):
    if request.method == 'POST':
        resized_input_image = request.FILES.get('input_image')
        mask_image = request.FILES.get('mask_image')

        if not resized_input_image or not mask_image:
            return JsonResponse({'error': 'Both input_image and mask_image are required.'}, status=400)

        # Save the uploaded files
        resized_input_name = resized_input_image.name
        mask_name = mask_image.name

        resized_input_dir = os.path.join('uploaded_images','resized_image')
        mask_input_dir = os.path.join('uploaded_images','mask_image')

        os.makedirs(resized_input_dir, exist_ok=True)
        os.makedirs(mask_input_dir, exist_ok=True)

        # Clear the directories before saving the new images
        clear_directory(resized_input_dir)
        clear_directory(mask_input_dir)

        resized_input_path = os.path.join(resized_input_dir, resized_input_name)
        mask_path = os.path.join(mask_input_dir, mask_name)

        # Save or overwrite the uploaded images
        save_or_overwrite_file(resized_input_image, resized_input_path)
        save_or_overwrite_file(mask_image, mask_path)

        # Define output path for inpainted image
        output_dir = os.path.join('output_images', resized_input_name.split('.')[0])
        os.makedirs(output_dir, exist_ok=True)
        # output_path = os.path.join(output_dir, 'inpainted.png')

        # Call your inpainting model
        inpaint_output_paths = demo(resized_input_dir, mask_input_dir, output_dir)
        inpainted_path = inpaint_output_paths['inpainted_image']

        # Convert inpainted image to base64
        def encode_image_to_base64(path):
            if not os.path.exists(path):
                return None
            with Image.open(path) as img:
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                return base64.b64encode(buffered.getvalue()).decode('utf-8')

        inpainted_b64 = encode_image_to_base64(inpainted_path)

        return JsonResponse({
            'inpainted_image': inpainted_b64
        })

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def add_color(request):
  if request.method == 'POST' and request.FILES['inpainted_image']:
    inpainted_input_image_for_color = request.FILES.get('inpainted_image')

    # Get width/height from the form data
    raw_w = request.POST.get('width')
    raw_h = request.POST.get('height')

    if raw_w is None or raw_h is None:
        return JsonResponse({"error": "Width and height fields are required."}, status=400)

    try:
        width = int(raw_w)
        height = int(raw_h)
    except ValueError:
        return JsonResponse({"error": "Width and height must be integers."}, status=400)

    # Save the uploaded image to a directory
    inpainted_image_name_for_color = inpainted_input_image_for_color.name
    inpainted_input_dir_for_color = os.path.join('uploaded_images','inpainted_image')

    os.makedirs(inpainted_input_dir_for_color, exist_ok=True)

    # Clear the directories before saving the new images
    clear_directory(inpainted_input_dir_for_color)

    inpainted_input_path_for_color = os.path.join(inpainted_input_dir_for_color, inpainted_image_name_for_color)

    # Save or overwrite the uploaded images
    save_or_overwrite_file(inpainted_input_image_for_color, inpainted_input_path_for_color)

    # Define output path for inpainted image
    output_dir = os.path.join('output_images', inpainted_image_name_for_color.split('.')[0])
    os.makedirs(output_dir, exist_ok=True)

    #call color model
    output_paths = color_image(inpainted_input_path_for_color, output_dir)
    print("Output paths:", output_paths)

    # Load the output images
    def encode_image_to_base64(path):
      print(f"Trying to encode image at: {path}")
      print("File exists:", os.path.exists(path))
      if not os.path.exists(path):
          return None  # Or raise a more descriptive error
      with Image.open(path) as img:
          buffered = BytesIO()
          img.save(buffered, format="PNG")
          img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
          return img_base64

    colored_image_path = output_paths['colored_image']
    colored_image_dir = os.path.dirname(colored_image_path)
    output_dir_final = os.path.join('output_images', "final_image")

    gfp_output_paths = run_gfp_pipeline(colored_image_path, output_dir_final, height, width )
    print("Returned from gfp_loading:", gfp_output_paths)
    # Encode GFP image to base64
    gfp_output_b64 = encode_image_to_base64(gfp_output_paths['high_reso_image'])
    # Return the paths of the processed images as JSON
    return JsonResponse({
      'final_image_output': gfp_output_b64,
    })
  
  return JsonResponse({"error": "Invalid request or no image uploaded."}, status=400)

@csrf_exempt
def use_gfp(request):
  if request.method == 'POST' and request.FILES['inpainted_image']:
    inpainted_input_image_for_gfp = request.FILES.get('inpainted_image')

        # Get width/height from the form data
    raw_w = request.POST.get('width')
    raw_h = request.POST.get('height')

    if raw_w is None or raw_h is None:
        return JsonResponse({"error": "Width and height fields are required."}, status=400)

    try:
        width = int(raw_w)
        height = int(raw_h)
    except ValueError:
        return JsonResponse({"error": "Width and height must be integers."}, status=400)

    # Save the uploaded image to a directory
    inpainted_image_name_for_gfp = inpainted_input_image_for_gfp.name
    inpainted_input_dir_for_gfp = os.path.join('uploaded_images','inpainted_image')

    os.makedirs(inpainted_input_dir_for_gfp, exist_ok=True)

    # Clear the directories before saving the new images
    clear_directory(inpainted_input_dir_for_gfp)

    inpainted_input_path_for_gfp = os.path.join(inpainted_input_dir_for_gfp, inpainted_image_name_for_gfp)

    # Save or overwrite the uploaded images
    save_or_overwrite_file(inpainted_input_image_for_gfp, inpainted_input_path_for_gfp)

    # Define output path for inpainted image
    output_dir = os.path.join('output_images', "final_image")
    os.makedirs(output_dir, exist_ok=True)

    #call color model
    output_paths = run_gfp_pipeline(inpainted_input_path_for_gfp, output_dir, height, width)
    print("Output paths:", output_paths)

    # Load the output images
    def encode_image_to_base64(path):
      print(f"Trying to encode image at: {path}")
      print("File exists:", os.path.exists(path))
      if not os.path.exists(path):
          return None  # Or raise a more descriptive error
      with Image.open(path) as img:
          buffered = BytesIO()
          img.save(buffered, format="PNG")
          img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
          return img_base64

    high_reso_image_b64 = encode_image_to_base64(output_paths['high_reso_image'])

    print("Encoded resized input:", high_reso_image_b64[:100])  # only show first 100 chars

    # Return the paths of the processed images as JSON
    return JsonResponse({
      'final_image_output': high_reso_image_b64,
    })
  
  return JsonResponse({"error": "Invalid request or no image uploaded."}, status=400)
