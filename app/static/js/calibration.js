$( document ).ready( function() {
    var sites_left, sites_top, sites_size, sites_pitch;

    function get_sites() {
        $.post( "/get_sites" )
        .done( function( response ) {
            sites_left = response.left;
            sites_top = response.top;
            sites_pitch = response.pitch;
            sites_size = response.size;
            draw_sites();
        });
    }

    function draw_sites() {
        var canvas = $( "#sites-canvas" )[0]
        var sc = canvas.getContext( "2d" );
        sc.clearRect(0, 0, canvas.width, canvas.height);
        sc.strokeStyle = "#FFFFFF"
        for ( var r = 0; r < 3; r++ ) {
            for ( var c = 0; c < 3; c++ ) {
                sc.strokeRect ( sites_left + (c * sites_pitch), sites_top + (r * sites_pitch), sites_size, sites_size );
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