import os
from typing import List

from file_sequence_detector import FileSequenceDetector

def list_files(dir_path)->List[str]:
    if os.path.isdir(dir_path):
        all_files = os.listdir(dir_path)    
    return all_files

test_dir = "C:\\gui2one\\3D\\houdini_19_playground\\render\\vellum_emit\\karma2"


all_files = list_files(test_dir)
detector = FileSequenceDetector(all_files)

detector.detect_file_sequences()

if len(detector.sequences): 
    print(f"Found {len(detector.sequences)} sequence(s)")
for seq in detector.sequences :
    print('\t', seq)

