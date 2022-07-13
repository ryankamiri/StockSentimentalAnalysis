const mongoose = require('mongoose');

const Schema = mongoose.Schema;

const headlineSchema = new Schema({
    sentiment: {
        type: Number,
        required: true,
    },
    headline: {
        type: String,
        required: true,
    },
    stocks: {
        type: Array,
        required: true,
    },
    date: {
        type: Date,
        required: true,
    },
    url: {
        type: String,
        required: true,
        unique: true
    },
}, {
    timestamps: true,
});

const Headline = mongoose.model('Headline', headlineSchema);

module.exports = Headline;