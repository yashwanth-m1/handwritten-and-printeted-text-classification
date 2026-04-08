document.addEventListener('DOMContentLoaded', () => {
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    const previewContainer = document.getElementById('preview-container');
    const resultsSection = document.getElementById('results-section');
    const imagePreview = document.getElementById('image-preview');
    const processedImage = document.getElementById('processed-image');
    const classifyBtn = document.getElementById('classify-btn');
    const loader = document.getElementById('loader');
    const cameraBtn = document.getElementById('camera-btn');
    const cameraContainer = document.getElementById('camera-container');
    const video = document.getElementById('video');
    const snapBtn = document.getElementById('snap-btn');
    const cancelCameraBtn = document.getElementById('cancel-camera-btn');

    let currentFile = null;
    let stream = null;

    // Click to upload
    dropZone.addEventListener('click', (e) => {
        if (e.target.id === 'camera-btn' || e.target.closest('#camera-btn')) {
            e.stopPropagation();
            return;
        }
        fileInput.click();
    });

    // Camera handling
    cameraBtn.addEventListener('click', async () => {
        try {
            stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'environment' } });
            video.srcObject = stream;
            cameraContainer.classList.remove('hidden');
            previewContainer.classList.add('hidden');
            dropZone.classList.add('hidden');
        } catch (err) {
            console.error("Error accessing camera:", err);
            alert("Could not access camera. Please ensure permissions are granted.");
        }
    });

    cancelCameraBtn.addEventListener('click', () => {
        stopCamera();
    });

    snapBtn.addEventListener('click', () => {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);

        canvas.toBlob((blob) => {
            const file = new File([blob], "capture.jpg", { type: "image/jpeg" });
            handleFile(file);
            stopCamera();
        }, 'image/jpeg');
    });

    function stopCamera() {
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
            stream = null;
        }
        cameraContainer.classList.add('hidden');
        dropZone.classList.remove('hidden');
    }

    // File input change
    fileInput.addEventListener('change', (e) => {
        handleFile(e.target.files[0]);
    });

    // Drag and drop events
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        handleFile(e.dataTransfer.files[0]);
    });

    function handleFile(file) {
        if (!file || !file.type.startsWith('image/')) {
            alert('Please upload a valid image file.');
            return;
        }

        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            previewContainer.classList.remove('hidden');
            resultsSection.classList.add('hidden');
        };
        reader.readAsDataURL(file);
    }

    classifyBtn.addEventListener('click', async () => {
        if (!currentFile) return;

        const formData = new FormData();
        formData.append('image', currentFile);

        loader.classList.remove('hidden');

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.error) {
                alert(data.error);
            } else {
                processedImage.src = `data:image/png;base64,${data.image}`;
                updateStats(data.results);
                resultsSection.classList.remove('hidden');
                resultsSection.scrollIntoView({ behavior: 'smooth' });
            }
        } catch (error) {
            console.error('Classification error:', error);
            alert('An error occurred during classification. Please check the console.');
        } finally {
            loader.classList.add('hidden');
        }
    });

    function updateStats(results) {
        const counts = {
            'Handwritten_extended': 0,
            'Printed_extended': 0,
            'Mixed_extended': 0,
            'Other_extended': 0
        };

        results.forEach(res => {
            if (counts.hasOwnProperty(res.label)) {
                counts[res.label]++;
            }
        });

        document.getElementById('count-handwritten').textContent = counts['Handwritten_extended'];
        document.getElementById('count-printed').textContent = counts['Printed_extended'] + counts['Mixed_extended']; // Mixed often counts as printed in simplified views or keep separate
        document.getElementById('count-mixed').textContent = counts['Mixed_extended'];
        document.getElementById('count-other').textContent = counts['Other_extended'];

        // Update combined printed if preferred
        document.getElementById('count-printed').textContent = counts['Printed_extended'];
    }

    downloadBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.download = 'classification_result.png';
        link.href = processedImage.src;
        link.click();
    });
});
