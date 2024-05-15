import os
from PIL import Image
from typing import List, Tuple

def create_similarity_directory(similarity_list: List[Tuple[str, str, float]], output_directory: str) -> None:
  """
  Create a directory with images and text files for each pair of similar images.

  Args:
      similarity_list: List of tuples where each tuple contains (path_to_image_A, path_to_image_B, similarity_ratio).
      output_directory: Path to the directory where the output will be saved.

  Returns:
      None
  """
  # Create the output directory if it doesn't exist
  os.makedirs(output_directory, exist_ok=True)

  # Create subdirectories for images and text files
  image_directory = os.path.join(output_directory, "images")
  text_directory = os.path.join(output_directory, "text")
  os.makedirs(image_directory, exist_ok=True)
  os.makedirs(text_directory, exist_ok=True)

  # Iterate over the similarity list
  for index, (image1_path, image2_path, similarity) in enumerate(similarity_list):
    # Open the images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    # Concatenate images side by side
    combined_image = Image.new('RGB', (image1.width + image2.width, max(image1.height, image2.height)))
    combined_image.paste(image1, (0, 0))
    combined_image.paste(image2, (image1.width, 0))

    # Save the combined image
    combined_image_path = os.path.join(image_directory, f"pair_{index}.jpg")
    combined_image.save(combined_image_path)

    # Write similarity information to text file
    text_file_path = os.path.join(text_directory, f"pair_{index}.txt")
    with open(text_file_path, 'w') as text_file:
        text_file.write(f"Image 1: {image1_path}\n")
        text_file.write(f"Image 2: {image2_path}\n")
        text_file.write(f"Similarity: {similarity}\n")

    # Close the images
    image1.close()
    image2.close()

from typing import List, Tuple

def extract_duplicate_paths(near_duplicates: List[Tuple[str, str, float]]) -> List[str]:
    """
    Extract paths of duplicate images from a list of near-duplicate tuples.
    Only one image from each pair of duplicates is added to the list.

    Args:
        near_duplicates: List of tuples where each tuple contains (path_to_image_A, path_to_image_B, similarity_ratio).

    Returns:
        A list of paths to the duplicate images.
    """
    duplicate_paths = set()
    unique_images = set()

    for img_a, img_b, similarity in near_duplicates:
        if img_a not in unique_images:
            duplicate_paths.add(img_a)
            unique_images.add(img_a)
        if img_b not in unique_images:
            duplicate_paths.add(img_b)
            unique_images.add(img_b)
    
    return list(duplicate_paths)

def delete_images(image_paths: List[str]) -> None:
    """
    Delete images given a list of their paths.

    Args:
        image_paths: List of paths to images to be deleted.
    """
    for image_path in image_paths:
        try:
            if os.path.exists(image_path):
                os.remove(image_path)
                print(f"Deleted: {image_path}")
            else:
                print(f"File not found: {image_path}")
        except Exception as e:
            print(f"Error deleting {image_path}: {e}")