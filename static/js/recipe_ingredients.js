document.addEventListener('DOMContentLoaded', function () {
    let ingredientCounter = 0;

    function addIngredientField() {
        const ingredientsContainer = document.getElementById('ingredients');
        const newIngredientId = ++ingredientCounter;

        const newIngredient = document.createElement('div');
        newIngredient.classList.add('ingredient', 'row', 'mb-4');

        newIngredient.innerHTML = `
            <div class="col-md-1">
                <label for="amount-${newIngredientId}" class="form-label">Amount:</label>
                <input type="text" name="amounts" id="amount-${newIngredientId}" class="form-control">
            </div>
            <div class="col-md-1">
                <label for="unit-${newIngredientId}" class="form-label">Unit:</label>
                <select class="form-select" id="unit-${newIngredientId}" name="amountUnits">
                    <option value="gr">gr</option>
                    <option value="kg">kg</option>
                    <option value="spoon">Spoon</option>
                </select>
            </div>
            <div class="col-md-9">
                <label for="ingredient-${newIngredientId}" class="form-label">Ingredient:</label>
                <input type="text" name="ingredients" id="ingredient-${newIngredientId}" class="form-control">
            </div>
            <button type="button" class="btn btn-warning btn-circle btn-circle-sm m-1 remove-ingredient col-md-1 align-self-end" onclick="removeIngredientField(this)">
                <i class="bi bi-dash remove-ingredient"></i>
            </button>
        `;

        ingredientsContainer.appendChild(newIngredient);
        renumberIngredients();
    }

    function removeIngredientField(button) {
        const ingredientContainer = button.closest('.ingredient');
        ingredientContainer.remove();
        renumberIngredients();
    }

    function renumberIngredients() {
        const ingredientsContainer = document.getElementById('ingredients');
        const ingredientElements = ingredientsContainer.querySelectorAll('.ingredient');

        ingredientElements.forEach((ingredient, index) => {
            const numberElement = ingredient.querySelector('h1');
            if (numberElement) {
                numberElement.textContent = index + 1;
            }
        });
    }

    document.querySelector('.add-ingredient').addEventListener('click', addIngredientField);

    document.addEventListener('click', function (event) {
        const clickedElement = event.target;
        if (clickedElement.classList.contains('remove-ingredient')) {
            event.preventDefault();
            removeIngredientField(clickedElement);
        }
    });
});