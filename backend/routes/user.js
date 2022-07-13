const router = require('express').Router();
const auth = require('../middleware/auth');

router.get('/', auth, async (req, res) => {
    try{
        const user = req.user;
        return res.json({
            username: user.username,
            email: user.email
        });
    }
    catch(err){
        return res.status(500).json({msg: err.message});
    }
});

router.put('/', auth, async (req, res) => {
    try{
        const {username} = req.body;
        const user = req.user;
        if(username){
            user.username = username;
        }
        await user.save();
        res.json({status: true});
    }
    catch (err) {
        return res.status(500).json({msg: err.message});
    }
});

router.delete('/', auth, async (req, res) => {
    await User.findByIdAndDelete(req.user._id);
    res.json({msg: 'User deleted.'});
});

module.exports = router;