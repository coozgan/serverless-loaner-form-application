const url = 'API_URL';
const deviceTypeSelect = document.getElementById('deviceType');
const deviceNameWrapper = document.getElementById('deviceNameWrapper');
const deviceNameContainer = document.getElementById('deviceNameContainer');

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

        deviceTypeSelect.addEventListener('change', populateDeviceNames);
        console.log('Event listener set up for deviceTypeSelect');

        populateDeviceNames();
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

function populateDeviceNames() {
    console.log('Populating device names...');
    const selectedDeviceType = deviceTypeSelect.value;
    console.log('Selected device type:', selectedDeviceType);

    deviceNameContainer.innerHTML = ''; // Clear previous options

    if (selectedDeviceType === "Select Device Type") {
        deviceNameWrapper.style.display = 'none';
        return;
    }

    deviceNameWrapper.style.display = 'block';

    const fragment = document.createDocumentFragment();
    const defaultOption = new Option("Select Device", "");
    fragment.appendChild(defaultOption);

    const filteredData = data.filter(item =>
        item.DeviceType === selectedDeviceType &&
        (!item.Email || item.Email.trim() === '')
    );

    filteredData.forEach(item => {
        const option = new Option(`${item.AssetID}`, item.AssetID);
        fragment.appendChild(option);
    });

    deviceNameContainer.appendChild(fragment);
    console.log('Device names populated');
}

// Rest of the code remains the same...

// Remove any existing event listeners from deviceTypeSelect
deviceTypeSelect.removeEventListener('change', fetchData);

// Call the fetchData function when the app starts
fetchData();
