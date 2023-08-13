const deviceDetail = document.getElementById('device-detail');
const editForm = document.getElementById('edit-device-form');

const apiEndpoints = {
    device: 'device_tracker/api/device',
    deviceStatus: 'device_tracker/api/device-status',
    port: 'device_tracker/api/port',
    deviceType: 'device_tracker/api/device-type',
    department: 'device_tracker/api/department',
    deviceIP: 'device_tracker/api/department',
};

async function fetchData(endpoint) {
    try {
        const response = await fetch(`${apiUrl}/${endpoint}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error(`Error fetching data from ${endpoint}:`, error);
        return null;
    }
}

async function populateSelectOptions(selectElement, data, valueKey, textKey) {
    data.forEach(item => {
        const option = document.createElement('option');
        option.value = item[valueKey];
        option.textContent = item[textKey];
        selectElement.appendChild(option);
    });
}

async function populateOptions(endpoint, selectId, valueKey, textKey) {
    try {
        const data = await fetchData(endpoint);
        if (data) {
            const selectElement = editForm.querySelector(selectId);
            populateSelectOptions(selectElement, data, valueKey, textKey);
        }
    } catch (error) {
        console.error(`Error populating ${selectId} options:`, error);
    }
}

async function displayDeviceDetail(deviceId) {
    try {
        const device = await fetchData(`${apiEndpoints.device}/${deviceId}/`);
        if (!device) {
            deviceDetail.innerHTML = '<p>Error fetching device details</p>';
            return;
        }

        const detailHTML = `
            <strong>${device.device_type.device_type}</strong> ${device.device_name}: ${device.device_serial_number}
            Status: ${device.device_status.status}
            IP: ${device.device_ip ? device.device_ip.ip : 'N/A'}
            Ports: ${device.device_ports.map(port => port.port).join(', ')}
            Department: ${device.department.department}<br>
        `;

        const deviceNameInput = editForm.querySelector('#device-name');
        const deviceSerialNumberInput = editForm.querySelector('#device-serial-number');
        const deviceStatusSelect = editForm.querySelector('#device-status');
        const deviceIpInput = editForm.querySelector('#device-ip');
        const devicePortsSelect = editForm.querySelector('#device-ports');
        const deviceTypeSelect = editForm.querySelector('#device-type');
        const deviceDepartmentSelect = editForm.querySelector('#department');

        deviceNameInput.value = device.device_name;
        deviceSerialNumberInput.value = device.device_serial_number;
        deviceStatusSelect.value = device.device_status.id;
        deviceIpInput.value = device.device_ip ? device.device_ip.ip : '';

        devicePortsSelect.innerHTML = '';
        await populateOptions(apiEndpoints.port, '#device-ports', 'id', 'port');
        device.device_ports.forEach(port => {
            const option = devicePortsSelect.querySelector(`option[value="${port.id}"]`);
            if (option) {
                option.selected = true;
            }
        });

        deviceTypeSelect.innerHTML = '';
        await populateOptions(apiEndpoints.deviceType, '#device-type', 'id', 'device_type');
        deviceTypeSelect.value = device.device_type.id;

        deviceDepartmentSelect.innerHTML = '';
        await populateOptions(apiEndpoints.department, '#department', 'id', 'department');
        deviceDepartmentSelect.value = device.department.id;

        deviceDetail.innerHTML = detailHTML;
    } catch (error) {
        console.error('Error displaying device details:', error);
    }
}

async function submitUpdatedDevice(deviceId, updatedDevice) {
    try {
        console.log('Sending the following data to server for updating:', updatedDevice);
        const response = await fetch(`${apiUrl}/device_tracker/api/device/${deviceId}/`, {
            method: 'PUT', // Use PUT or PATCH depending on your API
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedDevice),
        });

        if (response.ok) {
            // Device details updated successfully, you might want to refresh the display
            displayDeviceDetail(deviceId);
        } else {
            console.error('Error updating device details:', response.status);
        }
    } catch (error) {
        console.error('Error updating device details:', error);
    }
}

async function getSelectedOptions(selectId) {
    const selectedOptions = [];
    const selectElement = editForm.querySelector(selectId);
    const options = selectElement.options;
    for (let i = 0; i < options.length; i++) {
        if (options[i].selected) {
            selectedOptions.push(parseInt(options[i].value));
        }
    }
    return selectedOptions;
}

editForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(editForm);
    const selectedPorts = await getSelectedOptions('#device-ports');
    const selectedType = parseInt(formData.get('device-type'));
    const selectedDepartment = parseInt(formData.get('department'));

    const updatedDevice = {
        device_name: formData.get('device-name'),
        device_serial_number: formData.get('device-serial-number'),
        device_status: parseInt(formData.get('device-status')),
        device_ip: parseInt(formData.get('device-ip')),
        device_ports: selectedPorts,
        device_type: selectedType,
        department: selectedDepartment,
        // ... other form fields ...
    };

    const deviceId = getDeviceIdFromURL();
    submitUpdatedDevice(deviceId, updatedDevice);
});

function getDeviceIdFromURL() {
    const pathParts = window.location.pathname.split('/');
    const deviceIdIndex = pathParts.indexOf('devices') + 1;
    return pathParts[deviceIdIndex];
}

const deviceId = getDeviceIdFromURL();
displayDeviceDetail(deviceId);
populateOptions(apiEndpoints.deviceStatus, '#device-status', 'id', 'status');
populateOptions(apiEndpoints.port, '#device-ports', 'id', 'port');
populateOptions(apiEndpoints.deviceType, '#device-type', 'id', 'device_type');
populateOptions(apiEndpoints.department, '#department', 'id', 'department');
