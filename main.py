from lsh import find_near_duplicates
from utils import create_similarity_directory, extract_duplicate_paths, delete_images

def main(input_dir: str, threshold: float, hash_fn: str, hash_size: int, bands: int, output_dir: str, delete: bool) -> None:
  try:
    near_duplicates = find_near_duplicates(input_dir, threshold, hash_fn, hash_size, bands)
    if len(near_duplicates) > 0:
      if delete:
        duplicates_paths = extract_duplicate_paths(near_duplicates)
        delete_images(duplicates_paths)
      else:
        print(f"Found {len(near_duplicates)} near-duplicate images in {input_dir} (threshold {threshold:.2%})")
        create_similarity_directory(near_duplicates, output_dir)
    else:
      print(f"No near-duplicates found in {input_dir} (threshold {threshold:.2%})")
  except OSError:
      print(f"Couldn't open input directory {input_dir}")


img_folders = [
  'dataset/train/images'
]

hash_fns = ["d", "a", "p", "h", "db", "c"]

input_dir = img_folders[0]
threshold = 0.70
hash_fn = hash_fns[2]
hash_size = 32
bands = 32
delete = True
output_dir = "results_00"

main(input_dir, threshold, hash_fn, hash_size, bands, output_dir, delete)