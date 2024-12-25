# **Scorify**

Scorify is an intelligent application designed to utilize computer vision, speech recognition, and natural language processing to provide real-time insights and functionalities such as image detection, speech recognition, and interactive responses.

---

## **Features**
1. **Start Camera**: Activates the camera to stream live video.
2. **Back Camera**: Switches to the back camera for video input.
3. **Detect Image**: Captures the video frame, analyzes it using the Google Vision API, and provides responses.
4. **Listen and Speak (LNS)**: Records spoken input, generates hints based on the input using GPT-3.5 Turbo, and reads them aloud.
5. **Interactive Design**: The application integrates seamlessly with modern web technologies for an engaging user experience.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd <repository-name>
```

### **2. Install Backend Dependencies**
Ensure you have Python 3.9+ installed. Install the required packages:
```bash
pip install -r requirements.txt
```

### **3. Start the Flask Application**
Run the following command to start the backend Flask app:
```bash
python yolov3.py
```

The Flask app will run at `http://127.0.0.1:5000`.

---

## **Frontend Deployment**

### **Serve Frontend Locally**
The frontend is served via a static HTTP server for development:
1. Install `http-server` globally using Node.js:
   ```bash
   npm install -g http-server
   ```
2. Navigate to the project directory:
   ```bash
   cd static/
   ```
3. Start the server:
   ```bash
   http-server -p 8080
   ```

Visit `http://localhost:8080` to access the frontend.

---

## **Environment Variables**
Ensure the following environment variables are configured:
- `GOOGLE_VISION_API_KEY`: Your Google Vision API Key.
- `PORT`: Port for the Flask backend (default: `8000`).

---

## **How to Use**
1. **Start the Flask Backend**:
   Ensure the backend is running at `http://127.0.0.1:5000`.

2. **Launch the Frontend**:
   Access the frontend at `http://localhost:8080`.

3. **Use Functionalities**:
   - **Start Camera**: Starts the live camera feed.
   - **Back Camera**: Switch to the back-facing camera.
   - **Detect Image**: Analyze the current camera frame for text and objects.
   - **Listen and Speak**: Record your voice input, process it, and receive spoken hints.

---

## **Demo**
A live demo is available at:
- **GitHub Pages**: `<GitHub Pages URL>`
- **Google Cloud Run**: `<Cloud Run URL>`

---

## **Future Enhancements**
- Integrate more NLP models for better hint generation.
- Improve UI/UX for seamless interaction.
- Expand support for object detection beyond text recognition.
