document.addEventListener('DOMContentLoaded', function () {
    function renumberSteps() {
        const stepsContainer = document.getElementById('steps');
        const stepElements = stepsContainer.querySelectorAll('.step');

        stepElements.forEach((step, index) => {
            const labelElement = step.querySelector('label');
            if (labelElement) {
                labelElement.textContent = `Step ${index + 1}:`;
            }
        });
    }

    function addStepField() {
        const stepsContainer = document.getElementById('steps');
        const newStepId = stepsContainer.children.length + 1;

        const newStep = document.createElement('div');
        newStep.classList.add('step', 'col-md-12', 'my-2');
        newStep.dataset.stepId = newStepId;

        newStep.innerHTML = `
            <div class="row">
                <div class="col-auto align-self-center pe-0">
                    <label for="id_instructions_${newStepId}">Step ${newStepId}:</label>
                </div>
                <div class="col-md-10">
                    <input type="text" name="instructions" id="id_instructions_${newStepId}" class="form-control">
                </div>
                <div class="col-auto ps-0">
                    <button type="button" class="btn btn-warning btn-circle btn-circle-sm m-1 remove-step align-self-center" onclick="removeStepField(this)">
                        <i class="bi bi-dash remove-step"></i>
                    </button>
                </div>
            </div>
        `;

        stepsContainer.appendChild(newStep);
        renumberSteps();
    }

    function removeStepField(button) {
        const stepContainer = button.closest('.step');
        stepContainer.remove();
        renumberSteps();
    }

    document.querySelector('.add-step').addEventListener('click', addStepField);

    document.addEventListener('click', function (event) {
        const clickedElement = event.target;
        if (clickedElement.classList.contains('remove-step')) {
            event.preventDefault();
            removeStepField(clickedElement);
        }
    });
});