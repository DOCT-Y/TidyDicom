from typing import Dict, Union, Any
import os
import shutil
import json

import pydicom

from custom import INFO_DICT, GetPathByInfo


class DicomReader:
    def __init__(self, info_dict:Dict[str, Union[tuple, str]]) -> None:
        self._info_dict = info_dict
    
    def read(self, dcm_path:str) -> Dict[str, Any]:
        ds = pydicom.dcmread(dcm_path)

        info = {}
        for k,v in self._info_dict.items():
            try:
                if isinstance(v, str):
                    info.update({k:ds[v].value})
                elif isinstance(v, tuple):
                    info.update({k:ds[v[0], v[1]].value})
                else:
                    raise TypeError('the tag should be accessed by either "str" or "tuple".')
            except KeyError:
                info.update({k:'unk'})

        return info


def tidy_up(in_root:str, out_root:str) -> None:
    dcmreader = DicomReader(INFO_DICT)
    for dirpath, dirnames, filenames in os.walk(in_root):
        for filename in filenames:
            try:
                origination = os.path.join(dirpath, filename)
                info = dcmreader.read(origination)
                destination_dirpath = os.path.join(out_root, GetPathByInfo(info))
                
                if not os.path.exists(destination_dirpath):
                    os.makedirs(destination_dirpath)
                
                destination = os.path.join(destination_dirpath, filename)
                while os.path.exists(destination):
                    destination = os.path.join(destination_dirpath, '1' + filename)
                
                shutil.move(origination, destination)

            except pydicom.errors.InvalidDicomError:
                pass


def fast_tidy_up(in_root:str, out_root:str) -> None:
    dcmreader = DicomReader(INFO_DICT)
    for dirpath, dirnames, filenames in os.walk(in_root):
        if not dirnames: # is the leaf node
            filename = filenames[0]
            info = dcmreader.read(os.path.join(dirpath, filename))
            origination = dirpath
            destination = os.path.join(out_root, GetPathByInfo(info))
            
            while os.path.exists(destination):
                destination = destination + '1'
            
            shutil.move(origination, destination)


if __name__ == '__main__':
    with open('./config.json', 'r') as f:
        args = json.load(f)

    if args['fast']:
        fast_tidy_up(args['in_dir'], args['out_dir'])
    else:
        tidy_up(args['in_dir'], args['out_dir'])