$(document).ready(function () {
        $("#del").click(function() {
            $.ajax({
                url: 'del',
                type: 'POST',
                async: true,
                dataType: 'json',
                data: $('#del').serialize(),
                success: function(data) {
                    document.getElementById('change').innerHTML = '';
                    $("#change").append(data['response']);

                },
                error: function (){alert("error");},
            });
        });
    });