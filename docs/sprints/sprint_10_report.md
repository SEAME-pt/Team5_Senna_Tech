# 🚀 Sprint 10 Report – Team5: Senna Tech

**Duration:** [23/03/2026] → [03/04/2026]

**Sprint Goal:** Complete the pipeline from model inference to post-processed output for control integration

---

## 🎯 Objectives for this Sprint

### GOAL 1 - Post-Processing Setup .hef
- Analyze the differences between the .pt and .hef outputs.
- Prepare the data for the control module.

### GOAL 2 - PID Control
- Adapt the code to run on the microcontroller
- Test and tune parameters
- Manual/Automatic Feature implementation

### GOAL 3 - Object Detection Exploration and initial Setup
- Understand and start developing the object detection pipeline and define initial target objects for detection.
- Bounding boxes, confidence scores, and classes.


#### Complementary Tasks
- MPC (Model predective control) SPIKE
- Reorganize PCs storage to free up space for work.
---

**Team Roles:**
| Name            | Responsibilities                          |
|-----------------|-------------------------------------------|
| Hellom          | AI/ML Integration                         |
| Vinicius        | AI/ML Integration                         |
| Jose            | PID                                       |
| Yasmine         | AI/ML Integration                         |
| Marcelo         | Object detection                          |

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+10)

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **23/03** | The team met to plan sprint 10, define the goals and split tasks **Hellom, Vinicius and Yasmine:** Going to study the problems envolving the post processing .hef with yolov8s **Marcelo:** Will start studies about object detection models **Jose:** PID control to STM. |
| **24/03** | The team identified flaws in the current lane detection model when it was tested with real images from our track, so a small replanning and redistribution of tasks was carried out. **Hellom, Vinicius:** Both are trying to better understand the .hef output and the compatibility of different models with the Hailo-8. Study of the tensor outputs from the YOLOv8s .hef, the calculations that need to be performed, and refinement of the post-processing on the Raspberry Pi. **Marcelo, Yasmine:** Working together with members of other teams to create the dataset for our track. **Jose:** Focus in Exam |
| **25/03** | | The team is currently starting the work of creating the new dataset for this year’s track. Work is also ongoing on the analysis of the .hef output, as well as research and testing with different models on Hailo. **Hellom:** Study and tests on the behavior of different models and their behavior in the .hef for post-processing. **Vinicius:** Continuation of studies on the output of YOLOv8-Seg in the .hef. First binary mask obtained. **Marcelo, Yasmine:** Working together with members of other teams to create the dataset for our track. **Jose:** Focus in Exam |
| **26/03** | **Hellom:** Review Hailo runtime examples, and built a simple main.py to test the parser while evaluating Python vs C++ post processing options.  **Vinicius:** Meta-Hailo-Tappas integration in AGL  **Marcelo, Yasmine:** Working together with members of other teams to create the dataset for our track. **Jose:** STM bug fix |
| **27/03** | **Hellom:** Conversion of our new yolos LKA models to .hef  **Marcelo:** Training yolov26s_seg with last year seame dataset  **Vinicius:** Study about Tappas integrations in AGL, problemas with opencv and libgsthailo versions incompatibility  **Jose:** STM bug fix **Yasmine:** Training Yolov8s_seg with last year sea:me dataset |
| **30/03** | **Hellom:** Study and research on the support and deployment possibilities of YOLOv8 segmentation on Hailo hardware. **Marcelo:** Wornking on Yolov26 model  **Vinicius:** Study and implement gstreamer integration in pipeline to obtain camera real time frames  **Jose:** STM bug is fixed, new pull request done **Yasmine:** Fixing errors in the LKA post processing inside raspberry that are not generating the correct output in the .hef |
| **31/03** | **Hellom:** Working on Yolov26s conversion **Marcelo:** Training of the YOLOv25n version.  **Vinicius:** Tests with videos and camera using yolov8s .hef **Jose:** Migratin PID C++ to C to work on STM **Yasmine:** Study on improving post-processing and fixing errors in line crossings and loss of line reference. |
| **01/04** | **Hellom:** Due to size issues with YOLOv26s, attempting to convert YOLOv26n instead. **Marcelo:** Research on the integration and operation of multiple models on Hailo and initial object detection researches  **Vinicius:** Camera Real time integration with LKA pipeline **Jose:** PID integrated and initial tests with joystick using PID to throotle the car **Yasmine:** Improvements in post-processing code within the Raspberry Pi pipeline. |
| **02/04** | sprint restrospective. |
---

## 🧠 Key Achievements
- Integrated end-to-end pipeline: Camera → Model Inference → Post-Processing.
- Model testing: YOLOv8s segmentation and YOLOv8n segmentation; FPS and resource consumption measured with full pipeline.
- Model improvements: Significant performance boost after retraining with more complete datasets, including last year’s track frames.
- PID integration: PID controller integrated with STM and briefly tested with joystick acceleration.

---