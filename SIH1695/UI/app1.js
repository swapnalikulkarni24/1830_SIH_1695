// Mock data for low battery and outliers
const batteryData = [
    { name: 'DWLR1', battery: 50, city: 'City A', state: 'State A' },
    { name: 'DWLR2', battery: 50, city: 'City B', state: 'State B' },
    { name: 'DWLR3', battery: 15, city: 'City C', state: 'State C' },
  ];
  
  const outliersData = {
    '2024-09-22': [
      { name: 'DWLR2', timestamp: '12:00:00' }
    ]
  };
  
  // Function to display the battery table
  function loadBatteryData() {
    const batteryTableBody = document.querySelector('#battery-table tbody');
    batteryTableBody.innerHTML = '';
  
    batteryData.forEach(dwlr => {
      const row = document.createElement('tr');
      row.className = dwlr.battery < 20 ? 'low-battery' : '';
  
      row.innerHTML = `
        <td>${dwlr.name}</td>
        <td>${dwlr.battery}%</td>
        <td>${dwlr.city}</td>
        <td>${dwlr.state}</td>
      `;
      batteryTableBody.appendChild(row);
    });
  }
  
  // Function to display the outliers table based on selected date
  function loadOutliersData() {
    const selectedDate = document.getElementById('date-picker').value;
    const outliersTableBody = document.querySelector('#outliers-table tbody');
    outliersTableBody.innerHTML = '';
  
    if (outliersData[selectedDate]) {
      outliersData[selectedDate].forEach(outlier => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${outlier.name}</td>
          <td>${outlier.timestamp}</td>
        `;
        outliersTableBody.appendChild(row);
      });
    } else {
      outliersTableBody.innerHTML = '<tr><td colspan="2">No outliers found for this date</td></tr>';
    }
  }
  
  // Function to show the requested page
  function showPage(page) {
    const batteryPage = document.getElementById('battery-page');
    const outliersPage = document.getElementById('outliers-page');
  
    if (page === 'battery') {
      batteryPage.style.display = 'block';
      outliersPage.style.display = 'none';
      loadBatteryData();
    } else if (page === 'outliers') {
      batteryPage.style.display = 'none';
      outliersPage.style.display = 'block';
    }
  }
  
  // Load the default page (battery) on load
  window.onload = function () {
    showPage('battery');
  };
  