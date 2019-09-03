let total_forms = $('#id_ingredientamount_set-TOTAL_FORMS');

let renmove_bar = '<div id="bar_remove" class="bar_add d-flex justify-content-center mb-2"><i class="fas fa-minus py-2 text-black-50"></i></div>';
let bar_managements = $('.bars-management');

function make_inputs(total_forms) {
    let inputs = '' +
        '<div class="form-row">' +
        '<div class="form-group col-md-5">' +
        `<select required name="ingredientamount_set-${total_forms.val()}-ingredient" class="form-control ingredient_input" id="id_ingredientamount_set-${total_forms.val()}-ingredient">` +
        '<option value="" selected>-------</option>' +
        '<option value="1">Farinha de Rosca</option>' +
        '<option value="2">CocaCola</option>' +
        '</select>' +
        '</div>' +
        '<div class="form-group col-md-5">' +
        `<input required type="number" name="ingredientamount_set-${total_forms.val()}-amount" class="form-control" id="id_ingredientamount_set-${total_forms.val()}-amount">` +
        '</div>' +
        '<div class="form-group col-md-2">' +
        `<select required name="ingredientamount_set-${total_forms.val()}-unit" class="form-control" disabled id="id_ingredientamount_set-${total_forms.val()}-unit">` +
        '</select>' +
        '</div>' +
        '</div>';
    return inputs;
}

$('#bar_add').click(function () {
    $('#ingredients_formset').append(make_inputs(total_forms));
    let total = parseInt(total_forms.val());
    total_forms.val(total + 1);
    if (total === 1) bar_managements.prepend(renmove_bar);

});

bar_managements.delegate("#bar_remove", "click",function(event){
    event.preventDefault();
    let total = parseInt(total_forms.val());
    if (total === 2) {
        $('#bar_remove').remove();
    }
    total_forms.val(total - 1);
    let form_row = `#ingredients_formset .form-row:nth-child(${total})`;
    console.log(form_row);
    $(form_row).remove();

});


$("#ingredients_formset").delegate(".ingredient_input", "change",function(event){
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


$(".form-control").click( function () {
   $(this).removeClass('error-input');
   $(this).siblings('.errorlist').remove();
});



$(function () {
$('[data-toggle="tooltip"]').tooltip()
})
