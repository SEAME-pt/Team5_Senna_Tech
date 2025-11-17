# Power Calculation Spreadsheet User Guide

## 1. Purpose of the Spreadsheet (The Why)

The objective of this spreadsheet is to centralize and standardize the analysis of power consumption for the project's electronic components. Its use is fundamental for:

- **Sizing the Power Supply:** Calculate the total power required to ensure that the chosen battery or power source can safely supply the entire system.
- **Ensuring System Stability:** Prevent unexpected failures and resets caused by current peaks that the power source cannot supply.
- **Analyzing Safety Margins:** Apply safety factors to accommodate component variations and unforeseen consumption peaks.
- **Validating Estimates:** Compare theoretical data (provided by datasheets) with real hardware measurements, allowing for more precise planning in future iterations.

The spreadsheet is available at the following link:
[Power Calculation Spreadsheet (Google Sheets)](https://docs.google.com/spreadsheets/d/17OTOM8TGwGTdGTEiZJhmAMZjc8ibhz_UrK2ZYge63Ok/edit?usp=sharing)

## 2. How to Use the Spreadsheet (The How)

The spreadsheet is divided into sections for data input, assumptions, and calculated results. Follow the steps below to fill it out correctly.

### Step 1: Enter Component Base Data

Fill in the following columns for each component that will be powered by the system:

- **Component**: Name of the component (e.g., Raspberry Pi 4, SG90 Servo Motor).
- **Rail**: The voltage line that powers the component (e.g., 5V, 12V).
- **Source/Datasheet**: Link or name of the document from which the data was obtained.
- **Voltage (V)**: The nominal operating voltage of the component.
- **Max Current (A)**: The maximum current the component can draw, according to the datasheet.

### Step 2: Define Safety Assumptions

These columns are essential for safe sizing:

- **Peak Factor**: A multiplier to estimate consumption peaks.
  - **Example**: DC motors can draw 3 to 5 times the nominal current when starting. In this case, the peak factor would be 3 or 5. For components without significant peaks (like an LED), the factor can be 1.
- **Margin (%)**: An additional safety margin to cover uncertainties or variations. A common value is between 10% and 20%.

### Step 3: Analyze Calculated Results

The following columns are automatically calculated and should not be edited manually:

- **Base Power (W)**: `Voltage × Max Current`. Represents consumption under normal conditions.
- **Final Power (W)**: `Base Power × Peak Factor × (1 + Margin / 100)`. This is the final value to be considered for sizing, as it already includes peaks and the safety margin.

In the corners of the spreadsheet, you will find the totals of **Final Power** for each voltage rail (`Total 5V`, `Total 12V`), which indicate the total demand that the power source must be able to supply.

### Step 4: Record Real Measurements (Optional)

After hardware assembly, you can measure actual consumption and fill in the `MED.` columns to validate your estimates:

- **MED. Voltage (V)**: Measured voltage at the component.
- **MED. Current (A)**: Measured current during operation.
- **MED. Power (W)**: Real power, calculated from the measurements.

### Battery Table

The second table in the spreadsheet helps calculate the total power your battery can provide, based on the number of cells and their capacity. This allows for a quick comparison between available power and the total power required by the system.