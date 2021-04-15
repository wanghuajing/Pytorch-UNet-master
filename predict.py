import argparse
import logging
import os

import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image
from torchvision import transforms

from unet import UNet
from utils.data_vis import plot_img_and_mask
from utils.dataset import BasicDataset
import pre_config


def predict_img(net, full_img, device, scale_factor=1, out_threshold=0.5):
    net.eval()

    img = torch.from_numpy(BasicDataset.preprocess(full_img, scale_factor,False))

    img = img.unsqueeze(0)
    img = img.to(device=device, dtype=torch.float32)

    with torch.no_grad():
        output = net(img)

        if net.n_classes > 1:
            probs = F.softmax(output, dim=1)
        else:
            probs = torch.sigmoid(output)

        probs = probs.squeeze(0)

        tf = transforms.Compose(
            [
                transforms.ToPILImage(),
                transforms.Resize(full_img.size[1]),
                transforms.ToTensor()
            ]
        )

        probs = tf(probs.cpu())
        full_mask = probs.squeeze().cpu().numpy()

    return full_mask > out_threshold


def get_output_filenames(pre_img, output):
    in_files = pre_img
    out_files = []

    if not output:
        for f in in_files:
            pathsplit = os.path.splitext(f)
            out_files.append("{}_OUT{}".format(pathsplit[0], pathsplit[1]))
    elif len(in_files) != len(output):
        logging.error("Input files and output files are not of the same length")
        raise SystemExit()
    else:
        out_files = output

    return out_files


def mask_to_image(mask):
    return Image.fromarray((mask * 255).astype(np.uint8))


if __name__ == "__main__":
    in_files = pre_config.pre_img
    out_files = get_output_filenames(pre_config.pre_img, pre_config.output)

    net = UNet(n_channels=pre_config.channels, n_classes=1)

    logging.info("Loading model {}".format(pre_config.model))

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logging.info(f'Using device {device}')
    net.to(device=device)
    net.load_state_dict(torch.load(pre_config.model, map_location=device))

    logging.info("Model loaded !")

    for i, fn in enumerate(in_files):
        logging.info("\nPredicting image {} ...".format(fn))

        img = Image.open(fn)
        if 'RIGHT' in fn:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        mask = predict_img(net=net,
                           full_img=img,
                           scale_factor=pre_config.scale,
                           out_threshold=pre_config.mask_threshold,
                           device=device)
        if not pre_config.no_save:
            out_fn = out_files[i]
            result = mask_to_image(mask)
            if 'RIGHT' in fn:
                result = result.transpose(Image.FLIP_LEFT_RIGHT)
            result.save(out_files[i])

            logging.info("Mask saved to {}".format(out_files[i]))

        if pre_config.viz:
            logging.info("Visualizing results for image {}, close to continue ...".format(fn))
            plot_img_and_mask(img, mask)
