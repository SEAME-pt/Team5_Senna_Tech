# Technical Analysis Report - Resolution of Issue 76

This document details the investigation process, analysis, and decisions made to complete the requirements of "issue 76," which aimed to estimate the electrical consumption of all system components.

## 1.0 Executive Summary
This report documents the power consumption analysis conducted to fulfill the requirements of "issue 76." The investigation concluded that the calculated power demand for the system (101.775 W) significantly exceeds the capacity of the originally specified power source (60.48 W). Additionally, critical limitations were identified in the Raspberry Pi 5's ability to power high-performance peripherals through its internal PCIe and USB interfaces, posing a risk to system stability and integrity.

## 2.0 Introduction and Objective
The primary objective of this analysis, as defined in "issue 76," was to quantify the power requirements of all electronic components of the system. This included verifying datasheets, calculating power, and applying safety margins to create a solid foundation for the power system design.

## 3.0 Technical Analysis of Critical Components

### 3.1 Motor Controller (TB6612FNG)
- **Analysis:** The existing motor controller, based on the TB6612FNG chip, has a continuous current capacity of 1.0A per channel. The system's motors (model 37-520) exhibit a peak (stall) current of 2.3A.
- **Conclusion:** The controller is undersized and represents a critical point of failure under load, being unable to safely support the motor's demand.

### 3.2 Hailo-8L AI Accelerator HAT (PCIe Power)
- **Analysis:** The Raspberry Pi 5's PCIe interface provides a maximum power of 5W (5V @ 1A). The maximum power consumption of the HAT with the Hailo-8L chip was verified to be 5W.
- **Conclusion:** Powering the HAT directly from the Raspberry Pi 5 would cause the system to operate at the absolute limit of its capacity (1A/1A), without any safety margin, leading to a high risk of instability and shutdowns under load.

### 3.3 mSATA SSD Adapter (USB Power)
- **Analysis:** The adapter, powered by a 5V USB port, consumes approximately 1.1A. The Raspberry Pi 5's USB ports can provide a total of 1.6A.
- **Conclusion:** Powering is feasible, but it critically depends on the Raspberry Pi 5 being powered by a 5V/5A USB-C Power Delivery (PD) source, which enables the 1.6A capacity on the USB ports.

## 4.0 Energy Balance Analysis
The final analysis, performed using data consolidated in the power calculation spreadsheet, resulted in the following values:
- **Total System Power Demand:** 101.775 W
- **Capacity of Original Power Source:** 60.48 W
- **Energy Deficit:** -41.295 W

## 5.0 General Conclusion
The quantitative analysis demonstrates that the power configuration originally planned for the project is insufficient to meet the system's maximum demand. Furthermore, the power supply limitations of the Raspberry Pi 5's internal interfaces pose significant risks to hardware stability and integrity. It is concluded that a re-evaluation and redesign of the power architecture are necessary to ensure safe and reliable system operation.

## 5.1 Power Source Analysis (3s1p Battery)

This analysis details the capacity of the `3s1p` battery pack to meet the system's demand, dividing the analysis into two scenarios: **Base Demand** (continuous operation) and **Peak Demand**.

**3s1p Battery Pack Characteristics:**
- **Nominal Voltage:** 10.8V
- **Available Continuous Power:** 10.8V * 1.6A = **17.28 W** (Based on the 1.6A continuous discharge limit)
- **Available Peak Power:** 10.8V * 10.4A = **112.32 W** (Based on the 10.4A pulse discharge limit)

**System Demand Calculation:**

From the consumption spreadsheet, we have:
- **Total Base Power Demand:** 65 W (sum of components' "Base Power")
- **Total Peak Power Demand:** 105.375 W (sum of "Final Power", which includes peak factors and margins)

For the 10.8V pack to power the components (at 5V and 12V), the efficiency of the DC-DC converters must be considered. Assuming a 90% efficiency, the actual power drawn from the pack is higher.

---

### Scenario Analysis

#### Scenario 1: Base Demand (Continuous Operation)

In this scenario, the system is under a normal workload, without motor or processing peaks.

- **Base Power Required from Pack:** 65 W / 0.90 = **72.22 W**
- **Continuous Power Available from Pack:** **17.28 W**

**Conclusion for Base Scenario:**
The system's base power demand (**72.22 W**) is more than **4 times higher** than the continuous power that the `3s1p` pack can safely provide (**17.28 W**). This means that **the system cannot operate stably even under its minimum workload.**

#### Scenario 2: Peak Demand

This scenario considers the maximum load, with motors in stall and all components at maximum consumption.

- **Peak Power Required from Pack:** 105.375 W / 0.90 = **117.08 W**
- **Peak Power Available from Pack:** **112.32 W**

**Conclusion for Peak Scenario:**
The peak power demand (**117.08 W**) **slightly exceeds** the maximum pulse power that the `3s1p` pack can provide (**112.32 W**). The pack cannot even supply the necessary power peaks, resulting in voltage drops and system failures during the most demanding operation.

**Update:** Subsequent analysis of the battery's protection board (BMS), based on the S-8254AA IC, reveals a hardware overcurrent protection limit estimated at **~7.5A (~81W)**. This limit is significantly lower than the calculated peak demand of **10.84A (117.08W)**. This means the BMS will trigger a hard shutdown long before the battery cells' own pulse limit is reached, making the BMS the primary bottleneck for peak performance.

---

### Final Recommendation

The analysis of both scenarios demonstrates that the `3s1p` configuration with the current cells is **critically insufficient**. The recommendation is to replace the current cells with others with a **higher discharge C-rate**, capable of meeting the system's demand.

Below are two possible upgrade strategies:

#### Strategy 1: Maintain the Minimum Configuration (`3s1p`)

For a `3s1p` pack to be viable, it would be necessary to find a new cell (18650 format, ~3200mAh) with the following minimum specifications:
- **Continuous Discharge Current:** > 6.7 A (for base demand)
- **Pulse Discharge Current:** > 10.9 A (for peak demand)

This translates to a cell with a **continuous C-rate of ~2.1C** and a **pulse C-rate of ~3.4C**.

#### Strategy 2: Use a Compact Pack (`3s2p`)

Using a `3s2p` pack (6 cells in total) would allow the use of cells with more common specifications and potentially lower cost. The current would be divided between two parallel cells.

In this case, the new cell would need to have the following minimum specifications:
- **Continuous Discharge Current:** > 3.4 A (for base demand)
- **Pulse Discharge Current:** > 5.5 A (for peak demand)

This translates to a cell with a **continuous C-rate of ~1.05C** and a **pulse C-rate of ~1.7C**. This option offers a greater safety margin and is technically easier to find on the market.

**Conclusion of the Recommendation:**
The replacement of the current cells is mandatory. **Strategy 2 (`3s2p`) is the most recommended**, as it balances size, cost, and the availability of cells on the market that meet the C-rate requirements for safe and stable operation.

## 6.0 Associated Documentation
- **Power Calculation Spreadsheet:** [Power Calculation Spreadsheet (Google Sheets)](https://docs.google.com/spreadsheets/d/17OTOM8TGwGTdGTEiZJhmAMZjc8ibhz_UrK2ZYge63Ok/edit?usp=sharing)
