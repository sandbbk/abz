
    $(document).ready(function () {
        $("#aj_form").click(function() {
            $.ajax({
                url: 'ajx',
                type: 'POST',
                async: true,
                dataType: 'json',
                data: $('#aj_form').serialize(),
                success: function(data) {
                    document.getElementById('aj_ch').innerHTML = '';
                    $("#aj_ch").append(data['response']);
                },
            });
        });
    });

