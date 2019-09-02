$("#id_ingredient").change(function () {
    let unit = $("#id_unit");
    if (this.value) {
        jQuery.get(
            '/manager/ingredient/ingredient_id/unit/available'.replace('ingredient_id', this.value),
            function (data) {
                console.log(data);
                unit.find('option').remove();
                console.log(data)
                for (const [key, value] of Object.entries(data)) {
                    unit.append(new Option(value, key));
                }

                unit.prop('disabled', false);

            });
    } else {
        unit.find('option').remove();
        unit.prop('disabled', true);
    }
});