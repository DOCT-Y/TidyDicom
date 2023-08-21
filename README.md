# TidyDicom

TidyDicom is a simple program based on Python . It can categorize all DICOM files in the root directory into specific folders. 

Welcome any issues and PR. 

![Python](https://img.shields.io/badge/python-v3.7-blue.svg)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-GPL3.0-blue.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)

## Release

The Windows version based on embeddable Python is uploaded. It can run without python pre-installed.

## Requirement

The below modules must be installed first to make the TidyDicom work. 

```
- pydicom=2.3.1
```

## Quick Start

Suppose that we have a root folder full of DICOM files and we need to categorize these DICOM files into specific folders. For example, if we want the first layer of the directory tree to be the patient's name and patient's ID, the second layer to be the study date, and the second layer to be the series description. DICOM files with the same patient's name, patient's ID, study date, and series description will go to the same folder.

### customize the code

Open the `custom.py` file:

Firstly, we need to tell the program which DICOM data element to read to get the informations. 

```python
INFO_DICT = {'pname':'PatientName', 'pid':'PatientID', 'date':(0x0008, 0x0020), 'series_description':(0x0008, 0x103E)}
```

We defined a Python dictionary in which the keyword is a string of anything and the value is used to get the tag information.

Standard DICOM data elements can be accessed by string keyword like `PatientName` for  `(0010,0010) Patient's Name` and `PatientID` for `(0010,0020) | Patient ID` . It can also be accessed by group number and element number like `(0x0008, 0x0020)` for  `(0008,0020) Study Date` and `(0x0008, 0x103E)` for `(0008,103E) Series Description` . 

Private DICOM data elements can only be accessed by group number and element number. For example, the b values of DWI images are usually private in DICOM files.

A list of keywords for all standard elements can be found [here](https://dicom.nema.org/medical/dicom/current/output/chtml/part06/chapter_6.html).

The program uses the `INFO_DICT` and returns a Python dictionary `info` containing the element informations.

Secondly, we need to tell the program what is the rule to categorize the DICOM files.

```python
def GetPathByInfo(info:Dict[str, Any]) -> str:
    pid = info['pid'] # no change
    pname = str(info['pname']).upper() # convert PersonName to str
    date = info['date'] # no change
    series_name = info['series_name'] if info['series_name'] else 'Unk_Series' # fill nan

    return '/'.join([pid+'_'+pname, date, series_name])
```

Suppose a DICOM file is named `1234.dcm` and the program read it and returns the `info = {'pname':'Jackson', 'pid':'111111', 'date':20211202, 'series_description':'arterial'}`. The function above will return `'111111_Jackson/20211202/arterial'`. Finally the file will be move to `'./111111_Jackson/20211202/arterial/1234.dcm'`.

### Set the arguments

Open the `config.json` file:

we need to tell the program where is the root folder and where we want to move the DICOM files to.

```json
{
    "in_dir": "C:\\Users\\J\\Desktop\\mess",
    "out_dir": "C:\\Users\\J\\Desktop\\clean",
    "fast": false
}
```

If `fast` is `true`, it means the dicom files are all located in the leaf nodes of `in_dir` directory tree and all files in the last branch are of the same `SeriesInstanceUID`.  While tidying up, the program will only read the first file and the whole folder will be move to the new place.

### Run

Run the `main.py` and the program will start to work.

## Embeddable Version

1. download `TidyDicom.zip` and unzip it.
2. modify `custom.py` and `config.json`.
3. double click `run.bat`

## License 

This project is licensed under the GPL 3.0 License

