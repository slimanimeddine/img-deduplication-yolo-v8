import imagehash
import numpy as np
from PIL import Image

def difference_hash(image_file: str, hash_size: int) -> np.ndarray:
  """ 
  Calculate the Difference hash signature of a given file
  
  Args:
    image_file: the image (path as string) to calculate the signature for
    hash_size: hash size to use, signatures will be of length hash_size^2
  
  Returns:
    Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
  """
  pil_image = Image.open(image_file).convert("L").resize(
                      (hash_size+1, hash_size),
                      Image.Resampling.LANCZOS)
  hash = imagehash.dhash(pil_image, hash_size)
  signature = hash.hash.flatten()
  pil_image.close()
  return signature

def average_hash(image_file: str, hash_size: int) -> np.ndarray:
  """ 
  Calculate the Average hash signature of a given file
  
  Args:
    image_file: the image (path as string) to calculate the signature for
    hash_size: hash size to use, signatures will be of length hash_size^2
  
  Returns:
    Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
  """
  pil_image = Image.open(image_file).convert("L").resize(
                      (hash_size, hash_size),
                      Image.Resampling.LANCZOS)
  hash = imagehash.average_hash(pil_image, hash_size)
  signature = hash.hash.flatten()
  pil_image.close()
  return signature

def perceptual_hash(image_file: str, hash_size: int) -> np.ndarray:
  """ 
  Calculate the Perceptual hash signature of a given file
  
  Args:
    image_file: the image (path as string) to calculate the signature for
    hash_size: hash size to use, signatures will be of length hash_size^2
  
  Returns:
    Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
  """
  pil_image = Image.open(image_file).convert("L").resize(
                      (hash_size, hash_size),
                      Image.Resampling.LANCZOS)
  hash = imagehash.phash(pil_image, hash_size)
  signature = hash.hash.flatten()
  pil_image.close()
  return signature


def haar_wavelet_hash(image_file: str, hash_size: int) -> np.ndarray:
  """ 
  Calculate the Haar wavelet hash signature of a given file
  
  Args:
    image_file: the image (path as string) to calculate the signature for
    hash_size: hash size to use, signatures will be of length hash_size^2
  
  Returns:
    Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
  """
  pil_image = Image.open(image_file).convert("L").resize(
                      (hash_size, hash_size),
                      Image.Resampling.LANCZOS)
  hash = imagehash.whash(pil_image, hash_size)
  signature = hash.hash.flatten()
  pil_image.close()
  return signature

def daubechies_wavelet_hash(image_file: str, hash_size: int) -> np.ndarray:
  """ 
  Calculate the Daubechies wavelet hash signature of a given file
  
  Args:
    image_file: the image (path as string) to calculate the signature for
    hash_size: hash size to use, signatures will be of length hash_size^2
  
  Returns:
    Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
  """
  pil_image = Image.open(image_file).convert("L").resize(
                      (hash_size, hash_size),
                      Image.Resampling.LANCZOS)
  hash = imagehash.whash(pil_image, hash_size, mode='db4')
  signature = hash.hash.flatten()
  pil_image.close()
  return signature

def color_hash(image_file: str, hash_size: int) -> np.ndarray:
  """ 
  Calculate the HSV Color hash signature of a given file
  
  Args:
    image_file: the image (path as string) to calculate the signature for
    hash_size: hash size to use, signatures will be of length hash_size^2
  
  Returns:
    Image signature as Numpy n-dimensional array or None if the file is not a PIL recognized image
  """
  pil_image = Image.open(image_file).convert("L").resize(
                      (hash_size, hash_size),
                      Image.Resampling.LANCZOS)
  hash = imagehash.colorhash(pil_image, hash_size)
  signature = hash.hash.flatten()
  pil_image.close()
  return signature

def calculate_signature(image_file: str, hash_fn: str, hash_size: int):
  """
  Compute the hash of an image
  
  Args:
    image_file: path to the image file
    hash_fn: the hash function to use: d, a, p, h, db, c

  Returns:
    the hash of the feature description
  """

  match hash_fn:
    case "d":
      return difference_hash(image_file, hash_size)
    case "a":
      return average_hash(image_file, hash_size)
    case "p":
      return perceptual_hash(image_file, hash_size)
    case "h":
      return haar_wavelet_hash(image_file, hash_size)
    case "db":
      return daubechies_wavelet_hash(image_file, hash_size)
    case "c":
      return color_hash(image_file, hash_size)
    case _:
      raise ValueError("Invalid hash function")