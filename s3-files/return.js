const url = 'API_URL';

let data = null;

async function fetchData() {
    if (data) {
        console.log('Data already fetched, skipping fetch');
        return;
    }

    console.log('Fetching data...');
    try {
        const response = await fetch(url);
        data = await response.json();
        console.log('Data fetched successfully');
        
        populateDeviceNameContainer();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function submission() {
    const submitButton = document.getElementById('submitButton');
    submitButton.disabled = true;
    submitButton.innerHTML = '<span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true">Loading...';

    const deviceNameFull = document.getElementById('deviceNameContainer').value;
    const deviceName = deviceNameFull.split(' ')[0].trim();
    const payload = {
        'AssetID': deviceName,
        "DeviceType": "",
        "Email": "",
        "Name": "",
        "Reason": ""
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Submission successful:', data);
        alert('Form submitted successfully!');
        window.location.href = 'index.html';
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was a problem submitting the form. Please try again.');
    })
    .finally(() => {
        submitButton.disabled = false;
        submitButton.innerHTML = 'Submit';
    });
}

function populateDeviceNameContainer() {
    const deviceNameContainer = document.getElementById('deviceNameContainer');
    const deviceNameWrapper = document.getElementById('deviceNameWrapper');
    deviceNameContainer.innerHTML = '';

    const defaultOption = new Option("Select Device", "");
    deviceNameContainer.add(defaultOption);

    const filteredData = data.filter(item => 
        (item.Email && item.Email.trim() !== '') ||
        (item.Name && item.Name.trim() !== '')
    );

    filteredData.forEach(item => {
        let displayText = item.AssetID;
        if (item.Name && item.Name.trim() !== '') {
            displayText += ` - ${item.Name}`;
        }
        if (item.Email && item.Email.trim() !== '') {
            displayText += ` (${item.Email})`;
        }
        const option = new Option(displayText, item.AssetID);
        deviceNameContainer.add(option);
    });

    deviceNameWrapper.style.display = 'block';
}

fetchData();
