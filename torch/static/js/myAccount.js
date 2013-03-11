$(document).ready(function() {
    $('a.my-account').click(function(e) {
        console.log('test');
        e.preventDefault();
        $('form.my-account-form').submit();
    });
});
