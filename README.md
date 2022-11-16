# Construction Site Hazards Identification Based on Computer Vision and Deep Learning

This project is a partial fulfillment of the requirements for the degree of Master of Science in Computer Science.

Special Thanks for my supervisor Dr. Mona Abdelbaset Sadek Ali for her continuous support.

Model YOLO-v5 was taken from the original author [Github repository](https://github.com/ultralytics/yolov5)

## Getting Started

In the terminal, cd to the project file and install all the required packagaes by running the following line:

```bash
pip install -qr requirements.txt
```

#### Run the detection model

you can run the detection model by running the following line: 

```bash
python3 detect.py --weight PPE_HE.pt --source 0
```
--weight PPE_HE.pt is used to detect workers/PPE.
you can change the weight to: 
- HE_weights.pt to detect heavy equipment.
- PPE_HE.pt to detect workers/PPE and heavy equipment.

--source 0 runs detection from the webcam.
you can change the value to images or videos. 

