import os
import shutil

def get_file_starts(folder):
    files = os.listdir(folder)
    file_starts = {}
    for f in files:
        name, ext = os.path.splitext(f)
        file_starts[f] = name  # Full name without extension
    return file_starts

def copy_matching_files(source_folder, compare_folder, dest_folder, image_exts=('.jpg', '.jpeg', '.png', '.gif')):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    source_files = get_file_starts(source_folder)
    compare_files = get_file_starts(compare_folder)

    for src_file, src_start in source_files.items():
        for cmp_file, cmp_start in compare_files.items():
            if cmp_start.startswith(src_start) and src_file.lower().endswith(image_exts):
                src_path = os.path.join(source_folder, src_file)
                dest_path = os.path.join(dest_folder, src_file)
                print(f"Copying: {src_file} → {dest_folder}")
                shutil.copy2(src_path, dest_path)
                break  # Avoid copying the same file multiple times

# Example usage:
if __name__ == "__main__":
    folder1 = r"C:\Users\maxmi\Documents\Swinburne\DEGREE\Y2S1\COS30018 INTELLIGENT SYSTEMS\testbatch\phyllis_carimages\carplate_annotation_raw_img"     # Folder with images
    folder2 = r"C:\Users\maxmi\Documents\Swinburne\DEGREE\Y2S1\COS30018 INTELLIGENT SYSTEMS\testbatch\phyllis_annotation\filtered_labels" # Folder to compare names
    destination = r"C:\Users\maxmi\Documents\Swinburne\DEGREE\Y2S1\COS30018 INTELLIGENT SYSTEMS\testbatch\phyllis_filteredimages"

    copy_matching_files(folder1, folder2, destination)