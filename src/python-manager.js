const { spawn } = require('child_process');
const temperatures = []; // Store readings

const sensor = spawn('python', ['sensor.py']);
sensor.stdout.on('data', function(data) {

    // convert Buffer object to Float
    temperatures.push(parseFloat(data));
    console.log(temperatures);
});