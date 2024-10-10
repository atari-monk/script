Given template below in the next prompt wait for scene data and create documentation.

### **Scene Name:** `YourSceneName`

---

### **1. Scene Overview**

- **Description:**
  Briefly describe the purpose and functionality of the scene.
  _Example: This scene is designed to test the spriteRenderer system, handle sprite positioning, and demonstrate the use of sprite flipping._

- **Version:** `1.0.0`
  - Mention the version of the scene.

---

### **2. Key Features**

- **Primary Elements:**

  - List and explain the primary elements within the scene, such as sprites, objects, or UI components.

    - **Element 1: Player1**
      - **Position:** `430, 540`
      - **Description:** Rendered to show how spriteRenderer draws position from the top left of the sprite.
    - **Element 2: Player2**
      - **Position:** _Defined via transform.position._
      - **Description:** Rendered using the `sprite.spriteOffset` property to demonstrate sprite translation for centering.
    - **Element 3: Player3 and Player4**
      - **Position:** `Player1 and Player2` flipped horizontally with an x+100 translation.
      - **Description:** Used to test sprite flipping.

- **Core System Components:**
  - `spriteRenderer 1.0.0`
    - **Description:** Renders the transform position from the top-left corner of the sprite.
  - `canvasScaler`
    - **Description:** Handles scaling for the scene.

---

### **3. Behavior and Logic**

- **Special Behavior:**
  - **spriteRenderer Positioning:** The system renders `transform.position` as the top-left point of the sprite in version 1.0.0.
  - **sprite.spriteOffset:** Demonstrates how the spriteOffset property moves the sprite so that the transform.position is at the sprite's center.
- **Behavioral Notes:**
  - Initial decisions, such as the use of `sprite.spriteOffset`, were made early in development and are now considered suboptimal. Kept for historical purposes.

---

### **4. Usage and Configuration**

- **How to Load the Scene:**
  Provide instructions on how to configure and load this scene.

  ```json
  "select": {
      "folder": "engine",
      "subFolder": "",
      "scene": "renderer100"
  }
  ```

---

### **5. Dependencies and Interactions**

- **Dependencies:**

  - List any modules, systems, or third-party libraries required for the scene to function.
    _Example: Depends on the spriteRenderer system and canvasScaler._

- **Interactions with Other Systems:**
  - Describe how this scene interacts with other game systems, components, or scenes.

---

### **6. Limitations and Assumptions**

- **Known Limitations:**
  - Describe any issues or limitations in this scene.
    _Example: The sprite rendering method is inefficient due to the improper use of `sprite.spriteOffset`._
- **Assumptions:**
  - Any assumptions made while designing the scene.
    _Example: Assumes that sprite flipping only affects horizontal orientation._

---

### **7. Historical Notes (Optional)**

- **Reasoning for Deprecated/Legacy Features:**
  - Explain why certain outdated features remain, even if they are no longer in use or optimal.
    _Example: Kept as a point of reference to show what not to do in future versions._

---
