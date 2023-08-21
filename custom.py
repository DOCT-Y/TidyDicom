from typing import Dict, Any


# reference: https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html
# Standard elements can be accessed by string and tuple, private elements can only be accessed by tuple
INFO_DICT = {'pname':'PatientName', 'pid':'PatientID', 'date':(0x0008, 0x0020), 'series_name':(0x0008, 0x103E), 'series_number':'SeriesNumber'}


def GetPathByInfo(info:Dict[str, Any]) -> str:
    # Set the dirname.
    # Suppose the full expected path of a dicom file to be 'C:\Users\J\Desktop\Jackson\20200202\arterial\IM123.dcm' and
    # the 'INFO_DICT' to be {'pname':'PatientName', 'date':(0x0008, 0x0020), 'series_name':(0x0008, 0x103E)}.
    # One got 'C:\Users\J\Desktop' as the root output folder and 'IM123.dcm' as the file name.
    # The 'info' returned by DicomReader.read() is {'pname':Jackson, 'date':'20200202', 'series_name':'arterial'}.
    # the function is supposed to return 'Jackson/20200202/arterial' by simply performing str join:
    #   '/'.join([str(info['pname']), info['date'], info['series_name']]) 

    pid = info['pid'] # no change
    pname = str(info['pname']).upper() # convert PersonName to str
    date = info['date'] # no change
    series_name = info['series_name'] if info['series_name'] else 'Unk_Series' # fill nan
    series_number = str(info['series_number']) # convert VI to str

    return '/'.join([pid+'_'+pname, date, series_number+'_'+series_name])