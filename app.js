const imageElement = document.getElementById('imageElement');
const detectionResultElement = document.getElementById('detectionResult');

// Check if elements exist
if (!imageElement || !detectionResultElement) {
    console.error("Required HTML elements are missing");
}

async function detectBird() {
    try {
        const result = await GetImage();
        updateDetectionResult(result);
        displayImage(result.image_data);
    } catch (err) {
        console.error("Error detecting bird:", err);
        updateDetectionResult(null, err);
    } finally {
        setTimeout(detectBird, 500);
    }
}

function updateDetectionResult(result, error = null) {
    if (detectionResultElement) {
        if (error) {
            detectionResultElement.innerHTML = `<h2 class="error">Error detecting bird: ${error.message}</h2>`;
        } else {
            const isBird = result.is_bird;
            const statusClass = isBird ? 'bird-detected' : 'no-bird';
            const statusText = isBird ? 'Bird detected!' : 'No bird detected';

            detectionResultElement.innerHTML = `
                <h2 class="detection-status ${statusClass}">${statusText}</h2>
                <div class="detection-details">
                    <h3>Detected: ${result.label}</h3>
                    <h3>Probability: ${(result.probability * 100).toFixed(2)}%</h3>
                </div>
            `;
        }
    }
}

function displayImage(imageData) {
    if (imageElement) {
        if (imageData) {
            imageElement.src = `data:image/jpeg;base64,${imageData}`;
            imageElement.style.display = 'block';
        } else {
            console.warn('No image data received');
            imageElement.style.display = 'none';
        }
    } else {
        console.error('Image element not found');
    }
}

async function GetImage() {
    try {
        const response = await fetch('http://huey:9111/detect', {
            method: 'GET',
            cache: 'no-store'
        });

        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Error accessing the webcam or sending image to detector:', error);
        throw error;
    }
}

// Start the detection process
detectBird();