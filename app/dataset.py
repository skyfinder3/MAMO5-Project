import os
import torch
import numpy as np
import nibabel as nib

from random import randint
from torch.utils.data import Dataset
from torchvision import transforms

class MRIDataset(Dataset):
    """Healthy MRI dataset."""

    def __init__(self, ROOT_DIR, transform=None, img_size=(32, 32), random_slice=False):
        """
        Args:
            ROOT_DIR (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
        """
        # 23/01/2025 RM this makes a transform method, transforming 
        self.transform = transforms.Compose(
                [transforms.ToPILImage(),                                 # 22/01/2025 RM transforms to pil image                 
                 transforms.RandomAffine(3, translate=(0.02, 0.09)),        # 22/01/2025 RM transforms by rotating a couple degrees
                 transforms.CenterCrop(256),                                # 22/01/2025 RM crops the center of the image (likely has to be adapted) TODO
                 transforms.Resize(img_size, transforms.InterpolationMode.BILINEAR),     # 22/01/2025 RM resizes to the original size  
                 # transforms.CenterCrop(256),                                # 28/01/2025 RM crop to center for new dataset
                 transforms.ToTensor(),                                     # 22/01/2025 RM transforms back to tensor 
                 transforms.Normalize((0.5), (0.5))                         # 22/01/2025 RM normalizes values
                 ]
                ) if not transform else transform

        self.filenames = [f for f in os.listdir(ROOT_DIR) if not f.startswith('.')] # 22/01/2025 RM added to exclude the .ipy files from the notebook
        if ".DS_Store" in self.filenames:
            self.filenames.remove(".DS_Store")
        self.ROOT_DIR = ROOT_DIR
        self.random_slice = random_slice

    def __len__(self):
        return len(self.filenames)

    def __getitem__(self, idx):
        # print(repr(idx))
        if torch.is_tensor(idx):
            idx = idx.tolist()
        if os.path.exists(os.path.join(self.ROOT_DIR, self.filenames[idx], f"{self.filenames[idx]}.npy")):
            # 23/01/2025 RM load np array if it already exists
            image = np.load(os.path.join(self.ROOT_DIR, self.filenames[idx], f"{self.filenames[idx]}.npy"))
            pass
        else:
            img_name = os.path.join(
                    self.ROOT_DIR, self.filenames[idx], f"{self.filenames[idx]}_2000002_1.nii.gz"
                    )
            # random between 40 and 130
            # print(nib.load(img_name).slicer[:,90:91,:].dataobj.shape)
            # 23/01/2025 RM loading of the new image 
            img = nib.load(img_name)
            image = img.get_fdata()

            # 23/01/2025 RM compute mean, standard deviation and range
            image_mean = np.mean(image)
           
            image_std = np.std(image)
            img_range = (image_mean - 1 * image_std, image_mean + 2 * image_std)
            # 23/01/2025 RM normalize image between 0 and 1
            image = np.clip(image, img_range[0], img_range[1])
            image = image / (img_range[1] - img_range[0])
            # 23/01/2025 RM save as npy array
            np.save(
                    os.path.join(self.ROOT_DIR, self.filenames[idx], f"{self.filenames[idx]}.npy"), image.astype(
                            np.float32
                            )
                    )
        
        if self.random_slice:
            # slice_idx = randint(32, 122)
            slice_idx = randint(0, 79) # RM 28/01/2025 change slices to 0-80 because of own dataset
        else:
            slice_idx = 40

        # RM 28/01/2025 adjusted to 256*256 
        image = image[:, :, slice_idx:slice_idx+1].astype(np.float32)
        
        # 22/01/2025 RM transform image if not transformed
        if self.transform:
            image = self.transform(image)

        # 24/01/2025 added print slice and filename to veryfy it working
        sample = {'image': image, "filenames": self.filenames[idx]}
        return sample
