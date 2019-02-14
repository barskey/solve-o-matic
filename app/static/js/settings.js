$( document ).ready( function() {

    function update_setting(data) {
        console.log(data);
    }

    $( ".settings-btn ").click( function() {
        var id = $( this ).attr( "id" );
        var ary = id.split("-");
        var gripper = ary[0];
        var setting = ary[1];
        var mod = ary[2];
        if (mod == "move")
        {
            $.post( "/move_gripper", {
                gripper: gripper,
                cmd: setting
            }).done( function(response) {
                console.log(response);
            });
        }
        else
        {
            $.post( "/set_calibrate", {
                gripper: gripper,
                setting: setting,
                mod: mod
            }).done( function( response ) {
                var id = response.gripper + "-" + response.setting + "-value";
                console.log(id);
                $( "#" + id ).addClass( 'text-warning' ).text( response.value );
            }).fail( function() {
                console.log( "Failed to set calibrate settings." );
            });
        }
    });

});