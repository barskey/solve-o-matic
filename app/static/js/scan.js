$( document ).ready( function() {
    const video = $( "#video" )[0]; // [0] gets the DOM object from the jquery object

    const constraints = {
        video: {width: {exact: 160}, height: {exact: 160}}
    };

    const canvas = document.createElement( "canvas" );
    canvas.width = 160;
    canvas.height = 160;
    console.log(canvas.width, canvas.height);

    // start the camera streaming
    navigator.mediaDevices.getUserMedia( constraints ).then(
        function(stream) {
            console.log("Capturing video...");
            video.srcObject = stream;
        }, function(error) {
            console.error("Error: ", error);
        }
    );

    // TODO - convert button click to ajax call to take video screenshot
    $( '#scan-next' ).click( function() {
        //draw image to canvas. scale to target dimensions
        var ctx = canvas.getContext( "2d" );
        ctx.drawImage( video, 0, 0, canvas.width, canvas.height );
        //convert to desired file format
        var dataURI = canvas.toDataURL( 'image/png' );
        console.log(dataURI);
        $.post( '/scan', { imgdata: dataURI })
        .done( function(response) {
            console.log(response);
        });

    });
});