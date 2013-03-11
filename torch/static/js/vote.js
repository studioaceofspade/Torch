$(document).ready(function() {
    $('a.like-this-idea').click(function(e) {
        var $that = $(this);
        e.preventDefault();
        $.ajax({
            url: $(this).data('url'),
            success: function(data) {
                if(data.created === true) {
                    var $tally = $that.prev();
                    var num_votes = $tally.html();
                    $tally.html(parseInt(num_votes, 10) + 1);
                }
            }
        });
    });
});
