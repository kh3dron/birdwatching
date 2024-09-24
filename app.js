const imageElement = document.getElementById('imageElement');
const detectionResultElement = document.getElementById('detectionResult');

// Check if elements exist
if (!imageElement || !detectionResultElement) {
    console.error("Required HTML elements are missing");
}
let stream;
let videoTrack;

async function startWebcam() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoTrack = stream.getVideoTracks()[0];
        captureAndDisplayImage();
    } catch (err) {
        console.error("Error accessing the webcam:", err);
    }
}

async function captureAndDisplayImage() {
    const imageCapture = new ImageCapture(videoTrack);
    
    try {
        const blob = await imageCapture.takePhoto();
        const imageUrl = URL.createObjectURL(blob);
        imageElement.src = imageUrl;
        
        // Send image to detector API
        const detectionResult = await sendImageToDetector(blob);
        if (detectionResultElement) {
            detectionResultElement.textContent = detectionResult ? "Bird detected!" : "No bird detected.";
        }
    } catch (err) {
        console.error("Error capturing image:", err);
    }

    // Schedule the next capture after 1 second
    setTimeout(captureAndDisplayImage, 1000);
}

async function sendImageToDetector(imageBlob) {
    const formData = new FormData();
    formData.append('image', imageBlob, 'image.jpg');

    try {
        const response = await fetch('http://localhost:9001/detect', {
            method: 'POST',
            body: formData
        });
        const result = await response.json();
        return result.bird_detected;
    } catch (error) {
        console.error('Error sending image to detector:', error);
        return false;
    }
}

startWebcam();