import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def main():
    print("--- 1. NumPy Array Fundamentals ---")
    array_1d = np.array([1.1, 9.2, 8.1, 4.7])
    print(f"1D Array Dimensions (Shape): {array_1d.shape}")
    print(f"Array Data Type: {array_1d.dtype}")
    
    array_2d = np.array([[1, 2, 3], [4, 5, 6]])
    print(f"2D Array Dimensions (Shape): {array_2d.shape}\n")

    print("--- 2. Image Representation as 3D Array ---")
    image_path = 'yummy_macarons.jpg'
    
    img = Image.open(image_path)
    img_array = np.array(img)
    
    print(f"Image Tensor Shape: {img_array.shape}") # (Height, Width, Color Channels)
    print(f"Total Dimensions (ndim): {img_array.ndim}")
    print(f"Pixel value range: Min={img_array.min()}, Max={img_array.max()}\n")

    print("--- 3. Processing Image Manipulations ---")
    
    inverted_img = 255 - img_array

    flipped_img = np.flip(img_array, axis=0)

    solarized_img = np.where(img_array < 100, 0, img_array)

    red_channel_img = img_array.copy()
    red_channel_img[:, :, 1] = 0  # Zero out Green channel
    red_channel_img[:, :, 2] = 0  # Zero out Blue channel

    print("Plotting Transformed Image Matrices...")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].imshow(img_array)
    axes[0, 0].set_title('Original Image')
    axes[0, 0].axis('off')

    axes[0, 1].imshow(inverted_img)
    axes[0, 1].set_title('Color Inverted (255 - Matrix)')
    axes[0, 1].axis('off')

    axes[1, 0].imshow(flipped_img)
    axes[1, 0].set_title('Vertically Flipped Matrix')
    axes[1, 0].axis('off')

    axes[1, 1].imshow(red_channel_img)
    axes[1, 1].set_title('Isolated Red Channel')
    axes[1, 1].axis('off')

    plt.tight_layout()
    print("Displaying transformed images. Close plot window to exit.")
    plt.show()

if __name__ == '__main__':
    main()