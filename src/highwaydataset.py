import torchvision.transforms as T
from torch.utils.data import Dataset, DataLoader

from utils import flatten
import cv2
import glob
import random


# A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
# A.RandomBrightnessContrast(p=0.5),
# A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
# A.HueSaturationValue(hue_shift_limit=0.2, sat_shift_limit=0.2, val_shift_limit=0.2, p=0.5),
# A.RandomBrightnessContrast(brightness_limit=(-0.1, 0.1), contrast_limit=(-0.1, 0.1), p=0.5),

# A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),

train_transforms = T.Compose(
    [
        T.ToTensor()
    ]
)

test_transforms = T.Compose(
    [
        T.ToTensor()
    ]
)

train_data_path = '/home/guest/shared/Dataset/train_reduced'
test_data_path = '/home/guest/shared/Dataset/test'

train_image_paths = []
classes = []

for data_path in glob.glob(train_data_path + '/*'):
    classes.append(data_path.split('/')[-1])
    train_image_paths.append(glob.glob(data_path + '/*'))

train_image_paths = list(flatten(train_image_paths))
random.shuffle(train_image_paths)

test_image_paths = []
for data_path in glob.glob(test_data_path + '/*'):
    test_image_paths.append(glob.glob(data_path + '/*'))

test_image_paths = list(flatten(test_image_paths))

idx_to_class = {i:j for i, j in enumerate(classes)}
class_to_idx = {value:key for key, value in idx_to_class.items()}

class HighwayDataset(Dataset):
    def __init__(self, image_paths, transform=None):
        self.image_paths = image_paths
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        image_filepath = self.image_paths[idx]
        image = cv2.imread(image_filepath)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        label = image_filepath.split('/')[-2]
        label = class_to_idx[label]
        if self.transform is not None:
            image = self.transform(image)
        return image, label


train_dataset = HighwayDataset(train_image_paths, train_transforms)
# test_dataset = HighwayDataset(test_image_paths, test_transforms)


def dataloader():
    train_loader = DataLoader(
        train_dataset, batch_size=64, shuffle=True
    )

    # test_loader = DataLoader(
    #     test_dataset, batch_size=64, shuffle=False
    # )

    return train_loader
    #, test_loader


