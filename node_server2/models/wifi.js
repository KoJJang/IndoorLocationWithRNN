var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var wifiSchema = new Schema({
    grid: Number,
    bssid: String,
    ssid: String,
    level: [Number]
});

module.exports = mongoose.model('wifi', wifiSchema);
