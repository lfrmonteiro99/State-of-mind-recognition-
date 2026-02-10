// Speech Emotion Recognition App
class EmotionRecognitionApp {
    constructor() {
        this.mediaRecorder = null;
        this.audioChunks = [];
        this.stream = null;
        this.startTime = null;
        this.timerInterval = null;
        this.audioContext = null;
        this.analyser = null;
        this.animationId = null;

        this.initElements();
        this.initEventListeners();
    }

    initElements() {
        this.recordBtn = document.getElementById('recordBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.statusIndicator = document.getElementById('statusIndicator');
        this.statusText = document.getElementById('statusText');
        this.timer = document.getElementById('timer');
        this.resultsSection = document.getElementById('resultsSection');
        this.topEmotion = document.getElementById('topEmotion');
        this.emotionBars = document.getElementById('emotionBars');
        this.visualizerCanvas = document.getElementById('visualizerCanvas');
        this.canvasContext = this.visualizerCanvas.getContext('2d');
    }

    initEventListeners() {
        this.recordBtn.addEventListener('click', () => this.startRecording());
        this.stopBtn.addEventListener('click', () => this.stopRecording());
    }

    async startRecording() {
        try {
            // Request microphone access
            this.stream = await navigator.mediaDevices.getUserMedia({ audio: true });

            // Setup audio context for visualization
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            this.analyser = this.audioContext.createAnalyser();
            const source = this.audioContext.createMediaStreamSource(this.stream);
            source.connect(this.analyser);
            this.analyser.fftSize = 256;

            // Setup media recorder
            this.mediaRecorder = new MediaRecorder(this.stream);
            this.audioChunks = [];

            this.mediaRecorder.ondataavailable = (event) => {
                this.audioChunks.push(event.data);
            };

            this.mediaRecorder.onstop = () => {
                this.processRecording();
            };

            // Start recording
            this.mediaRecorder.start();
            this.startTime = Date.now();

            // Update UI
            this.updateUIRecording();
            this.startTimer();
            this.startVisualization();

        } catch (error) {
            console.error('Error accessing microphone:', error);
            alert('Unable to access microphone. Please check permissions.');
        }
    }

    stopRecording() {
        if (this.mediaRecorder && this.mediaRecorder.state !== 'inactive') {
            this.mediaRecorder.stop();
            this.stream.getTracks().forEach(track => track.stop());
            this.stopTimer();
            this.stopVisualization();
            this.updateUIProcessing();
        }
    }

    updateUIRecording() {
        this.recordBtn.disabled = true;
        this.stopBtn.disabled = false;
        this.statusText.textContent = 'Recording...';
        this.statusIndicator.querySelector('.status-dot').classList.add('recording');
        this.resultsSection.classList.remove('active');
    }

    updateUIProcessing() {
        this.recordBtn.disabled = true;
        this.stopBtn.disabled = true;
        this.statusText.textContent = 'Analyzing...';
    }

    updateUIReady() {
        this.recordBtn.disabled = false;
        this.stopBtn.disabled = true;
        this.statusText.textContent = 'Ready to record';
        this.statusIndicator.querySelector('.status-dot').classList.remove('recording');
    }

    startTimer() {
        this.timerInterval = setInterval(() => {
            const elapsed = Math.floor((Date.now() - this.startTime) / 1000);
            const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
            const seconds = (elapsed % 60).toString().padStart(2, '0');
            this.timer.textContent = `${minutes}:${seconds}`;
        }, 1000);
    }

    stopTimer() {
        if (this.timerInterval) {
            clearInterval(this.timerInterval);
            this.timerInterval = null;
        }
    }

    startVisualization() {
        const bufferLength = this.analyser.frequencyBinCount;
        const dataArray = new Uint8Array(bufferLength);

        const draw = () => {
            this.animationId = requestAnimationFrame(draw);

            this.analyser.getByteFrequencyData(dataArray);

            this.canvasContext.fillStyle = '#334155';
            this.canvasContext.fillRect(0, 0, this.visualizerCanvas.width, this.visualizerCanvas.height);

            const barWidth = (this.visualizerCanvas.width / bufferLength) * 2.5;
            let x = 0;

            for (let i = 0; i < bufferLength; i++) {
                const barHeight = (dataArray[i] / 255) * this.visualizerCanvas.height;

                const gradient = this.canvasContext.createLinearGradient(0, 0, 0, this.visualizerCanvas.height);
                gradient.addColorStop(0, '#667eea');
                gradient.addColorStop(1, '#764ba2');

                this.canvasContext.fillStyle = gradient;
                this.canvasContext.fillRect(
                    x,
                    this.visualizerCanvas.height - barHeight,
                    barWidth,
                    barHeight
                );

                x += barWidth + 1;
            }
        };

        // Resize canvas
        this.visualizerCanvas.width = this.visualizerCanvas.offsetWidth;
        this.visualizerCanvas.height = this.visualizerCanvas.offsetHeight;

        draw();
    }

    stopVisualization() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
            this.animationId = null;
        }
        if (this.audioContext) {
            this.audioContext.close();
            this.audioContext = null;
        }
    }

    async processRecording() {
        try {
            // Create audio blob
            const audioBlob = new Blob(this.audioChunks, { type: 'audio/webm' });

            // Check if full analysis mode is enabled
            const fullAnalysisMode = document.getElementById('fullAnalysisMode').checked;

            // Send to backend
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');

            const endpoint = fullAnalysisMode ? '/analyze-full' : '/predict-emotion';
            const response = await fetch(endpoint, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Failed to analyze audio');
            }

            const result = await response.json();

            if (fullAnalysisMode) {
                this.displayFullAnalysis(result);
            } else {
                this.displayResults(result.data);
            }

        } catch (error) {
            console.error('Error processing recording:', error);
            alert(`Error: ${error.message}`);
        } finally {
            this.updateUIReady();
        }
    }

    displayResults(data) {
        const emotionEmojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'fear': '😨',
            'disgust': '🤢',
            'neutral': '😐',
            'surprise': '😲'
        };

        const emotionColors = {
            'happy': '#10B981',
            'sad': '#3B82F6',
            'angry': '#DC2626',
            'fear': '#8B5CF6',
            'disgust': '#059669',
            'neutral': '#6B7280',
            'surprise': '#F59E0B'
        };

        // Update top emotion
        const topEmotionName = data.top_emotion;
        const confidence = (data.confidence * 100).toFixed(1);

        this.topEmotion.innerHTML = `
            <div class="emotion-icon">${emotionEmojis[topEmotionName] || '😐'}</div>
            <div class="emotion-name">${topEmotionName}</div>
            <div class="confidence">${confidence}% confident</div>
        `;

        // Sort emotions by probability
        const emotions = Object.entries(data.predictions)
            .sort((a, b) => b[1] - a[1]);

        // Create emotion bars
        this.emotionBars.innerHTML = emotions.map(([emotion, probability]) => {
            const percentage = (probability * 100).toFixed(1);
            const color = emotionColors[emotion] || '#6B7280';

            return `
                <div class="emotion-bar">
                    <div class="emotion-label">
                        <span>${emotionEmojis[emotion] || '😐'}</span>
                        <span>${emotion}</span>
                    </div>
                    <div class="bar-container">
                        <div class="bar-fill" style="width: ${percentage}%; background: ${color};"></div>
                    </div>
                    <div class="bar-percentage">${percentage}%</div>
                </div>
            `;
        }).join('');

        // Show results section
        this.resultsSection.classList.add('active');

        // Smooth scroll to results
        this.resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    displayFullAnalysis(result) {
        // Display emotion results first
        this.displayResults(result.emotion);

        // Display transcription
        const transcriptionText = document.getElementById('transcriptionText');
        transcriptionText.textContent = result.transcription.text || 'No transcription available';

        // Display AI analysis
        const emotionalAnalysis = document.getElementById('emotionalAnalysis');
        const stateOfMind = document.getElementById('stateOfMind');
        const advice = document.getElementById('advice');

        emotionalAnalysis.textContent = result.analysis.emotional_analysis || 'Analyzing...';
        stateOfMind.textContent = result.analysis.state_of_mind || 'Assessing...';
        advice.textContent = result.analysis.advice || 'Generating advice...';

        // Show full analysis section
        const fullAnalysisSection = document.getElementById('fullAnalysisSection');
        fullAnalysisSection.classList.add('active');

        // Smooth scroll to full analysis
        fullAnalysisSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    const app = new EmotionRecognitionApp();
    console.log('🎤 Speech Emotion Recognition App initialized');
});
