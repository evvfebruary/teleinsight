document.getElementById('toggleButton').addEventListener('click', function() {
    const textInputGroup = document.getElementById('textInputGroup');
    const fileInputGroup = document.getElementById('fileInputGroup');
    const toggleButton = document.getElementById('toggleButton');

    if (textInputGroup.style.display === 'none') {
        textInputGroup.style.display = 'flex';
        fileInputGroup.style.display = 'none';
        toggleButton.textContent = 'Switch to Drag & Drop';
    } else {
        textInputGroup.style.display = 'none';
        fileInputGroup.style.display = 'flex';
        toggleButton.textContent = 'Switch to Text Input';
    }
});

document.getElementById('dragDropArea').addEventListener('click', function() {
    document.getElementById('fileInput').click();
});

document.getElementById('fileInput').addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('dragDropArea').textContent = `Selected file: ${file.name}`;
    }
});

document.getElementById('textForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const textInput = document.getElementById('textInput').value;
    const fileInput = document.getElementById('fileInput').files[0];
    const responseDiv = document.getElementById('response');
    const thumbnailsDiv = document.getElementById('thumbnails');
    const progressDiv = document.getElementById('progress');
    const progressText = document.getElementById('progressText');
    let formData = new FormData();

    if (textInput) {
        formData.append('text', textInput);
    } else if (fileInput) {
        formData.append('file', fileInput);
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
