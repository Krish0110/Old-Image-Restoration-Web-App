import torch
from torch import nn
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.models as models
from PIL import Image
from torch.nn.functional import conv2d






class VGG19(nn.Module):
    def __init__(self, resize_input=False):
        super(VGG19, self).__init__()
        features = models.vgg19(pretrained=True).features

        self.resize_input = resize_input
        self.mean = torch.Tensor([0.485, 0.456, 0.406]).cuda()
        self.std = torch.Tensor([0.229, 0.224, 0.225]).cuda()
        prefix = [1, 1, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5]
        posfix = [1, 2, 1, 2, 1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
        names = list(zip(prefix, posfix))
        self.relus = []
        for pre, pos in names:
            self.relus.append("relu{}_{}".format(pre, pos))
            self.__setattr__("relu{}_{}".format(pre, pos), torch.nn.Sequential())

        nums = [
            [0, 1],
            [2, 3],
            [4, 5, 6],
            [7, 8],
            [9, 10, 11],
            [12, 13],
            [14, 15],
            [16, 17],
            [18, 19, 20],
            [21, 22],
            [23, 24],
            [25, 26],
            [27, 28, 29],
            [30, 31],
            [32, 33],
            [34, 35],
        ]

        for i, layer in enumerate(self.relus):
            for num in nums[i]:
                self.__getattr__(layer).add_module(str(num), features[num])

        # don't need the gradients, just want the features
        for param in self.parameters():
            param.requires_grad = False

    def forward(self, x):
        # resize and normalize input for pretrained vgg19
        x = (x + 1.0) / 2.0
        x = (x - self.mean.view(1, 3, 1, 1)) / (self.std.view(1, 3, 1, 1))
        if self.resize_input:
            x = F.interpolate(x, size=(256, 256), mode="bilinear", align_corners=True)
        features = []
        for layer in self.relus:
            x = self.__getattr__(layer)(x)
            features.append(x)
        out = dict(zip(self.relus, features))
        return out


class Perceptual(nn.Module):
    def __init__(self):
        super(Perceptual, self).__init__()
        self.vgg = VGG19().cuda()
        self.criterion = nn.L1Loss()


    def forward(self, x, y):
        vgg_x, vgg_y = self.vgg(x), self.vgg(y)
        loss = 0

        for i in range(1,6):
            loss += self.criterion(vgg_x[f"relu{i}_1"], vgg_y[f"relu{i}_1"])

        return loss




class GANLoss(nn.Module):
    def __init__(self, gan_mode='vanilla', real_label=1.0, fake_label=0.0):
        super().__init__()
        self.register_buffer('real_label', torch.tensor(real_label))
        self.register_buffer('fake_label', torch.tensor(fake_label))
        if gan_mode == 'vanilla':
            self.loss = nn.BCEWithLogitsLoss()
        elif gan_mode == 'lsgan':
            self.loss = nn.MSELoss()
    
    def get_labels(self, preds, target_is_real):
        if target_is_real:
            labels = self.real_label
        else:
            labels = self.fake_label
        return labels.expand_as(preds)
    
    def __call__(self, preds, target_is_real):
        labels = self.get_labels(preds, target_is_real)
        loss = self.loss(preds, labels)
        return loss