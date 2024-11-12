import time
import random

class TemperatureControlSystem:
    def __init__(self, target_temp):
        self.target_temp = target_temp
        self.current_temp = random.uniform(target_temp - 5, target_temp + 5)
        self.adjustment_factor = 0.5  # Determines the rate of adjustment

    def measure(self):
        # Simulate a measurement with some random noise
        noise = random.uniform(-1, 1)
        measured_temp = self.current_temp + noise
        return measured_temp

    def adjust(self, measured_temp):
        # Calculate the difference between the current and target temperatures
        error = self.target_temp - measured_temp
        # Adjust temperature based on the error
        adjustment = error * self.adjustment_factor
        self.current_temp += adjustment

    def run(self):
        while True:
            measured_temp = self.measure()
            print(f"Measured Temperature: {measured_temp:.2f}")
            
            # Check if close enough to target to stop adjustments
            if abs(self.target_temp - measured_temp) < 0.01:
                print("Target temperature reached.")
                break
            
            self.adjust(measured_temp)
            print(f"Adjusted Temperature: {self.current_temp:.2f}")
            
            # Simulate a time delay in the loop
            time.sleep(1)
