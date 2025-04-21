import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

MODEL_PATHS = {
  "swin_model": os.path.join(BASE_DIR, "models", "swin", "best_model_1.pth"),
  "aot_generator" : os.path.join(BASE_DIR, "models", "aot", "G.pt"),
  "aot_discriminator" : os.path.join(BASE_DIR, "models", "aot", "D.pt"),
  "aot_optimizer" : os.path.join(BASE_DIR, "models", "aot", "O.pt"),
  "color_model": os.path.join(BASE_DIR, "models", "color","colorModel.pth"),
  "gfp_model": os.path.join(BASE_DIR, "models", "gfp", "gfpgan_final_model.pth"),
}

print("BASE_DIR:", BASE_DIR)
print("Model Path:", MODEL_PATHS["swin_model"])
