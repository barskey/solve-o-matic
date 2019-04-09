$( document ).ready( function() {
    var sites;

    const video = $( "#video" )[0]; // [0] gets the DOM object from the jquery object

    const constraints = {
        video: {width: {exact: 160}, height: {exact: 160}}
    };

    // start the camera streaming
    navigator.mediaDevices.getUserMedia( constraints ).then(
        function(stream) {
            console.log("Capturing video...");
            video.srcObject = stream;
        }, function(error) {
            console.error("Error: ", error);
        }
    );

    function get_sites() {
        $.post( "/get_sites" )
        .done( function( response ) {
            sites = response.sites;
            draw_sites();
        });
    }

    var canvas = $( "#sites-canvas" )[0]
    var sc = canvas.getContext( "2d" );
    function draw_sites() {
        sc.clearRect(0, 0, canvas.width, canvas.height);
        sc.strokeStyle = "#FFFFFF"
        for ( var r = 0; r < 3; r++ ) {
            for ( var c = 0; c < 3; c++ ) {
                sc.strokeRect ( sites.tlx + (c * sites.pitch), sites.tly + (r * sites.pitch), sites.size, sites.size );
            }
        }
    }

    get_sites();

    $( ".set-btn" ).click( function() {
        var id = $( this ).attr( "id" );
        var ary = id.split( "-" );
        var prop = ary[0];
        var setting = ary[1];
        var mod = ary[2];
        $.post( "/set_cal_data", {
            prop: prop,
            setting: setting,
            mod: mod
        }).done( function( response ) {
            get_sites();
            draw_sites();
        }).fail( function() {
            $( "#cal-results" ).text( "Failed to set calibrate settings." )
        });
    });

    $( ".cal-btn" ).click( function() {
        var id = $( this ).attr( "id" );
        var ary = id.split( "-" );
        var prop = ary[0];
        var setting = ary[1];
        var mod = ary[2];
        if (mod == "move")
        {
            $.post( "/move_gripper", {
                gripper: prop,
                cmd: setting
            }).done( function( response ) {
                var msg;
                if ( response.code < 0) {
                    msg = "Error: " + response.msg;
                } else {
                    msg = "Success"
                }
                $( "#cal-results" ).text( msg );
            });
        }
        else
        {
            $.post( "/set_cal_data", {
                prop: prop,
                setting: setting,
                mod: mod
            }).done( function( response ) {
                var id = response.prop + "-" + response.setting + "-value";
                console.log(id);
                $( "#" + id ).addClass( 'text-warning' ).text( response.value );
                $( "#cal-results" ).text( "Saved calibration setting." )
            }).fail( function() {
                $( "#cal-results" ).text( "Failed to set calibrate settings." )
            });
        }
    });
});