from os import listdir
from os.path import isfile, join
from typing import Dict, List, Tuple
import numpy as np
from imagehash_image_hash_fns import calculate_signature

def find_near_duplicates(input_dir: str, threshold: float, hash_fn: str, hash_size: int, bands: int) -> List[Tuple[str, str, float]]:
  """
  Find near-duplicate images
  
  Args:
    input_dir: Directory with images to check
    threshold: Images with a similarity ratio >= threshold will be considered near-duplicates
    hash_size: Hash size to use, signatures will be of length hash_size^2
    bands: The number of bands to use in the locality sensitve hashing process
      
  Returns:
    A list of near-duplicates found. Near duplicates are encoded as a triple: (filename_A, filename_B, similarity)
  """
  
  rows: int = int(hash_size**2/bands)
  signatures = dict()
  hash_buckets_list: List[Dict[str, List[str]]] = [dict() for _ in range(bands)]
  
  # Build a list of candidate files in given input_dir
  file_list = [join(input_dir, f) for f in listdir(input_dir) if isfile(join(input_dir, f))]

  # Iterate through all files in input directory
  for fh in file_list:
    try:
      signature = calculate_signature(fh, hash_fn, hash_size)
    except IOError:
      # Not a PIL image, skip this file
      continue

    # Keep track of each image's signature
    signatures[fh] = np.packbits(signature)
    
    # Locality Sensitive Hashing
    for i in range(bands):
      signature_band = signature[i*rows:(i+1)*rows]
      signature_band_bytes = signature_band.tobytes()
      if signature_band_bytes not in hash_buckets_list[i]:
        hash_buckets_list[i][signature_band_bytes] = list()
      hash_buckets_list[i][signature_band_bytes].append(fh)

  # Build candidate pairs based on bucket membership
  candidate_pairs = set()
  for hash_buckets in hash_buckets_list:
    for hash_bucket in hash_buckets.values():
      if len(hash_bucket) > 1:
        hash_bucket = sorted(hash_bucket)
        for i in range(len(hash_bucket)):
          for j in range(i+1, len(hash_bucket)):
            candidate_pairs.add(
                tuple([hash_bucket[i],hash_bucket[j]])
            )

  # Check candidate pairs for similarity
  near_duplicates = list()
  for cpa, cpb in candidate_pairs:
    hd = sum(np.bitwise_xor(
            np.unpackbits(signatures[cpa]), 
            np.unpackbits(signatures[cpb])
    ))
    similarity = (hash_size**2 - hd) / hash_size**2
    if similarity > threshold:
      near_duplicates.append((cpa, cpb, similarity))
          
  # Sort near-duplicates by descending similarity and return
  near_duplicates.sort(key=lambda x:x[2], reverse=True)
  return near_duplicates