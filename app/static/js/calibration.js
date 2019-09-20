$( document ).ready( function() {
    var sites;

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

    $( ".move-btn" ).click( function() {
        var gripper = $( this ).attr( "data-grip" );
        var setting = $( this ).attr( "data-val" );
        console.log(gripper);
        console.log(setting);
        $.post( "/move_gripper", {
            gripper: gripper,
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
    });

    $( ".cal-btn" ).click( function() {
        var prop = $( this ).attr( "data-prop" );
        var setting = $( this ).attr( "data-setting" );
        var val = $( this ).attr( "data-val" );
        $.post( "/set_cal_data", {
            prop: prop,
            setting: setting,
            val: val
        }).done( function( response ) {
            var id = response.prop + "-" + response.setting + "-value";
            $( "#" + id ).addClass( 'text-warning' ).text( response.value );
            $( "#cal-results" ).text( "Saved calibration setting." )
        }).fail( function() {
            $( "#cal-results" ).text( "Failed to set calibrate settings." )
        });
    });
});