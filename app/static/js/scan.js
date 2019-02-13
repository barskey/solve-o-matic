$( document ).ready( function() {
    const screenshotButton = $( '#screenshot-button' );
    const img = $( '#screenshot img' );
    const video = $( '#video' )[0]; // gets the DOM object from the jquery object

    const constraints = {
        video: {width: {exact: 160}, height: {exact: 160}}
    };

    const canvas = document.createElement( 'canvas' );

    navigator.mediaDevices.getUserMedia( constraints ).then(
        function(stream) {
            console.log("Capturing video...");
            video.srcObject = stream;
        }, function(error) {
            console.error('Error: ', error);
        }
    );

    // TODO - convert button click to ajax call to take video screenshot
    screenshotButton.click( function() {
        console.log("Screenshot btn clicked.");
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        canvas.getContext( '2d' ).drawImage( video, 0, 0 );
        // Other browsers will fall back to image/png
        img.src = canvas.toDataURL( 'image/webp' );
    });

    function handleSuccess( stream ) {
        console.log("Capturing video...");
        console.log(video);
        video.srcObject = stream;
    }

    function handleError( error ) {
        console.error('Error: ', error);
    }
});
