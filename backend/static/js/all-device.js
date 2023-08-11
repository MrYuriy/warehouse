// all-device.js

async function fetchDevices() {
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
            <strong>${device.device_type}</strong>
            <a class="device-link" href="/device_tracker/devices/${device.id}/">
                 ${device.device_name}: ${device.device_serial_number}
            </a>
            <br>
            Status: ${device.device_status}
            IP: ${device.device_ip}
            Ports: ${device.device_ports.join(', ')}
            Department: ${device.department}<br>
        `;
        deviceList.appendChild(listItem);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    displayDevices();
});
