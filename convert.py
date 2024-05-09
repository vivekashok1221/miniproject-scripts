import time
from pathlib import Path
from collections import Counter

import matplotlib.pyplot as plt
import nibabel as nib
import pydicom


def convert_nii_to_png(nii_file: Path, output: Path) -> None:
    img = nib.load(nii_file)
    data = img.get_fdata()
    print(img.get_filename())
    # print(f"Creating {data.shape[0]} slices\n")
    # for i in range(data.shape[0]):
    i = 120
    print(f"{output}.jpg")
    plt.imshow(data[i, :, :], cmap="gray")
    plt.axis("off")
    plt.savefig(f"{output}.jpg")
    plt.close()


def convert_dcm_to_png(dcm_file: Path, output: Path) -> None:
    dicom_data = pydicom.dcmread(dcm_file)
    pixel_array = dicom_data.pixel_array

    plt.imshow(pixel_array, cmap="gray")
    plt.axis("off")

    output_path = output / f"{dcm_file.stem}.png"
    plt.savefig(output_path)
    plt.close()


def convert(root_dir: Path) -> None:
    count = Counter()
    for subject in root_dir.iterdir():
        print(f"subject: {subject.stem}")
        for dirpath, dirnames, filenames in subject.walk():
            if filenames:
                count[str(len(filenames))] += 1
            for filename in filenames:
                if filename.endswith(".nii"):
                    # output = root_dir / "output" / subject.stem / filename.removesuffix(".nii")
                    output = root_dir / "output"
                    output.mkdir(parents=True, exist_ok=True)
                    output = root_dir / "output" / filename.removesuffix(".nii")
                    convert_nii_to_png(dirpath / filename, output)
                    print()
                elif filename.endswith(".dcm"):
                    output = root_dir / "output" / subject.stem / dirpath.stem
                    output.mkdir(parents=True, exist_ok=True)
                    convert_dcm_to_png(dirpath / filename, output)
        print()
    print(count)


data_root_directory = input() or "/home/vivek/Programs/miniproject/miniproject-scripts/datasets/ADNI/ADNI"
start = time.perf_counter()
convert(Path(data_root_directory))
print(time.perf_counter() - start)


