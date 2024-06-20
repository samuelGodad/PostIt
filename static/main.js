document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('upload-form');
    const videoInput = document.getElementById('video');
    const videoContainer = document.getElementById('video-container');
    const uploadedVideo = document.getElementById('uploaded-video');
    const loadingSpinner = document.getElementById('loading-spinner');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        loadingSpinner.style.display = 'block';
        uploadedVideo.style.display = 'none';

        const formData = new FormData(form);
        const xhr = new XMLHttpRequest();

        xhr.open('POST', '/uploads', true);

        xhr.onload = function() {
            loadingSpinner.style.display = 'none';

            if (xhr.status === 200) {
                const response = JSON.parse(xhr.responseText);
                uploadedVideo.src = response.video_url;
                uploadedVideo.style.display = 'block';
            } else {
                alert('Error uploading video');
            }
        };

        xhr.send(formData);
    });
});