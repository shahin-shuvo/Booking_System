$(document).ready(function () {
    $('#class_info').dataTable({
        "aaSorting": [[0, 'asc']],

    });

    var path=window.location.pathname;
   console.log(path);
    $(function () {
        $('.trigger').click(function () {
            console.log("clicked");

            $('#add_class_btn').click(function () {
                name = $('#add_room_name').val();
                capacity = $('#add_capacity').val();
                console.log(name+capacity);
                if (name.length > 4 && capacity > 0) {
                    var xhttp = new XMLHttpRequest();
                    xhttp.onreadystatechange = function () {
                        if (this.readyState == 4 && this.status == 200) {
                            // Typical action to be performed when the document is ready:
                            console.log(xhttp.responseText);
                            var reply = xhttp.responseText;
                            if (reply == "error") {
                                //$('#room_name').css({'background-color' : '#DD2C00'});
                                showAutoCloseTimerMessage(name);

                            }else{
                                location.reload();
                            }
                        }
                    };
                    if(path=="/ClassUpdate"){
                        xhttp.open("GET", "http://127.0.0.1:5000/class_insert_data?new_name=" + name + "&capacity=" + capacity, true);
                    }
                    else if(path=="/LabUpdate"){
                        xhttp.open("GET", "http://127.0.0.1:5000/lab_insert_data?new_name=" + name + "&capacity=" + capacity, true);
                    }
                    xhttp.send();
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
    showCancelMessage(name, row);

}

function showCancelMessage(room, row) {
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

            xhttp.open("GET", "http://127.0.0.1:5000/class_delete?name=" + name, true);
            xhttp.send();
        }
    });
}

function edit_row(row) {
    var row = row.parentNode.parentNode;
    var path=window.location.pathname;
    //console.log(typeof (p));
    console.log(row);
    var prev_name = row.childNodes[1].textContent;
    var capacity = row.childNodes[3].textContent;
    console.log(prev_name);
    $('#room_name').val(prev_name);
    $('#capacity').val(capacity);

    $('#update').click(function () {
        var new_name = $('#room_name').val();

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                // Typical action to be performed when the document is ready:
                console.log(xhttp.responseText);
                var reply = xhttp.responseText;
                if (reply == "error") {
                    //$('#room_name').css({'background-color' : '#DD2C00'});
                    showAutoCloseTimerMessage(new_name);

                }else{
                    location.reload();
                }
            }
        };
        if(path=="/ClassUpdate"){
            xhttp.open("GET", "http://127.0.0.1:5000/class_update_data?old_name=" + prev_name + "&new_name=" + new_name + "&capacity=" + capacity, true);
        }else if(path=="/LabUpdate"){
            xhttp.open("GET", "http://127.0.0.1:5000/lab_update_data?old_name=" + prev_name + "&new_name=" + new_name + "&capacity=" + capacity, true);
        }

        xhttp.send();
        console.log(prev_name + " " + new_name + " " + capacity);
    });

}

function showAutoCloseTimerMessage(new_name) {
    var path=window.location.pathname;
    var type_name;
    if(path=="/ClassUpdate"){
        type_name="Room";
    }else if(path=="/LabUpdate"){
        type_name="Lab";
    }
    swal({
        title: "Error!",
        text: type_name+" " + new_name + " already exists",
        timer: 1500,
        showConfirmButton: false

    });
}

function showAutoCloseTimerMessage_add() {
    swal({
        title: "Error!",
        text: "Enter a vallid name",
        timer: 1500,
        showConfirmButton: false

    });
}



