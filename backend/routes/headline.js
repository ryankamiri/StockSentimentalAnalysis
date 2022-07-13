const router = require('express').Router();
const auth = require('../middleware/auth');
const Headline = require('../models/headline.model');

router.get('/', auth, async (req, res) => {
    try{
        const MAXLIMIT = 50
        let offset = req.query.offset
        let limit = req.query.limit
        if(!offset)
            offset = 0
        if(!limit)
            limit = 0
        else if(limit > MAXLIMIT)
            limit = MAXLIMIT
        const headlines = await Headline.find().sort({date: 'descending'}).skip(offset).limit(limit);
        return res.json({
            "headlines": headlines,
            "count": headlines.length,
            "total": await Headline.count()
        })
    }
    catch(err){
        return res.status(500).json({msg: err.message});
    }
});

module.exports = router;