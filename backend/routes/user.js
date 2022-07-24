const router = require('express').Router();
const auth = require('../middleware/auth');

router.get('/', auth, async (req, res) => {
    try{
        const user = req.user;
        return res.json({
            firstName: user.firstName,
            lastName: user.lastName,
            email: user.email,
            phoneNumber: user.phoneNumber,
            notificationTarget: user.notificationTarget
        });
    }
    catch(err){
        return res.status(500).json({msg: err.message});
    }
});

router.put('/', auth, async (req, res) => {
    try{
        let {phoneNumber, notificationTarget} = req.body;
        const user = req.user;
        if(notificationTarget && notificationTarget < .50){
            return res.status(400).json({msg: "Notification Target must be greater than 50%."})
        }
        else if(!notificationTarget){
            notificationTarget = null;
        }
        user.phoneNumber = phoneNumber;
        user.notificationTarget = notificationTarget;
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