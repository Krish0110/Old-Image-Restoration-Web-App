import os
from ..modelPipelines.gfpLoadModel.gfp_main import gfp_loading

def run_gfp_pipeline(inpainted_image_path, output_dir, height, width):
    """
    :param colored_image_dir: folder containing your colored images
    :param output_dir: destination folder for high‑res outputs
    :returns: whatever gfp_loading returns, i.e. {'high_reso_image': '/full/path/to/output.png'}
    """
    os.makedirs(output_dir, exist_ok=True)
    return gfp_loading(inpainted_image_path, output_dir, height, width)

