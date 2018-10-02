var mongoose = require('mongoose');
var Schema = mongoose.Schema;

var levelSchema = new Schema({
    level: [Number]
});

module.exports = mongoose.model('level', levelSchema);
