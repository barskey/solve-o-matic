$( document ).ready( function() {

    function update_setting(data) {
        console.log(data);
    }

    $( ".settings-btn ").click( function() {
        var id = $( this ).attr( "id" );
        var ary = id.split("-");
        var gripper = ary[0];
        var cmd = ary[1];
        var value = ary[2];
        if (value == "cmd")
        {
            $.post("/move_gripper", {
                gripper: gripper,
                cmd: cmd
            });
        }
        else
        {
            $.post("/set_calibrate", {
                setting: gripper,
                value: value
            }).done(function(response) {
                update_setting(response.data);
            }).error(function() {
                console.log("Error setting calibration data.");
            });
        }
    });

});