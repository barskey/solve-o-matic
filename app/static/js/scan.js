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

    $.post( "/ready_load" )
    .done( function( reponse ) {  
        $( "#scan-status" ).html( "Place cube with logo\nopposite the camera." );
    });

    function get_sites() {
        $.post( "/get_sites" )
        .done( function( response ) {
            sites = response.sites;
        });
    }

    get_sites();

    // canvas for drawing cube site boxes on
    var cc = $( "#cube-flat" )[0].getContext( "2d" );
    var blank = "#000000";
    for (var face in face_tl) {
        drawFace( face, [blank, blank, blank, blank, blank, blank, blank, blank, blank] );
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

    function drawCamView( siteColors ) {
        var i = 0;
        for ( var r = 0; r < 3; r++ ) {
            for ( var c = 0; c < 3; c++) {
                var x = sites.tlx + (sites.pitch * c);
                var y = sites.tly + (sites.pitch * r);
                //console.log(x,y);
                camc.fillStyle = siteColors[i];
                camc.fillRect( x, y, sites.size, sites.size );
                camc.strokeStyle = "#707070";
                camc.strokeRect( x, y, sites.size, sites.size );
                i++;
            }
        }
    }

    $( "#scan-next" ).click( function() {
        if ( $( this ).text() == "Start" ) {
            $( this ).attr( { "disabled": true } );
            $( "#scan-status" ).text( "Gripping..." );
            $.post( "/scan_next", { start: "true" })
            .done( function ( response ) {
                $( "#scan-next" ).removeAttr( "disabled" ).text( "Go" );
                $( "#scan-status" ).html( "Everything look good? Let's go..." );
            });
        } else {
            $( this ).attr( { "disabled": true } );
            $( "#scan-status" ).text( "Moving to position..." );
            scan_next();
        }
    });

    function scan_next() {
        $.post( "/scan_next", { start: "false" })
        .done( function( response ) {
            drawFace( response.upface, response.colors );
            drawCamView( response.colors );
            console.log( response );
            if (response.result == 0) {
                scan_next();
            }
        });
    }

});