# **Traffic Simulation with Burstiness Analysis**

## **Overview**
This project simulates a server queue handling heterogeneous traffic types (data, voice, video) to analyze their response times under varying video traffic burstiness.

The server has:
- **100 Mbps** capacity.
- Infinite queue capability.

The goal is to measure the mean response times and study the effects of video traffic burstiness on the network.

---

## **Features**
1. **Traffic Types**:
   - **Data Traffic**: Poisson-distributed arrivals with varying packet sizes.
   - **Voice Traffic**: Constant-sized packets with regular intervals.
   - **Video Traffic**: Bursty ON/OFF traffic modeled with exponential distributions.
2. **Configurable Burstiness**:
   - The burstiness factor (\( \beta \)) determines the ON and OFF periods for video traffic.
3. **Results**:
   - Mean response times and 95% confidence intervals.
   - Plots visualizing the impact of burstiness on all traffic types.

---

## **File Structure**

### **1. Folders**
- **`results/`**:
  - Stores plots or simulation outputs (e.g., `sample_plot.png`).
- **`src/`**:
  - Contains the simulation logic and all supporting classes.

### **2. Files**
| File/Folder                  | Description                                                        |
|------------------------------|--------------------------------------------------------------------|
| **`sources/TrafficSources.py`** | Defines the traffic sources: Poisson, Constant, and Bursty models. |
| **`sources/QueueClass.py`**  | Implements the server queue logic (FIFO).                         |
| **`sources/Globals.py`**     | Stores global variables for simulation (e.g., response times).    |
| **`sources/Simulation.py`**  | Main simulation logic combining sources and server queue.         |
| **`main.py`**                | Orchestrates the simulation and generates plots.                  |
| **`plotResults.ipynb`**      | Jupyter notebook for advanced visualization and debugging.        |
| **`requirements.txt`**       | Python dependencies for the project.                             |
| **`readme.md`**              | Documentation for the project.                                    |

---

## **How to Use**

### **1. Install Dependencies**
Ensure Python is installed on your system. Install the required libraries using:
```bash
pip install -r requirements.txt
