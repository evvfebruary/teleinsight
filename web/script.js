document.addEventListener('DOMContentLoaded', function() {
    const textInputGroup = document.getElementById('textInputGroup');
    const fileInputGroup = document.getElementById('fileInputGroup');
    const textInput = document.getElementById('textInput');
    const fileInput = document.getElementById('fileInput');
    const toggleButton = document.getElementById('toggleButton');
    const dragDropArea = document.getElementById('dragDropArea');
    const responseDiv = document.getElementById('response');
    const thumbnailsDiv = document.getElementById('thumbnails');
    const progressDiv = document.getElementById('progress');
    const progressText = document.getElementById('progressText');
    const textForm = document.getElementById('textForm');

    toggleButton.addEventListener('click', function() {
        if (textInputGroup.style.display === 'none') {
            textInputGroup.style.display = 'flex';
            textInput.required = true;
            fileInputGroup.style.display = 'none';
            fileInput.required = false;
            toggleButton.textContent = 'Switch to Drag & Drop';
        } else {
            textInputGroup.style.display = 'none';
            textInput.required = false;
            fileInputGroup.style.display = 'flex';
            fileInput.required = true;
            toggleButton.textContent = 'Switch to Text Input';
        }
    });

    dragDropArea.addEventListener('click', function() {
        if (fileInput) {
            fileInput.click();
        } else {
            console.error('File input element not found.');
        }
    });

    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            dragDropArea.textContent = `Selected file: ${file.name}`;
        }
    });

    textForm.addEventListener('submit', function(event) {
        event.preventDefault();

        let formData = new FormData();

        if (textInput && textInput.value) {
            formData.append('text', textInput.value);
        } else if (fileInput && fileInput.files.length > 0) {
            formData.append('file', fileInput.files[0]);
        } else {
            responseDiv.style.display = 'block';
            responseDiv.textContent = 'Please enter text or select a file.';
            responseDiv.classList.remove('alert-info');
            responseDiv.classList.add('alert-danger');
            return;
        }

        // Show progress message
        progressDiv.style.display = 'block';
        progressText.textContent = '';
        let progressMessage = "Что ты от меня хочешь я родился за 5 минут";
        let index = 0;

        const typingInterval = setInterval(() => {
            progressText.textContent += progressMessage[index];
            index++;
            if (index >= progressMessage.length) {
                index = 0;
                progressText.textContent = '';
            }
        }, 50);  // Speed up typing

        fetch('http://127.0.0.1:8000/api', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            clearInterval(typingInterval);
            progressDiv.style.display = 'none';
            responseDiv.style.display = 'block';
            responseDiv.textContent = 'Response received.';
            responseDiv.classList.remove('alert-danger');
            responseDiv.classList.add('alert-info');
            thumbnailsDiv.innerHTML = ''; // Clear previous thumbnails

            data.forEach((item, index) => {
                const colDiv = document.createElement('div');
                colDiv.className = 'col-md-3 thumbnail';

                const img = document.createElement('img');
                img.src = `data:image/png;base64,${item.image_data}`;
                img.alt = `Image ${index + 1}`;
                img.addEventListener('click', () => {
                    showModalImage(img.src);
                });

                const descriptionDiv = document.createElement('div');
                descriptionDiv.className = 'description';
                descriptionDiv.textContent = item.text_description.join(', ');

                colDiv.appendChild(img);
                colDiv.appendChild(descriptionDiv);
                thumbnailsDiv.appendChild(colDiv);
            });
        })
        .catch(error => {
            clearInterval(typingInterval);
            progressDiv.style.display = 'none';
            responseDiv.style.display = 'block';
            responseDiv.textContent = 'Error: ' + error;
            responseDiv.classList.remove('alert-info');
            responseDiv.classList.add('alert-danger');
        });
    });

    function showModalImage(src) {
        const modalImage = document.getElementById('modalImage');
        modalImage.src = src;
        $('#imageModal').modal('show');
    }
});
