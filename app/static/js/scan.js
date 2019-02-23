$( document ).ready( function() {
    var sites;
    const face_tl = {
        "U": [45,55],
        "F": [45,100],
        "D": [45,145],
        "L": [0,100],
        "R": [90,100],
        "B": [135,100]
    }

    const video = $( "#video" )[0]; // [0] gets the DOM object from the jquery object

    const constraints = {
        video: {width: {exact: 160}, height: {exact: 160}}
    };

    function get_sites() {
        $.post( "/get_sites" )
        .done( function( response ) {
            sites = response.sites;
            draw_sites();
        });
    }

    get_sites();

    // canvas for drawing cube site boxes on
    var cc = $( "#cube-flat" )[0].getContext( "2d" );
    var blank = "#000000";
    for (var face in face_tl) {
        drawFace(face, [blank, blank, blank, blank, blank, blank, blank, blank, blank]);
    }

    function drawFace( face, siteColors ) {
        var i = 0;
        for ( var r = 0; r < 3; r++ ) {
            for ( var c = 0; c < 3; c++) {
                var x = face_tl[face][0] + (15 * c);
                var y = face_tl[face][1] + (15 * r);
                cc.fillStyle = siteColors[i];
                cc.fillRect( x, y, 15, 15 );
                cc.strokeStyle = "#707070";
                cc.strokeRect( x, y, 15, 15 );
                i++;
            }
        }
        cc.strokeStyle = "black";
        cc.strokeRect( face_tl[face][0], face_tl[face][1], 45, 45 );
    }

    // canvas for drawing cube site boxes over camera view
    var camc = $( "#cam-view" )[0].getContext( "2d" );

    function drawCamView( siteColors, unsureColors ) {
        var i = 0;
        for ( var r = 0; r < 3; r++ ) {
            for ( var c = 0; c < 3; c++) {
                var x = sites.tlx + (sites.pitch * c);
                var y = sites.tly + (sites.pitch * r);
                console.log(x,y);
                camc.fillStyle = siteColors[i];
                camc.fillRect( x, y, sites.size, sites.size );
                camc.strokeStyle = "#707070";
                unsureColors.forEach(site => {
                    if (i == site) {
                        camc.strokeStyle = "#00FF00";
                    }
                });
                camc.strokeRect( x, y, sites.size, sites.size );
                i++;
            }
        }
    }

    // canvas for capturing img from video
    const canvas = document.createElement( "canvas" );
    canvas.width = 160;
    canvas.height = 160;

    // start the camera streaming
    navigator.mediaDevices.getUserMedia( constraints ).then(
        function(stream) {
            console.log("Capturing video...");
            video.srcObject = stream;
        }, function(error) {
            console.error("Error: ", error);
        }
    );

    $( "#scan-next" ).click( function() {
        if ($( this ).text() == "Start") {
            $( this ).attr( { "disabled": true } );
            $( "#scan-status" ).text( "Gripping..." );
            $.post( "/scan_next", { start: true })
            .done( function ( response ) {
                $( "#scan-next" ).removeAttr( "disabled" ).text( "Next..." );
                $( "#scan-status" ).html( "Does everything look OK?<br />Adjust position if necessary." );
            });
        } else {
            $( this ).attr( { "disabled": true } );
            $( "#scan-status" ).text( "Moving to position..." );
            $.post( "/scan_next", { start: false })
            .done( function( response ) {
                grabImage( response.upface );
            });
        }
    });

    function grabImage( upface ) {
        //draw image to canvas. scale to target dimensions
        var ctx = canvas.getContext( "2d" );
        ctx.drawImage( video, 0, 0, canvas.width, canvas.height );
        //convert to desired file format
        var dataURI = canvas.toDataURL( 'image/png' );
        $.post( '/process_img', { imgdata: dataURI, face: upface })
        .done( function( response ) {
            drawFace( response.face, response.colors );
            //var colors = ["#FF0000","#FFFF00","#FF00FF","#00FF00","#0000FF","#FFFFFF","#FF0F00F","#FFF000","#FFFF00"]
            drawCamView( response.colors, response.unsure );
            if ( response.unsure.length > 0 ) {
                console.warn("Unsure Sites!");
            }
            console.log(response.unsure);
        });
    }

});