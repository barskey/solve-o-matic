$( document ).ready( function() {
    const captureVideoButton = $( '#capture-button' );
    const screenshotButton = $( '#screenshot-button' );
    const img = $('#screenshot-img');
    const video = $('#screenshot-video');

    const canvas = document.createElement('canvas');

    captureVideoButton.onclick = function() {
        console.log("Capture btn clicked.");
        navigator.mediaDevices.getUserMedia(constraints).
        then(handleSuccess).catch(handleError);
    };

    screenshotButton.onclick = video.onclick = function() {
        console.log("Screenshot btn clicked.");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        // Other browsers will fall back to image/png
        img.src = canvas.toDataURL('image/webp');
    };

    function handleSuccess(stream) {
        screenshotButton.disabled = false;
        video.srcObject = stream;
    }
});
