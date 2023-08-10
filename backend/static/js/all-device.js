async function fetchDevices() {
    console.log(apiUrl + 'device_tracker/api/device/');
    const response = await fetch(apiUrl + '/device_tracker/api/device/');
    const data = await response.json();
    return data;
}

async function displayDevices() {
    const deviceList = document.getElementById('device-list');
    const devices = await fetchDevices();

    devices.forEach(device => {
        const listItem = document.createElement('li');
        listItem.innerHTML = `
            <strong>${device.device_type}</strong> ${device.device_name}: ${device.device_serial_number}
            Status: ${device.device_status}
            IP: ${device.device_ip}
            Ports: ${device.device_ports.join(', ')}
            Department: ${device.department}<br>
        `;
        deviceList.appendChild(listItem);
    });
}

displayDevices();
