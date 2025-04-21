import torch
from torch import optim
from .loss import *
from .models import *
import numpy as np
from skimage.color import rgb2lab, lab2rgb
# from pytorch_msssim import ssim
# from pytorch_msssim import ssim
# from torchmetrics.image.fid import FrechetInceptionDistance
from .metric import compare_mae, compare_psnr, compare_ssim, fid
class MainModel(nn.Module):
    def __init__(self, net_G=None, lr_G=2e-4, lr_D=2e-4, 
                 beta1=0.5, beta2=0.999, lambda_L1=100.):
        super().__init__()
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.lambda_L1 = lambda_L1
        
        if net_G is None:
            # print('SIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII')
            self.net_G = Unet(input_c=1, output_c=2, n_down=8, num_filters=64).to(self.device)
        else:
            self.net_G = net_G.to(self.device)
        self.net_D = PatchDiscriminator(input_c=3, n_down=3, num_filters=64).to(self.device)
        self.GANcriterion = GANLoss(gan_mode='vanilla').to(self.device)
        self.L1criterion = nn.L1Loss()
        self.perceptual = Perceptual().to(self.device)
        self.opt_G = optim.Adam(self.net_G.parameters(), lr=lr_G, betas=(beta1, beta2))
        self.opt_D = optim.Adam(self.net_D.parameters(), lr=lr_D, betas=(beta1, beta2))
    
    def set_requires_grad(self, model, requires_grad=True):
        for p in model.parameters():
            p.requires_grad = requires_grad
        
    def setup_input(self, data):
        self.L = data['L'].to(self.device)
        self.ab = data['ab'].to(self.device)
        
    def forward(self, val = False):
        self.fake_color = self.net_G(self.L)
        #You need original ab values now which is self.ab

        if val:
            self.real_rgb = self.lab_to_rgb_postprocess(self.L, self.ab).to('cuda')
            self.fake_rgb = self.lab_to_rgb_postprocess(self.L, self.fake_color).to('cuda')
            fake_image = torch.cat([self.L, self.fake_color], dim=1)
            fake_preds = self.net_D(fake_image)
            self.loss_G_GAN = self.GANcriterion(fake_preds, True)
            self.loss_G_L1 = self.L1criterion(self.fake_color, self.ab) * self.lambda_L1
            self.loss_G_per = self.perceptual(self.fake_rgb, self.real_rgb)
            # self.loss_G_sty = self.style(self.fake_color, self.ab)

            self.loss_G = 0.01 * self.loss_G_GAN + self.loss_G_L1 + 0.1*self.loss_G_per
            # Ensure tensors are on CPU and converted to NumPy
            real_np = self.real_rgb.detach().cpu().numpy()  # Shape: (16, 3, 256, 256)
            fake_np = self.fake_rgb.detach().cpu().numpy()  # Shape: (16, 3, 256, 256)
            # print(real_np, fake_np)
            # Initialize accumulators for batch averaging
            

            # Compute metrics for each image in the batch
            
            self.mae = compare_mae((fake_np, real_np))
            self.psnr = compare_psnr((fake_np, real_np))
            self.ssim = compare_ssim((fake_np, real_np))

            # # Compute batch average
            # self.mae = mae_total / real_np.shape[0]
            # self.psnr = psnr_total / real_np.shape[0]
            # self.ssim = ssim_total / real_np.shape[0]

            # Compute FID using the entire batch
            # print('Shapes : ',self.real_rgb.shape, self.fake_rgb.shape)
            # self.fid = fid(self.real_rgb.cpu(), self.fake_rgb.cpu())



    
    #Converting Lab (ab - 2 channels) format into RGB format (3- channels) as we need 3 channels input for VGG19 based perceptual loss

    def lab_to_rgb_postprocess(self, L, ab):
        # Denormalize
        L = (L + 1) * 50  # Scale back L
        ab = ab * 110  # Scale back ab

        batch_size = L.shape[0]  # Get batch size
        rgb_images = []

        for i in range(batch_size):
            lab_image = np.zeros((L.shape[2], L.shape[3], 3), dtype=np.float32)  # (H, W, 3)
            lab_image[:, :, 0] = L[i, 0].cpu().detach().numpy()  # L channel
            lab_image[:, :, 1:] = ab[i].cpu().detach().numpy().transpose(1, 2, 0)  # ab channels

            # Convert to RGB
            rgb_image = lab2rgb(lab_image)
            rgb_images.append(torch.tensor(rgb_image).permute(2, 0, 1))  # Convert to (C, H, W)

        # Stack all images into a single batch tensor (B, C, H, W)
        return torch.stack(rgb_images)

    # # Apply post-processing
    # rgb_tensor = lab_to_rgb_postprocess(L, ab)
    def backward_D(self):
        fake_image = torch.cat([self.L, self.fake_color], dim=1)
        fake_preds = self.net_D(fake_image.detach())
        self.loss_D_fake = self.GANcriterion(fake_preds, False)
        real_image = torch.cat([self.L, self.ab], dim=1)
        real_preds = self.net_D(real_image)
        self.loss_D_real = self.GANcriterion(real_preds, True)
        self.loss_D = (self.loss_D_fake + self.loss_D_real) * 0.5
        self.loss_D.backward()
    
    def backward_G(self):
        real_rgb = self.lab_to_rgb_postprocess(self.L, self.ab).to('cuda')
        fake_rgb = self.lab_to_rgb_postprocess(self.L, self.fake_color).to('cuda')
        fake_image = torch.cat([self.L, self.fake_color], dim=1)
        fake_preds = self.net_D(fake_image)
        self.loss_G_GAN = self.GANcriterion(fake_preds, True)
        self.loss_G_L1 = self.L1criterion(self.fake_color, self.ab) * self.lambda_L1
        self.loss_G_per = self.perceptual(fake_rgb, real_rgb)
        # self.loss_G_sty = self.style(self.fake_color, self.ab)

        self.loss_G = 0.01 * self.loss_G_GAN + self.loss_G_L1 + 0.1*self.loss_G_per
        self.loss_G.backward()
    
    def optimize(self):
        self.forward()
        self.net_D.train()
        self.set_requires_grad(self.net_D, True)
        self.opt_D.zero_grad()
        self.backward_D()
        self.opt_D.step()
        
        self.net_G.train()
        self.set_requires_grad(self.net_D, False)
        self.opt_G.zero_grad()
        self.backward_G()
        self.opt_G.step()

model = MainModel()
