# 🚀 Sprint 9 Report – Team5: Senna Tech

**Duration:** [09/03/2026] → [20/03/2026]

**Sprint Goal:** Define the initial architecture of our ADAS

**Team Roles:**
| Name            | Responsibilities                          |
|-----------------|-------------------------------------------|
| Hellom          | Hailo HAT                                 |
| Vinicius        | PID                                       |
| Jose            | PID                                       |
| Yasmine         | Scrum Master / LKA developer              |
| Marcelo         | CARLA developer                           |

---

## 🎯 Objectives for this Sprint

- Define the model of LKA to be used.
- Study CARLA in more depth, test more inputs, and define the desired output for the training.
- Start PID development.
- Understand the workflow with Hailo.

---

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83)

---

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **09/03** | The team met to plan sprint 9. **Hellom:** going to study the problems we're having at Hailo. **Marcelo:** advance in CARLA's studies **Vinicius:** Day off (worked at the carnival) **Jose:** transcendence study **Yasmine:** Filter final LKA model options. |
| **10/03** | **Hellom:** Verify compatibility between LKA models and .hef compilation for use in hailo. **Marcelo:** to understand how we extract a specific dataset from CARLA to train the LKA model we will use. **Vinicius:** Day off (worked at the carnival) **Jose:** PID **Yasmine:** Understanding what is needed to use the yolov8-seg as our initial training model for LKA. |
| **11/03** | **Hellom:** See how to convert the code to .hef.  **Marcelo:** testing pre-trained models in CARLA  **Vinicius:** Day off (worked at the carnival)  **Jose:** PID **Yasmine:** organize public dataset. |
| **12/03** | **Hellom:** Perform the first conversion of the trained model to .hef.  **Marcelo:** Extract dataset from CARLA  **Vinicius:** Day off (worked at the carnival)  **Jose:** PID **Yasmine:** train model with vill-100 and CULane(public dataset). |
| **13/03** | **Hellom:** Convert our second trained model to .hef and organize the conversion scripts.  **Marcelo:** testing the first model in the car.  **Vinicius:** Day off (worked at the carnival)  **Jose:** PID **Yasmine:** Organize the public dataset + the CARLA dataset for training with the larger dataset and with more epochs and batchs. |
| **16/03** | **Hellom:** Integration of the .hef conversion into hailo. **Marcelo:** Integration of the first trained model in the CARLA simulator.  **Vinicius:** Day off (worked at the carnival)  **Jose:** PID **Yasmine:** Organization of the CARLA dataset and study of new training parameters. |
| **17/03** | **Hellom:** post-processing study of .hef files. **Marcelo:** Comparison between models trained within the CARLA environment.  **Vinicius:** Day off (worked at the carnival)  **Jose:** PID **Yasmine:** Developing pipeline code for image processing. |
| **18/03** | **Hellom:** post-processing study of .hef files. **Marcelo:** Adaptation of the PID code for use in the CARLA API.  **Vinicius:** Adaptation of the PID code for use in the CARLA API. **Jose:** PID **Yasmine:** Developing pipeline code for image processing. |
| **19/03** | **Hellom:** post-processing study of .hef files. **Marcelo:** Adaptation of the PID code for use in the CARLA API.  **Vinicius:** PID test in the car. **Jose:** PID **Yasmine:** adaptation of the output values ​​of the image post-processing code. |
| **20/03** | sprint restrospective. |
---

## 🧠 Key Achievements

- Defined YOLOv8n-sec model, training versions, model integration and PID in the Carla simulator.

---

## ⚙️ Pending for next sprint

-
