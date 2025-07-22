import pydicom
from tqdm import tqdm

import importlib
import json
import os
import shutil
import time


class DicomTag:
    def __init__(self, standard_name:str=None, group_id:str=None, element_id:str=None, is_file_meta:bool=False, default_value=None) -> None:
        '''
        standard_name: str, default=None
        standard dicom date element keyword, reference at https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html

        group_id: str, default=None
        the first hex number of the data element, for example, '0008' for SOP Instance UID (0x0008, 0x0018)

        element_id: str, default=None
        the second hex number of the data element, for example, '0018' for SOP Instance UID (0x0008, 0x0018)

        is_file_meta: bool, default=False
        if True, the tag is search in file_meta elements

        default_value: default=None
        the default value of this tag. when error occurs, return the default value
        '''
        if standard_name is not None:
            self.standard_name = standard_name
            if is_file_meta:
                self.get_value_method = self.get_metavalue_by_name
            else:
                self.get_value_method = self.get_value_by_name
        elif group_id is not None and element_id is not None:
            self.group_id = int(str(group_id), 16)
            self.element_id = int(str(element_id), 16)
            if is_file_meta:
                self.get_value_method = self.get_metavalue_by_id
            else:
                self.get_value_method = self.get_value_by_id

        self.default_value = default_value
    
    def get_metavalue_by_name(self, ds):
        return ds.file_meta.__getattr__(self.standard_name)
    
    def get_metavalue_by_id(self, ds):
        return ds.file_meta.__getitem__((self.group_id, self.element_id)).value
    
    def get_value_by_name(self, ds):
        return ds.__getattr__(self.standard_name)
    
    def get_value_by_id(self, ds):
        return ds.__getitem__((self.group_id, self.element_id)).value

    def get_value(self, ds):
        try:
            value = self.get_value_method(ds)
        except AttributeError:
            value = self.default_value
        
        return value
    

def tidy_up(in_dir:str, out_dir:str, copy_or_cut:str, custom_file:str, batch_size:int) -> None:
    def process(work_list):
        batch_failures = []

        with tqdm(work_list) as pbar:
            for dirpath, dicom_file in pbar:
                try:
                    dcm = pydicom.dcmread(os.path.join(dirpath, dicom_file))

                    info = {k: v(dcm) for k, v in value_extractor.items()}

                    src = os.path.join(dirpath, dicom_file)
                    destination_dirpath = os.path.join(out_dir, GetPathByInfo(info))
                    os.makedirs(destination_dirpath, exist_ok=True)

                    if os.path.exists(os.path.join(destination_dirpath, dicom_file)):
                        file_root, ext = os.path.splitext(dicom_file)  
                        timestamp = time.strftime('%Y%m%d%H%M%S')  
                        dst = os.path.join(destination_dirpath, f"{file_root}_{timestamp}{ext}")
                    else:
                        dst = os.path.join(destination_dirpath, dicom_file)
                    
                    move_func(src, dst)

                except pydicom.errors.InvalidDicomError:
                    continue
                except Exception as e:
                    batch_failures.append([dirpath, dicom_file, repr(e)])
        
        return batch_failures

                
    custom = importlib.import_module(custom_file)
    value_extractor = {k: DicomTag(**v).get_value for k,v in custom.INFO_DICT.items()}
    GetPathByInfo = custom.GetPathByInfo

    if copy_or_cut == 'cut':
        move_func = shutil.move
    else:
        move_func = shutil.copy

    work_list = []
    failures = []
    for dirpath, _, filenames in os.walk(in_dir):
        for filename in filenames:
            work_list.append([dirpath, filename])
        
        if len(work_list) > batch_size:
            failures += process(work_list)
            work_list = []

    if len(work_list) != 0:
        failures += process(work_list)
        work_list = []

    if len(failures) > 0:
        failure_dir = os.path.join(out_dir, 'failures.csv')
        with open(failure_dir, 'w') as f:
            f.write(f'dirpath,filename,error_info\n')

            for dirpath, filename,error_info in failures:
                f.write(f'{dirpath},{filename},{error_info}\n')
        
        print(f'failure files log saved at {failure_dir}')


if __name__ == '__main__':
    with open('./TidyDicom/config.json', 'r') as f: # portable version
        args = json.load(f)

    # with open('./config.json', 'r') as f:
    #     args = json.load(f)

    tidy_up(**args)
