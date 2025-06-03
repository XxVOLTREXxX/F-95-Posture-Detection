# F-95 Posture Detection System

A real-time posture detection and analysis system with a modern GUI interface. This application helps users maintain proper posture by providing instant feedback and detailed joint angle measurements.

![F-95 Demo](demo.gif)

## Features

- 🎯 Real-time posture detection and analysis
- 📐 Live joint angle measurements
- 🖥️ Modern, dark-themed GUI interface
- 📊 Beautiful side panel with angle metrics
- 🔄 Instant posture feedback
- 🎨 Clean and intuitive design
- 🖼️ Centered camera window with black background
- 📱 Responsive window sizing

## Joint Angles Measured

- Neck Tilt
- Right Shoulder
- Left Shoulder
- Back Angle
- Hip Angle

## Requirements

- Python 3.8 or higher
- Webcam
- Windows/Linux/MacOS

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/F-95.git
cd F-95
```

2. Create a virtual environment (recommended):
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/MacOS
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python main.py
```

2. Click the "Get Started" button on the welcome screen

3. Click "Start Posture Detection" to begin posture analysis

4. Press 'Q' or 'q' to exit the posture detection window

## Interface Guide

### Welcome Screen
- Modern welcome page with feature highlights
- Easy navigation with "Get Started" button

### Main Screen
- Centered "Start Posture Detection" button
- Clean, minimalist design
- Easy return to home with "Back" button

### Posture Detection Window
- Real-time camera feed in center
- Posture status at top
- Joint angle measurements panel on right
- Semi-transparent overlay for better readability

## Technical Details

The application uses several key technologies:

- **OpenCV**: For camera capture and image processing
- **MediaPipe**: For pose detection and landmark tracking
- **CustomTkinter**: For modern GUI elements
- **NumPy**: For angle calculations and mathematical operations

## File Structure

```
F-95/
├── main.py              # Main application and GUI
├── posture_detection.py # Posture detection implementation
├── requirements.txt     # Project dependencies
└── README.md           # Documentation
```

## Dependencies

Main dependencies with versions:

```
opencv-python==4.8.1.78
mediapipe==0.10.9
customtkinter==5.2.2
pillow==10.2.0
numpy==1.26.3
```

For a complete list of dependencies, see `requirements.txt`.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


## Acknowledgments

- MediaPipe team for their pose detection model
- CustomTkinter for modern GUI components
- OpenCV team for computer vision capabilities

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

## Future Improvements

- [ ] Add pose history tracking
- [ ] Implement custom angle thresholds
- [ ] Add exercise routine suggestions
- [ ] Include posture statistics over time
- [ ] Export data functionality
- [ ] Multiple camera support

---
Made with ❤️ by Ayush Parchure 