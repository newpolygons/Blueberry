# Functions for converting image sequence to video and any other issues along the way.


import cv2
import os

def imagesToVideo(image_folder, output_path, fps=24):
    """Converts a folder of images into a video."""

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
    images.sort()  # Ensure images are in the desired order

    if not images:
        print("No images found in the folder.")
        return

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, _ = frame.shape

    video = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        img = cv2.imread(os.path.join(image_folder, image))
        video.write(img)

    video.release()
    print("Video created successfully!")


def clearImagesFolder(imageDirectory):
    return


def changeCSSColors():
    return

'''
if __name__ == "__main__":
    image_folder = "your_image_folder"
    output_path = "output_video.mp4"
    images_to_video(image_folder, output_path)
'''