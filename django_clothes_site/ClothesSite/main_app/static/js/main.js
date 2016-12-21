$('.gender-button').on('click', function(event) {
    event.preventDefault();
    var element = $(this);

    //unclicks all other buttons except button of interest (so that no more than one button is clicked at once)
    $('.gender-button').each( function() {
        var button = $(this);
        var gender = button.attr('data');
        if (!(gender === element.attr('data')) && button.hasClass('btn-danger')) {
            button.removeClass('btn-danger').addClass('btn-info');
            $("#" + gender.toLowerCase() + "-form-holder").addClass('collapsed-panel');
        }
    });
    //if button has not yet been clicked by user
    if (element.hasClass('btn-info')) {
        element.removeClass('btn-info').addClass('btn-danger');
        $(id = "#" + element.attr('data').toLowerCase() + "-form-holder").removeClass('collapsed-panel');
    }
    //Case where button has been previously clicked
    else {
        element.removeClass('btn-danger').addClass('btn-info');
        $("#" + element.attr('data').toLowerCase() + "-form-holder").addClass('collapsed-panel');
    }
});

$('.favorite-button').on('click', function(event) {

    event.preventDefault();
    var element = $(this); //button that was clicked
    //if button has not yet been clicked by user
    if (element.hasClass('btn-danger')) {
        $.ajax({
            url : '/favorite_clothes_item/',
            type: 'GET',
            data: { clothes_item_id : element.attr("data-id") },
            success: function(response) {
                element.removeClass("btn-danger");
                element.addClass("btn-success");
            }
        });
    }
    //if button has been previously clicked by user
    else {
        $.ajax({
            url : '/unfavorite_clothes_item/',
            type: 'GET',
            data: { clothes_item_id : element.attr("data-id") },
            success: function(response) {
                element.removeClass("btn-success");
                element.addClass("btn-danger");
            }
        });
    }
});


//Only one gender filter can be applied at a time
$('.gender-filter-button').on('click', function(event) {

    event.preventDefault();
    var element = $(this); //button that was clicked
    btn_unclicked = "btn-warning" //class that all unclicked buttons should have
    btn_clicked = "btn-success"   //class that all clicked buttons should have

    //Case where button has not yet been clicked
    if ( element.hasClass(btn_unclicked) ) {
        //Change visual appearance of all other buttons
        //since only one filter can be applied at once
        $('.gender-filter-button').each( function() {
            $(this).removeClass(btn_clicked);
            $(this).addClass(btn_unclicked);
        });
        //Change visual appearance of newly clicked button
        element.addClass(btn_clicked);
        element.removeClass(btn_unclicked);
        filters = {'gender_filter': element.val()}
        //call to home view
        $.ajax({
            url : 'search/ajax_filter/',
            type: 'GET',
            data: filters,
            success: function() {
                alert("here");
            }
        });
    }
    //Case where button has been previously clicked
    else {
        //Change visual appearance of button
        element.removeClass(btn_clicked);
        element.addClass(btn_unclicked);
        //Do not need to worry about changing appearance of other
        //buttons since only one button can be clicked at any time
        filters = {'gender_filter': 'noFilter'}
        $.ajax({
            url : 'search/ajax_filter/',
            type: 'GET',
            data: filters,
        });
    }
});
