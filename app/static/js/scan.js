$( document ).ready( function() {
    const $captureVideoButton = $( '#capture-button' );
    const $screenshotButton = $( '#screenshot-button' );
    const $img = $( '#screenshot img' );
    const $video = $( '#screenshot video' );

    const constraints = {
        video: {width: {exact: 240}, height: {exact: 120}}
    };

    const canvas = document.createElement( 'canvas' );

    console.log("Capturing video...");
    navigator.mediaDevices.getUserMedia( constraints ).
    then( handleSuccess ).catch( handleError );

    // TODO - convert button click to ajax call to take video screenshot
    $screenshotButton.click( function() {
        console.log("Screenshot btn clicked.");
        canvas.width = $video.videoWidth;
        canvas.height = $video.videoHeight;
        canvas.getContext( '2d' ).drawImage( $video, 0, 0 );
        // Other browsers will fall back to image/png
        $img.src = canvas.toDataURL( 'image/webp' );
    });

    function handleSuccess( stream ) {
        $screenshotButton.disabled = false;
        $video.srcObject = stream;
    }

    function handleError( error ) {
        console.error('Error: ', error);
    }
});
