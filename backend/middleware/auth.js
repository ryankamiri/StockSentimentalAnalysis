const User = require('../models/user.model');

const auth = async (req, res, next) => {
    try{
        const token = req.header("authorization");
        if (!token)
            return res.status(401).json({msg: "Unauthorized"});
        
        const user = await User.findOne({tokens: token});
        if (!user)
            return res.status(401).json({msg: "Unauthorized"});
        req.user = user;
        req.token = token;
        next();
    }
    catch (err) {
        res.status(500).json({error: err.message});
    }
    
};

module.exports = auth;