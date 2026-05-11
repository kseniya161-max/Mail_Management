$('.select2').select2({
    placeholder: "Выберите город",
    allowClear: true,
    width: '100%',
    language: 'ru',
    matcher: function(params, data) {
        return $.fn.select2.defaults.defaults.matcher(params, data);
    }
});