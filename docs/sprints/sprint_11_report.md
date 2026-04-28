# 🚀 Sprint 11 Report – Team5: Senna Tech

**Duration:** [13/04/2026] → [24/04/2026]

**Sprint Goal:** Integrate PID (steering) with Lane Detection Model and perform a live demo

---

## 🎯 Objectives for this Sprint

- Define a communication pipeline between the Lane Detection model, PID and servo motors.
- Improve Lane Detection post processing, focusing on curves and intersections
- Perform initial training of Object Detection Model (YOLOv8/v26)
- Implement Manual/Autonomous driving modes
- Conduct a Spike on Model Predictive Control (MPC)
- Improve the the energy distribution system 

---

**Team Roles:**
| Name            | Responsibilities                          |
|-----------------|-------------------------------------------|
| Hellom          | Energy and Hardware                         |
| Vinicius        | PID + Lane Detection Integration                         |
| Jose            | PID + Lane Detection Integration                                      |
| Yasmine         | Lane Detection Model              |
| Marcelo         | PID + Lane Detection Integration                                      | 

## 📋 Backlog Overview

See [Projects](https://github.com/orgs/SEAME-pt/projects/83/views/1?sliceBy%5Bvalue%5D=Sprint+10)

## 🗣️ Daily Standup Logs

| Data | Progress Summary and Plan | Obstacles? |
| :--- | :--- | :--- |
| **13/04** | The team planned sprint 11, define the goals and split tasks **Marcelo, Vinicius and José:** Will work together to integrate the PID (steering) with the Lane Detection Model and servo motors **Yasmine:** Will work on the improvement of the Lane Detection Model post processing, focusing on curves and intersections. **Hellom:** Will upgrade the energy distribution system by adding a stepdown to feed the microcontroller and the display. |
| **14/04** | **Hellom**: Changed the energy distribution, adding a new step-down that feeds the microcontroller and the display, as well as heat sinks and coolers for the system. Today is focused on installing monitoring systems on the Raspberry Pi. **José**: Focused on finishing the 42 Common Core. **Yasmine**: Will work on improving the Lane Detection model post-processing, focusing on curves and intersections. **Vinicius**: Helped Hellom install new monitoring libraries into the AGL build, recompiling the entire system and flashing it onto the microSD card. He will also work together with **Marcelo** to integrate the PID class into the Lane Detection pipeline code, sending the steering value to the microcontroller via the CAN protocol. |
| **15/04** | **José**: Will work on the implementation of Manual/Autonomous driving modes by pressing buttons on the joystick. **Yasmine**: Improved the Lane Detection post-processing by creating imaginary lines on the road whenever the model doesn't recognize one of the lines. By implementing this, the detection has improved a lot, especially in curves.  **Vinicius and Marcelo**: Fine-tuning the PID control by calibrating the three PID parameters (Kp, Ki, Kd). **Hellom**: Day off. |
| **16/04** | **José**: Will work on documenting the implementation of Manual/Autonomous driving modes. **Yasmine and Marcelo**: Will improve the Lane Detection model dataset by creating new images of closed curves and challenging scenarios to improve the model's decision-making. **Vinicius**: Migrated the files to the new AGL system and will work on Object Detection model training. **Hellom**: Will explore the new monitoring features installed on the Raspberry Pi system. |
| **17/04** | **José**: Will work on creating a new driving mode called DEBUG, where the car tries to maintain a constant speed using PID on the microcontroller, while the steering is controlled by a PID controller on the Raspberry Pi. **Yasmine**: Will improve the Lane Detection post-processing and train a new model to detect lanes and crosswalks. **Vinicius**: Will work on Object Detection model training and study how to improve its precision, especially for speed signs. **Hellom**: Will convert the trained YOLOv26n model to the .hef format. **Marcelo**: Will work on improving Lane Detection post-processing to enhance decision-making in challenging scenarios, such as tight curves and/or when the camera fails to detect one of the lane lines. |
| **20/04** | **Vinicius**: Trained the YOLOv26n model for Object Detection from scratch, will think about a strategy to detect obstacles with different shapes and sizes, and will study how to convert the model to .hef format to run on Hailo. **Hellom**: Converted the new Lane Detection model, trained to recognize two classes (lanes and crosswalks), to .hef format and will work on understanding its output and post-processing. **Yasmine**: Will work on the decision-making system considering the output from both the Lane Detection and Object Detection models, creating a state machine that will control the actions and send instructions to the microcontroller. **Marcelo**: Will conduct a spike on Model Predictive Control and propose a possible implementation in our system. **José**: Focused on ft_transcendence, 42’s Common Core final project. | The car does not perform well in tight curves, as it sometimes swaps the left and right lane detections, generating a path outside the lane boundaries.
| **21/04** | **Hellom**: Converted the YOLOv26n-seg Lane Detection model, trained with a larger dataset containing hard scenarios and tight curves, so now we can validate it running on Hailo. **Vinicius**: Will work on converting the Object Detection model to .hef format so it can run properly on Hailo. **Yasmine**: Will work on the decision-making system. **Marcelo**: Will refactor the Qt code to receive two types of signs (speed and traffic signals) and display them at the same time. Also will think about a strategy to update this data based on the integration between Kuksa Databroker and Qt’s backend. **José**: Focused on ft_transcendence, 42’s Common Core final project. | The car does not perform well in tight curves, as it sometimes swaps the left and right lane detections, generating a path outside the lane boundaries.
| **22/04** | **Yasmine and Marcelo**: Worked on fixing the Lane Detection post-processing to improve the car’s performance in tight curves and keep the trajectory clean and correct, without leaving the lane boundaries, but did not have success. **Vinicius**: Successfully converted the Object Detection model to .hef format and will work on post-processing its output so he can test the model inside the car system. **Hellom**: Will reorganize the Lane Detection post-processing code, as it is currently all in a single file. **José**: Focused on ft_transcendence, 42’s Common Core final project. | The car does not perform well in tight curves, as it sometimes swaps the left and right lane detections, generating a path outside the lane boundaries.
| **23/04** | **Yasmine**: Will start working on curvature consistency validation to solve the blocker and asked José to provide steering information from the microcontroller to the Raspberry Pi. **Vinicius**: Managed to convert and test the Object Detection model, but noticed a drop in quality between the .pt and .hef versions. Because of that, he started another training yesterday with a lower resolution and will try to convert and test it today as well. **Hellom**: Currently working on the issue related to organizing the Lane Detection model execution code. **José**: Focused on ft_transcendence, 42’s Common Core final project, but will be at school and available to help. **Marcelo**: Could not work today due to personal matters. | The car does not perform well in tight curves, as it sometimes swaps the left and right lane detections, generating a path outside the lane boundaries.
| **24/04** | **Marcelo**: Will update all data related to this sprint, working on the presentation slides development. **Yasmine and José**: Worked together and managed to solve the blocker we were facing by fixing the Lane Detection post-processing code, and today will focus on organizing this architecture and documenting it. **Vinicius**: Will create new images from the SEAME lane with blurred images and also include data from public datasets, making the model more robust and improving its reliability in different scenarios. **Hellom**: Focused on the Europe and Defense Hackathon taking place this weekend at school. |

---

## 🧠 Key Achievements
- PID was successfully integrated with the Lane Detection model, calculating the steering angle and sending commands to the servo motors at every frame.
- The car can now complete a full lap autonomously. The post-processing was improved, enabling the prototype to handle tight curves while keeping the trajectory within the lane boundaries.
- The Object Detection model was trained and converted to .hef format, allowing it to run on Hailo. It already shows satisfactory reliability.
- Automatic and manual driving modes were implemented and validated, operating through joystick button inputs.
- The power distribution system was improved, and a new step-down converter was integrated into the system.
- Model Predictive Control (MPC) was studied, and a possible implementation strategy was documented.

---