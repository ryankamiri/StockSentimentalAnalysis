const express = require('express');
const mongoose = require('mongoose');
const morgan = require('morgan');
const helmet = require('helmet');
const cors = require('cors');

require('dotenv').config();

const app = express();

app.use(express.json({ limit: "1kb" }));
app.use(helmet());
app.use(morgan("dev"));
app.use(cors());

const PORT = process.env.PORT || 5000;

// Set up mongoose

mongoose.connect(process.env.MONGO_URI, {useNewUrlParser: true, useUnifiedTopology: true}, (err) => {
    if (err) {
        console.log("Error on MongoDB connection: " + err.message);
        throw err;
    }
    console.log("MongoDB connection established");
});

// Set up routes
app.use('/api/users', require('./routes/user'));
app.use('/api/auth', require('./routes/auth'));
app.use('/api/headlines', require('./routes/headline'));

const server = app.listen(PORT, () => console.log(`The server has started on port: ${PORT}`));