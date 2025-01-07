const express = require("express");
const {handleSignUp, handleLogin, handleAuthenticate, handleTakeTest, handleLogout, handleTestResults,
    handleShareResults, handleSharedTestResults, handlePredict
} = require("../controllers/indexController");
const router = express.Router();
const logRequest = require("../middlewares/logger");
const authenticateUser = require("../middlewares/auth");
const multer  = require('multer')

const storage = multer.diskStorage({
    destination: function (req, file, cb) {
        cb(null, './uploads')
    },
    filename: function (req, file, cb) {
        cb(null, 'web_snap.png')
    }
})

const upload = multer({storage})


router.post('/signup', handleSignUp);

router.post('/login', handleLogin);

router.post("/take-test", authenticateUser, upload.single('file'), handleTakeTest)
router.post("/predict", upload.single('image'), handlePredict)

router.get('/authenticate', authenticateUser, handleAuthenticate);

router.get('/logout', authenticateUser, handleLogout);

router.get('/test-results', authenticateUser, handleTestResults);
router.get('/test-results/:key', handleSharedTestResults);

router.get('/share-results', authenticateUser, handleShareResults);

module.exports = router;