$(document).ready(function() {
    $('.idea-create-tags a').click(function(e) {
        e.preventDefault();
        $('.idea-create-tags a').removeClass('current');
        $(this).addClass('current');
    });
    $('.submit-your-idea').click(function(e) {
        e.preventDefault();
        var title = $('.title-input input#id_title').val();
        var description = $('.description-input textarea#id_description').val();
        var tag = $('.tag-input a.current').data('val');

        var $submitForm = $('form.submit-form');
        $submitForm.find('input#id_title').val(title);
        $submitForm.find('textarea#id_description').val(description);
        $submitForm.find('select#id_tag').find('option').removeAttr('selected').each(function() {
            if (parseInt($(this).val(), 10) === tag) {
                $(this).attr('selected', 'selected');
            }
        });
        $.ajax({
            type: 'POST',
            url: $submitForm.attr('action'),
            data: $submitForm.serialize(),
            success: function(data) {
                $('a.thepermalink').attr('href', data.url);
                $('.slideshow').cycle.next();
            }
        });
    });
});
