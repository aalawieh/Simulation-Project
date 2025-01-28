# **Simulation Project**

## **Overview**
This project simulates heterogeneous network traffic (data, voice, and video) flowing through an infinite capacity queue. The objective is to analyze the **mean response times** of each traffic type under varying levels of video traffic burstiness.

## **Key Features**
- Simulates three types of traffic:
  - **Data**: Poisson arrivals with variable packet sizes.
  - **Voice**: Fixed-size packets arriving at regular intervals.
  - **Video**: Bursty traffic modeled with ON/OFF periods.
- Tracks **response times** for each traffic type.
- Computes **confidence intervals** for the response times.
- Provides visual analysis with a plot of response times vs. burstiness factors.

---

## **How It Works**
1. **Traffic Generation**:
   - **Data traffic** is generated with Poisson arrivals and variable packet sizes.
   - **Voice traffic** is periodic with fixed-size packets.
   - **Video traffic** follows a bursty ON/OFF model, where the burstiness factor (\( \beta \)) controls the ON and OFF durations.

2. **Queue Processing**:
   - Packets are processed in **FIFO** (First In, First Out) order by a server with a capacity of **100 Mbps**.

3. **Output**:
   - Mean response times and their 95% confidence intervals are computed.
   - Results are saved as:
     - A plot (`burstiness_vs_response_times.png`).
     - Response time data (`response_times.txt`).

---

## **Dependencies**
The project requires the following Python libraries:
- `simpy` (4.1.1): Discrete-event simulation.
- `numpy` (>=1.20): Numerical computations.
- `matplotlib` (>=3.3): Plotting results.
- `scipy` (>=1.6): Statistical computations.

Install the dependencies with:
```bash
pip install -r requirements.txt

