# update dependency
from pathlib import Path

from cv2 import cv2
import pandas as pd
# from google_drive_downloader import GoogleDriveDownloader as gdd
from tqdm import tqdm
datasetPath = Path('/mnt/ssd_ext/phongphu/nxq/self-built-masked-face-recognition-dataset')
maskPath = datasetPath/'AFDB_masked_face_dataset'
nonMaskPath = datasetPath/'AFDB_face_dataset'
maskDF = pd.DataFrame()
for subject in tqdm(list(nonMaskPath.iterdir()), desc='non mask photos'):
    for imgPath in subject.iterdir():
        image = cv2.imread(str(imgPath))
        maskDF = maskDF.append({
            'image': image,
            'mask': 0
            }, ignore_index=True)
for subject in tqdm(list(maskPath.iterdir()), desc='mask photos'):
    for imgPath in subject.iterdir():
        image = cv2.imread(str(imgPath))
        maskDF = maskDF.append({
            'image': image,
            'mask': 1
             }, ignore_index=True)
dfName = 'covid-mask-detector/data/mask_df.csv'
print(f'saving Dataframe to: {dfName}')
maskDF.to_csv(dfName)
