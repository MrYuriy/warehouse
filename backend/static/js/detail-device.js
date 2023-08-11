const deviceDetail = document.getElementById('device-detail');
const deviceId = getDeviceIdFromURL();
console.log(deviceId)
async function fetchDeviceDetail() {
    try {
        const response = await fetch(`${apiUrl}/device_tracker/api/device/${deviceId}/`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching device details:', error);
        return null;
    }
}

async function displayDeviceDetail() {
    const device = await fetchDeviceDetail();
    if (!device) {
        deviceDetail.innerHTML = '<p>Error fetching device details</p>';
        return;
    }

    const detailHTML = `
        <strong>${device.device_type.device_type}</strong> ${device.device_name}: ${device.device_serial_number}
        Status: ${device.device_status.status}
        IP: ${device.device_ip} <!-- Assuming device_ip is an array -->
        Ports: ${device.device_ports.map(port => port.port).join(', ')}
        Department: ${device.department.department}<br>
    `;
    deviceDetail.innerHTML = detailHTML;
}

displayDeviceDetail();

function getDeviceIdFromURL() {
    const pathParts = window.location.pathname.split('/');
    const deviceIdIndex = pathParts.indexOf('devices') + 1;
    return pathParts[deviceIdIndex];
}
