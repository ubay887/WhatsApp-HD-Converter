// ===== DOM Elements =====
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFile = document.getElementById('removeFile');
const convertBtn = document.getElementById('convertBtn');
const progressContainer = document.getElementById('progressContainer');
const progressFill = document.getElementById('progressFill');
const progressText = document.getElementById('progressText');
const statusMessage = document.getElementById('statusMessage');
const downloadSection = document.getElementById('downloadSection');
const downloadBtn = document.getElementById('downloadBtn');
const convertAnother = document.getElementById('convertAnother');

// ===== State =====
let selectedFile = null;
let convertedBlob = null;

// ===== Constants =====
const MAX_FILE_SIZE = 100 * 1024 * 1024; // 100MB
const ALLOWED_TYPES = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska', 'video/webm', 'video/x-m4v'];
const ALLOWED_EXTENSIONS = ['mp4', 'mov', 'avi', 'mkv', 'webm', 'm4v'];

// ===== Smooth Scroll =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===== Upload Area Events =====
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

removeFile.addEventListener('click', () => {
    resetUpload();
});

convertAnother.addEventListener('click', () => {
    resetUpload();
});

// ===== File Handling =====
function handleFile(file) {
    // Validate file type
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const isValidType = ALLOWED_TYPES.includes(file.type) || ALLOWED_EXTENSIONS.includes(fileExtension);
    
    if (!isValidType) {
        showStatus('Format file tidak didukung! Gunakan: MP4, MOV, AVI, MKV, WEBM, M4V', 'error');
        return;
    }
    
    // Validate file size
    if (file.size > MAX_FILE_SIZE) {
        showStatus('File terlalu besar! Maksimal 100MB', 'error');
        return;
    }
    
    // Store file
    selectedFile = file;
    
    // Update UI
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    fileInfo.classList.add('show');
    uploadArea.style.display = 'none';
    
    // Enable convert button
    convertBtn.disabled = false;
    convertBtn.querySelector('.btn-text').textContent = 'Convert to HD';
    
    // Hide previous results
    downloadSection.classList.remove('show');
    statusMessage.classList.remove('show');
    progressContainer.classList.remove('show');
}

function resetUpload() {
    selectedFile = null;
    convertedBlob = null;
    fileInput.value = '';
    
    // Reset UI
    fileInfo.classList.remove('show');
    uploadArea.style.display = 'block';
    downloadSection.classList.remove('show');
    statusMessage.classList.remove('show');
    progressContainer.classList.remove('show');
    
    // Reset button
    convertBtn.disabled = true;
    convertBtn.querySelector('.btn-text').textContent = 'Select a video to start';
    
    // Reset progress
    progressFill.style.width = '0%';
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// ===== Convert Function =====
convertBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    
    // Disable button
    convertBtn.disabled = true;
    convertBtn.querySelector('.btn-text').textContent = 'Converting...';
    
    // Show progress
    progressContainer.classList.add('show');
    progressFill.style.width = '0%';
    progressText.textContent = 'Uploading video...';
    
    // Hide previous results
    downloadSection.classList.remove('show');
    statusMessage.classList.remove('show');
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('video', selectedFile);
        
        // Simulate upload progress
        progressFill.style.width = '20%';
        
        // Upload and convert
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData
        });
        
        progressFill.style.width = '50%';
        progressText.textContent = 'Converting to HD...';
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Conversion failed');
        }
        
        progressFill.style.width = '80%';
        progressText.textContent = 'Finalizing...';
        
        // Get the converted video as blob
        convertedBlob = await response.blob();
        
        progressFill.style.width = '100%';
        progressText.textContent = 'Complete!';
        
        // Create download link
        const url = URL.createObjectURL(convertedBlob);
        downloadBtn.href = url;
        downloadBtn.download = 'HD_' + selectedFile.name;
        
        // Show success
        setTimeout(() => {
            progressContainer.classList.remove('show');
            downloadSection.classList.add('show');
            showStatus('Video berhasil dikonversi ke HD quality!', 'success');
        }, 500);
        
    } catch (error) {
        console.error('Conversion error:', error);
        showStatus('Error: ' + error.message, 'error');
        progressContainer.classList.remove('show');
        
        // Re-enable button
        convertBtn.disabled = false;
        convertBtn.querySelector('.btn-text').textContent = 'Try Again';
    }
});

// ===== Status Message =====
function showStatus(message, type) {
    statusMessage.textContent = message;
    statusMessage.className = 'status-message show ' + type;
    
    // Auto hide after 5 seconds for success/info
    if (type === 'success' || type === 'info') {
        setTimeout(() => {
            statusMessage.classList.remove('show');
        }, 5000);
    }
}

// ===== Download Button =====
downloadBtn.addEventListener('click', () => {
    // Track download
    console.log('Video downloaded:', selectedFile.name);
    
    // Show message
    showStatus('Video downloaded! Upload ke WhatsApp Status sekarang.', 'info');
});

// ===== Animations on Scroll =====
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe elements
document.querySelectorAll('.feature-card, .step, .converter-card').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(30px)';
    el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(el);
});

// ===== Prevent accidental page leave during conversion =====
window.addEventListener('beforeunload', (e) => {
    if (progressContainer.classList.contains('show')) {
        e.preventDefault();
        e.returnValue = '';
        return '';
    }
});

// ===== Console Welcome Message =====
console.log('%c🎬 WhatsApp HD Converter', 'font-size: 20px; font-weight: bold; color: #25D366;');
console.log('%cFree tool to optimize videos for WhatsApp Status', 'font-size: 14px; color: #666;');
console.log('%cMade with ❤️', 'font-size: 12px; color: #999;');
