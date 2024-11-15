import random

class SimpleMind:
    def __init__(self):
        self.memory = []
        self.senses = {
            "sight": None,
            "sound": None,
            "touch": None
        }

    # Sensory input simulation
    def sense(self, sense_type, input_data):
        if sense_type in self.senses:
            self.senses[sense_type] = input_data
            print(f"Sensed {sense_type}: {input_data}")
        else:
            print("Unknown sense!")

    # Memory - storing experiences
    def store_memory(self, sense_type, data):
        self.memory.append((sense_type, data))
        print(f"Memory stored: {sense_type} - {data}")

    # Response generation - simple approximation of thought
    def think(self):
        if any(self.senses.values()):  # If any sense has data
            response = "I'm processing what I sense..."
            self.store_memory("thought", response)
        else:
            response = "I don't sense anything right now."
        
        return response

    # Decision making - simplistic
    def decide_action(self):
        if self.senses["sight"] == "danger":
            action = "Run away!"
        elif self.senses["sound"] == "voice":
            action = "Say hello!"
        else:
            action = random.choice(["Walk around", "Stay still"])

        print(f"Action decided: {action}")
        return action

# Example usage
mind = SimpleMind()

# Sensory inputs
mind.sense("sight", "danger")
mind.sense("sound", "voice")

# Memory storage
mind.store_memory("sight", "danger")
mind.store_memory("sound", "voice")

# Thinking and deciding actions based on senses
print(mind.think())
action = mind.decide_action()
