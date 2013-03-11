$(document).ready(function() {
    $('.user-login-input input#id_first_name').hide();
    $('.user-login-input .first-name-label').hide();
    $('.idea-create-tags a').click(function(e) {
        e.preventDefault();
        $('.idea-create-tags a').removeClass('current');
        $(this).addClass('current');
    });
    $('.user-login-input a').click(function(e) {
        if ($(this).hasClass('forgot-password-link')) {
            return;
        }
        e.preventDefault();
        $('.user-login-input a').removeClass('current');
        $(this).addClass('current');
        if ($(this).hasClass('already-have-account')) {
            $('.user-login-input input#id_first_name').hide();
            $('.user-login-input .first-name-label').hide();
        } else {
            $('.user-login-input input#id_first_name').show();
            $('.user-login-input .first-name-label').show();
        }
    });
    $('.submit-your-idea').click(function(e) {
        e.preventDefault();
        var title = $('.title-input input#id_title').val();
        var description = $('.description-input textarea#id_description').val();
        var tag = $('.tag-input a.current').data('val');
        var first_name = $('.user-login-input input#id_first_name').val();
        var username = $('.user-login-input input#id_username').val();
        var password = $('.user-login-input input#id_password').val();

        var $submitForm = $('form.submit-form');
        $submitForm.find('input#id_title').val(title);
        $submitForm.find('textarea#id_description').val(description);
        $submitForm.find('input#id_first_name').val(first_name);
        $submitForm.find('input#id_username').val(username);
        $submitForm.find('input#id_password').val(password);
        $submitForm.find('select#id_tag').find('option').removeAttr('selected').each(function() {
            if (parseInt($(this).val(), 10) === tag) {
                $(this).attr('selected', 'selected');
            }
        });
        if ($('.already-have-account').hasClass('current')) {
            console.log('test');
            $submitForm.find('input#id_first_name').remove();
        }
        var $errors = $('.form-errors-container');
        $.ajax({
            type: 'POST',
            url: $submitForm.attr('action'),
            data: $submitForm.serialize(),
            success: function(data) {
                if (data.url) {
                    $errors.hide();
                    $('a.thepermalink').attr('href', data.url);
                    $('.slideshow').cycle.next();
                } else {
                    $errors.find('.form-errors').html(data.errors);
                    $errors.show();
                    $('.slideshow').cycle(0);
                    //$('.slideshow').cycle.prev();
                    //$('.slideshow').cycle.prev();
                }
            },
            error: function() {
            }
        });
    });
});
