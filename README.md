# 🎨 Paint in Air ✨

**Paint in Air** is a real-time air drawing application built with Python and OpenCV. It allows you to use a mobile camera (via DroidCam) as a webcam to track colored markers in the air and draw on a persistent digital canvas. The application dynamically selects the drawing color when a marker is placed in a designated Region of Interest (ROI) and continues to track and draw its movement across the entire screen.

## 🛠 Demo
https://github.com/user-attachments/assets/cd1df7e3-e1d8-44d5-bee6-b2b51df5edd4
## 🚀 Features

- 🎭 **Dynamic Color Selection:**  
  Place a colored marker (e.g., 🔵 or 🔴) in the ROI to select it as the active drawing color.

- ✏️ **Air Drawing:**  
  Move the marker in the frame to draw lines on a persistent canvas.

- 📱 **Mobile Camera Integration:**  
  Use your smartphone as a webcam via DroidCam.

- 🎯 **Robust Color Detection:**  
  Uses HSV color space and morphological operations for accurate marker detection.

- ⏳ **Real-Time Tracking:**  
  Tracks the marker’s movement and updates the drawing instantly.

## 🔑 Keywords

OpenCV, Python, Air Drawing, Mobile Camera, DroidCam, ROI, Color Detection, Marker Tracking, HSV, Real-Time, Computer Vision, Interactive Drawing.

## 🛠 Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/HusainAli512/Paint_in_air.git
   cd Paint_in_air
   ```

2. **Install Dependencies:**

   Ensure you have Python 3 installed, then run:

   ```bash
   pip install opencv-python numpy
   ```

3. **Set Up DroidCam (Optional):**

   - Install the [📲 DroidCam App](https://play.google.com/store/apps/details?id=com.dev47apps.droidcam) on your mobile device.
   - Launch the app and note the IP address.
   - Update the `DROIDCAM_IP` variable in the code with your mobile device’s IP address.

## ▶️ Usage

Run the application with:





```bash
python your_script_name.py
```

- A fixed ROI will appear on the live video feed.
- Place your marker (🔵 or 🔴) inside the ROI to select its color.
- Move the marker across the screen to draw a continuous trail on the canvas.
- The application displays the live feed with the drawing overlay and active color mask.
- Press **'q'** to exit the application.

## 📝 Code Overview

- **🟨 ROI Color Selection:**  
  The application defines a small, fixed ROI (e.g., a 150×100 rectangle) where the marker's color is detected. The ROI is processed in HSV color space to determine if a marker is present and to select the active color.

- **🟢 Full-Frame Tracking:**  
  Once the active color is set (🔵 or 🔴), the entire frame is processed using HSV thresholding to track the marker's movement. Contours are detected and their centers computed.

- **🖌️ Drawing on Canvas:**  
  The detected marker positions are stored, and lines are drawn between successive points on a persistent canvas using the active color. This canvas is overlaid on the live feed for real-time drawing feedback.

## 🤝 Contributing

Contributions are welcome! If you have suggestions or improvements, please feel free to open an issue or submit a pull request. 💡

## 📜 License

This project is licensed under the MIT License.

## 💖 Acknowledgements

- [OpenCV](https://opencv.org/) 🖥️
- [DroidCam](https://www.dev47apps.com/) 📸
- Inspired by various computer vision projects and tutorials. 🚀
