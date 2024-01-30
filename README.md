# Vehicle_counting_tracking_in_a_roundabout
Detecting and tracking the vehicles in ["car", "bus/truck", "motorbike"].

## Dependencies
- ubuntu/windows
- cuda>=10.0
- python>=3.6
- `pip3 install -r requirements.txt`

## Usage
1. Run `python3 app.py` ;
2. Select video and double click the image to select area, and then start;
3. After detecting and tracking, the result video and file are saved under `results` directory, the line of `results.txt` with format \[videoName,id,objectName] for each vehicle.
