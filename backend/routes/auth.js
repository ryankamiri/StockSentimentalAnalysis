const router = require('express').Router();
const auth = require('../middleware/auth');
const md5 = require("md5");
const crypto = require('crypto');
const bcrypt = require('bcryptjs');
const User = require('../models/user.model');

router.post('/register', async (req, res) => {
    try{
        const {username, email, password, passwordCheck} = req.body;
        // Validate

        if(!username || !email || !password || !passwordCheck)
            return res.status(400).json({msg: "Not all fields have been entered."});
        if (password.length < 8)
            return res.status(400).json({msg: "The password needs to be at least 8 characters long."});
        if (password !== passwordCheck)
            return res.status(400).json({msg: "Please enter the same password twice for verification."});
        
        const existingUser = await User.findOne({email: email})
        if (existingUser)
            return res.status(400).json({msg: "An account with this email already exists."});
        
        const salt = await bcrypt.genSalt(9);
        const passwordHash = await bcrypt.hash(password, salt)
        
        const token = md5(Math.round(Date.now() / 1000) + crypto.randomBytes(16).toString("base64"));

        const newUser = new User({
            email,
            username,
            password: passwordHash,
            tokens: [token]
        });

        await newUser.save();
        return res.json({
            token
        });
        
    }
    catch (err) {
        res.status(500).json({error: err.message});
    }
    
});

router.post('/login', async (req, res) => {
    try{
        const {email, password} = req.body;

        // Validate
        if(!email || !password)
            return res.status(400).json({msg: "Not all fields have been entered."});
        
        const user = await User.findOne({email: email});
        if (!user)
            return res.status(400).json({msg: "No account with this email has been registered."});
        
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch)
            return res.status(400).json({msg: "Invalid credentials."});

        const token = md5(Math.round(Date.now() / 1000) + crypto.randomBytes(16).toString("base64"));
        
        user.tokens.push(token);

        await user.save();

        return res.json({
            token
        });
        
        
    }
    catch (err) {
        res.status(500).json({error: err.message});
    }
});

router.post('/logout', auth, async (req, res) => {
    try{
        
        const index = req.user.tokens.indexOf(req.token);
        if (index <= -1) {
            res.status(500).json({msg: "Invalid index of token"});
        }
        req.user.tokens.splice(index, 1);

        await req.user.save();

        return res.json({
            status: true
        });
        
    }
    catch (err) {
        res.status(500).json({msg: err.message});
    }
});

module.exports = router;