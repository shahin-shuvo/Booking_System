$(document).ready(function () {
    $('#class_info').dataTable({
        "aaSorting": [[0, 'asc']],

    });

    var path = window.location.pathname;
    console.log(path);
    $(function () {
        $('.trigger').click(function () {
            // console.log("clicked");

            $('#add_class_btn').click(function () {
                var name = $('#add_name').val();
                var capacity = $('#add_capacity').val();
                var address = $('#add_address').val();
                var details = $('#add_details').val();
                // console.log(name+capacity+address+details+ "   be");
                if (name.length > 3 && capacity > 0) {
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function () {
                        if (this.readyState == 4 && this.status == 200) {
                            // Typical action to be performed when the document is ready:
                            console.log(xhttp.responseText);
                            var reply = xhttp.responseText;
                            if (reply == "error") {
                                //$('#room_name').css({'background-color' : '#DD2C00'});
                                showAutoCloseTimerMessage(name);

                            } else {
                                location.reload();
                            }
                        }
                    };
                    if (path == "/AuditoriumUpdate") {
                        xhttp.open("POST", "http://127.0.0.1:5000/auditorium_insert_data?new_name=" + name +
                               "&address="+address+"&details="+details+"&capacity=" + capacity, true);
                    }
                    else if (path == "/FieldUpdate") {
                        xhttp.open("POST", "http://127.0.0.1:5000/field_insert_data?new_name=" + name +
                               "&address="+address+"&details="+details+"&capacity=" + capacity, true);
                    }
                    xhttp.send();
                    // console.log(name+address+capacity+details);
                } else {
                    showAutoCloseTimerMessage_add();
                }
            });

        });

    })
});

function delete_row(row) {
    var row = row.parentNode.parentNode;
    //console.log(typeof (p));
    //console.log(row);
    var name = row.childNodes[1].textContent;
    //console.log(name);
    var path = window.location.pathname;
    showCancelMessage(name, row, path);

}

function showCancelMessage(room, row, path) {
    swal({
        title: "Are you sure?",
        text: room + " will be deleted!",
        type: "warning",
        showCancelButton: true,
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Yes, delete it!",
        cancelButtonText: "No, cancel!",
        closeOnConfirm: false,
        closeOnCancel: true
    }, function (isConfirm) {
        if (isConfirm) {

            swal("Deleted!", "Room " + room + " is deleted", "success");
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4 && this.status == 200) {

                    var reply = xhttp.responseText;
                    if (reply == "Success") {
                        row.parentNode.removeChild(row);
                    }

                }
            };
            if (path == "/AuditoriumUpdate") {
                xhttp.open("GET", "http://127.0.0.1:5000/auditorium_delete?name=" + room, true);
            } else if (path == "/FieldUpdate") {
                xhttp.open("GET", "http://127.0.0.1:5000/field_delete?name=" + room, true);
            }

            xhttp.send();
        }
    });
}

function edit_row(row) {
    var row = row.parentNode.parentNode;
    var path = window.location.pathname;
    //console.log(typeof (p));
    console.log(row);
    var prev_name = row.childNodes[1].textContent;
    var capacity = row.childNodes[5].textContent;
    var address = row.childNodes[3].textContent;
    var details = row.childNodes[7].textContent
    console.log(prev_name + "  " + address + " " + address + " " + details);
    $('#name').val(prev_name);
    $('#capacity').val(capacity);
    $('#address').val(address);
    $('#details').val(details);

    $('#update').click(function () {
        var new_name = $('#name').val();
        capacity = $('#capacity').val();
        address = $('#address').val();
        details = $('#details').val();
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                // Typical action to be performed when the document is ready:
                console.log(xhttp.responseText);
                var reply = xhttp.responseText;
                if (reply == "error") {
                    //$('#room_name').css({'background-color' : '#DD2C00'});
                    showAutoCloseTimerMessage(new_name);

                } else {
                    location.reload();
                }
            }
        };
        if (path == "/AuditoriumUpdate") {
            xhttp.open("POST", "http://127.0.0.1:5000/auditorium_update_data?old_name=" + prev_name +
                "&new_name=" + new_name + "&address=" + address + "&capacity=" + capacity + "&details=" + details, true);
        } else if (path == "/FieldUpdate") {
            xhttp.open("POST", "http://127.0.0.1:5000/field_update_data?old_name=" + prev_name +
                "&new_name=" + new_name + "&address=" + address + "&capacity=" + capacity + "&details=" + details, true);
        }

        xhttp.send();
        // console.log(prev_name + " " + new_name + " " + capacity + " " + address + " " + details);
    });

}

function showAutoCloseTimerMessage(new_name) {
    var path = window.location.pathname;
    var type_name;
    if (path == "/AuditoriumUpdate") {
        type_name = "Auditorium";
    } else if (path == "/FieldUpdate") {
        type_name = "Field";
    }
    swal({
        title: "Error!",
        text: type_name + " " + new_name + " already exists",
        timer: 1500,
        showConfirmButton: false

    });
}

function showAutoCloseTimerMessage_add() {
    swal({
        title: "Error!",
        text: "Enter a vallid name or capacity",
        timer: 1500,
        showConfirmButton: false

    });
}



