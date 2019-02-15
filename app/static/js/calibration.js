$( document ).ready( function() {

    $( ".cal-btn" ).click( function() {
        var id = $( this ).attr( "id" );
        var ary = id.split( "-" );
        var gripper = ary[0];
        var setting = ary[1];
        var mod = ary[2];
        if (mod == "move")
        {
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
        }
        else
        {
            $.post( "/set_cal_data", {
                gripper: gripper,
                setting: setting,
                mod: mod
            }).done( function( response ) {
                var id = response.gripper + "-" + response.setting + "-value";
                console.log(id);
                $( "#" + id ).addClass( 'text-warning' ).text( response.value );
                $( "#cal-results" ).text( "Saved calibration setting." )
            }).fail( function() {
                $( "#cal-results" ).text( "Failed to set calibrate settings." )
            });
        }
    });

});