# TidyDicom

TidyDicom is a simple program based on Python . It can categorize all DICOM files in the root directory into specific folders. 

Welcome any issues and PR. 

![Python](https://img.shields.io/badge/python-v3.8-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-GPL3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Release

The Windows version based on embeddable Python is uploaded. It can run without python pre-installed.

## Requirement

The below modules must be installed first to make the TidyDicom work. 

```
- pydicom=2.4.3
- tqdm=4.66.4
```

## Quick Start

<p align="center">
  <img src="https://github.com/DOCT-Y/TidyDicom/blob/main/overview.png" width="600" height="300">
</p>

Suppose that we have a root folder full of DICOM files and we need to categorize these DICOM files into specific folders. For example, if we want the first layer of the directory tree to be the patient's name and patient's ID, the second layer to be the study date, and the second layer to be the series description. DICOM files with the same patient's name, patient's ID, study date, and series description will go to the same folder.

### customize the code

Open the `custom.py` file:

Firstly, we need to tell the program which DICOM data element to read to get the informations. 

```python
INFO_DICT = {
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
        }
    }
```

We defined a Python dictionary in which the keyword is a string of anything and the value is used to get the tag information.

Standard DICOM data elements can be accessed by standard keyword like `PatientName` for  `(0010,0010) Patient's Name` and `PatientID` for `(0010,0020) | Patient ID` . It can also be accessed by group number and element number like `group_id=0008, element_id=0020` for `(0008,0020) Study Date` and `group_id=0008, element_id=103E` for `(0008,103E) Series Description` . 

Private DICOM data elements can only be accessed by group number and element number.

A list of keywords for all standard elements can be found [here](https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html).

The program uses the `INFO_DICT` and returns a Python dictionary `info` containing the element informations.

Secondly, we need to tell the program what is the rule to categorize the DICOM files.

```python
def GetPathByInfo(info:Dict[str, Any]) -> str:
    pid = info['PatientID'] # no change

    pname = info['PatientName'].components # PearsonName object, return tuple
    pname = ''.join(pname).lower().replace(' ', '')

    date = info['StudyDate'] # no change

    series_description = info['SeriesDescription'] # no change

    return os.path.join(id+'_'+pname, date, series_name) # using os.path.join is a safe method for all OS.
```

Suppose a DICOM file is named `1234.dcm` and the program read it and returns the `info = {'PatientName':'Jackson', 'PatientID':'111111', 'StudyDate':20211202, 'SeriesDescription':'arterial'}`. The function above will return `'111111_Jackson/20211202/arterial'`. Finally the file will be move to `'./111111_Jackson/20211202/arterial/1234.dcm'`.

### Set the arguments

Open the `config.json` file:

we need to tell the program where is the root folder and where we want to move the DICOM files to.

```json
{
    "in_dir": "C:\\Users\\J\\Desktop\\mess",
    "out_dir": "C:\\Users\\J\\Desktop\\clean",
    "copy_or_cut": "copy", 
    "custom_file":"custom", 
    "batch_size":2000
}
```

The `in_dir` is the root folder of your unsorted DICOM files. The `out_dir` is the root folder of your sorted DICOM files. `copy_or_cut` defines the method when moving the files, by either `shutil.copy` or `shutil.move`. `custom_file` is the filename of the custom.py. You can write different custom files (e.g., `custom_a` for `custom_a.py`, `custom_b` for `custom_b.py`) to handle different DICOMs. `batch_size` is the number of files processed in one batch.

### Run

Run the `main.py` and the program will start to work.

The terminal will display the process bar batch by batch.

When any error occurs, a `failures.csv` will be stored in `out_dir` logging the filepath and error information.

## Embeddable Version

1. download `TidyDicom.zip` and unzip it.
2. modify `custom.py` and `config.json`.
3. double click `run.bat`

## License 

This project is licensed under the GPL 3.0 License

