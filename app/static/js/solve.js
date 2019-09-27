$( document ).ready( function() {

    function update_solve( solveto ) {
        $.post( "/update_solve", {
            solve_to: solveto
        })
        .done( function ( response ) {
            var img = "/static/images/" + response.solve_img;
            $( "#solve-img" ).attr( "src", img );
            $( "#solve-to" ).text( response.solve_to );
            $( "#moves" ).text( response.moves );
        });
    }

    update_solve( "Solid Cube" ); // refresh the solve image and stats on load

    $( "#solveTo" ).change( function() {
        update_solve( $( this ).children( "option:selected" ).val() );
    });

});