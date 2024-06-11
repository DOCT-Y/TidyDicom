# YUAN EN YU 20240610
# this version is used for MRI series.

from typing import Dict, Any
import re
import os

# reference: https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html
# Standard elements can be accessed by string and tuple, private elements can only be accessed by tuple
INFO_DICT = {
    'SOPClassUID':{
        'standard_name':'SOPClassUID', 
        'default_value':'NoSOPClassUIDTag'
        }, 
    'PatientName':{
        'standard_name':'PatientName', 
        'default_value':'NoPatientNameTag'
        }, 
    'PatientID':{
        'standard_name':'PatientID', 
        'default_value':'NoPatientIDTag'
        },
    'StudyDate':{
        'group_id':'0008', 
        'element_id':'0020', 
        'default_value':'NoStudyDateTag'
        }, 
    'SeriesDescription':{
        'group_id':'0008', 
        'element_id':'103E', 
        'default_value':'NoSeriesDescriptionTag'
        }, 
    'SeriesTime':{
        'group_id':'0008', 
        'element_id':'0031', 
        'default_value':'NoSeriesDescriptionTag'
        }
    }


invalid_pattern_replace = re.compile(r"""[/\\]""")
invalid_pattern_remove = re.compile(r"""[:?"<>|]""")


def GetPathByInfo(info:Dict[str, Any]) -> str:
    # Set the dirname.
    # Suppose the full expected path of a dicom file to be 'C:\Users\J\Desktop\Jackson\20200202\arterial\IM123.dcm' and
    # the 'INFO_DICT' to be {'pname':'PatientName', 'date':(0x0008, 0x0020), 'series_description':(0x0008, 0x103E)}.
    # One got 'C:\Users\J\Desktop' as the root output folder and 'IM123.dcm' as the file name.
    # The 'info' returned by DicomReader.read() is {'pname':Jackson, 'date':'20200202', 'series_description':'arterial'}.
    # the function is supposed to return 'Jackson/20200202/arterial' by simply performing str join:
    #   '/'.join([str(info['pname']), info['date'], info['series_description']]) 
    
    pid = info['PatientID'] # no change

    pname = info['PatientName'].components # PearsonName object, return tuple
    pname = ''.join(pname).lower().replace(' ', '')

    date = info['StudyDate'] # no change

    series_dirname = os.path.join(pid+'_'+pname, date)

    if info['SOPClassUID'] == '1.2.840.10008.5.1.4.1.1.4': # 'MR Image Storage'
        series_description = info['SeriesDescription'] if info['SeriesDescription'] else 'Unk_Series' # fill nan
        series_description = series_description.replace('*', ' star')
        series_description = invalid_pattern_replace.sub('_', series_description)
        series_description = invalid_pattern_remove.sub('', series_description)
        series_time = info['SeriesTime']
        series_name = series_description+'@'+series_time
    else:
        series_name = 'raw_data_storage'

    return os.path.join(series_dirname, series_name)