import re
import os
from typing import List


from dataclasses import dataclass

@dataclass
class IFileSequence :
    num_files : int
    name_pattern : str
    start_number : int

class FileSequenceDetector :
    
    all_files : List[str]
    sequences : List[IFileSequence]
    
    def __init__(self, all_files : List[str]):
        self.all_files = all_files
        self.sequences = []
        
    def detect_file_sequences(self):
        max_tries = 10
        num_tries = 0
        while len(self.all_files):
            first_file = self.all_files[0]
            # print("all files : ")
            # print(self.all_files)
            matches = re.findall(r'\d+', first_file)
            
            r = re.compile(r'\d+')
            ranges =[[m.start(),m.end()] for m in r.finditer(first_file)]
            
            assert len(matches) == len(ranges) 
            
            num_pattern = None

            if len(ranges) :
                num_pattern = matches[len(matches)-1] # assume sequence numbers are the last numbers in file name 

            if num_pattern != None :
                
                parts = first_file.split(num_pattern)


                num_files = 0
                indices_to_delete = []
                for i, file in enumerate(self.all_files) :
                    r = re.compile(f'{parts[0]}\d+{parts[1]}')
                    ranges =[[m.start(),m.end()] for m in r.finditer(file)]
                    if len(ranges):
                        
                        num_files += 1
                        indices_to_delete.append(i)
                
                
                for i, file in reversed(list(enumerate(self.all_files))):
                    r = re.compile(f'{parts[0]}\d+{parts[1]}')
                    ranges =[[m.start(),m.end()] for m in r.finditer(file)]

                        
                def keep_function(item):
                    
                    parts = first_file.split(num_pattern)

                    if len(parts) < 2 : return True
                    r = re.compile(f'{parts[0]}\d+{parts[1]}')
                    ranges =[[m.start(),m.end()] for m in r.finditer(item)]            

                    return len(ranges) == 0
                
                filtered = filter(keep_function, self.all_files)
                
                self.all_files = list(filtered)
                                
                final_pattern = f'{parts[0]}%0{len(num_pattern)}d{parts[1]}'
                final_path = os.path.join(final_pattern)
                final_path = final_path.replace("\\", "/")
                
                result_sequence = IFileSequence(num_files, final_pattern, int(num_pattern) )


                self.sequences.append(result_sequence)
                
            num_tries += 1
            if num_tries > max_tries : break
   