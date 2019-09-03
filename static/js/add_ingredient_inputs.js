let total_forms = $('#id_ingredientamount_set-TOTAL_FORMS');
let initial = parseInt(total_forms.val());

let renmove_bar = '<div id="bar_remove" class="bar_add d-flex justify-content-center mb-2"><i class="fas fa-minus py-2 text-black-50"></i></div>';
let bar_managements = $('.bars-management');
let empty_form;

$('#bar_add').click(function () {
    let total = parseInt(total_forms.val());
    // $('#ingredients_formset').append(make_inputs(total_forms));
    $('#rows-input').append(empty_form.replace(/__prefix__/g, total));
    total_forms.val(total + 1);
    if (total === initial) bar_managements.prepend(renmove_bar);

});

bar_managements.delegate("#bar_remove", "click", function (event) {
    event.preventDefault();
    let total = parseInt(total_forms.val());
    if (total === initial + 1) {
        $('#bar_remove').remove();
    }
    total_forms.val(total - 1);
    let form_row = `#rows-input .form-row:nth-of-type(${total})`;
    $(form_row).remove();

});


$("#ingredients_formset").delegate(".ingredient_input", "change", function (event) {
    event.preventDefault();
    let unit_id = this.id.replace('-ingredient', '-unit');
    let unit = $(`#${unit_id}`);
    if (this.value) {
        jQuery.get(
            '/manager/ingredient/ingredient_id/unit/available'.replace('ingredient_id', this.value),
            function (data) {
                unit.find('option').remove();
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


$(".form-control").click(function () {
    $(this).removeClass('error-input');
    $(this).siblings('.errorlist').remove();
});


$(function () {
    $('[data-toggle="tooltip"]').tooltip()
});

$(document).ready(function () {
    empty_form = $('#empty_form div')[0].outerHTML;
    $('#empty_form').remove();
});