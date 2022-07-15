import React, {useState, useContext} from 'react';
import UserContext from '../../context/user.context';
import Axios from 'axios';
import PhoneInput from 'react-phone-input-2'
import sendToast from '../../utils/toast';

export default function Settings() {
    const {userData, setUserData} = useContext(UserContext);

    const [phoneNumber, setPhoneNumber] = useState(userData.user.phoneNumber ? userData.user.phoneNumber.toString() : null);
    const [notificationTarget, setNotificationTarget] = useState(userData.user.notificationTarget ? userData.user.notificationTarget * 100 : null);

    const save = async() => {
        try{
            const saveRes = await Axios.put(process.env.REACT_APP_BACKEND_DOMAIN + "/api/users", {phoneNumber, notificationTarget: notificationTarget / 100}, {headers: {"authorization": userData.token}});
            if(saveRes.data.status){
                const userRes = await Axios.get(process.env.REACT_APP_BACKEND_DOMAIN + '/api/users', {headers: {"authorization": userData.token}});
                setUserData({
                    token: userData.token,
                    user: userRes.data,
                });
                sendToast("Updated account settings.", "success");
            }
        }
        catch(err){
            sendToast(err.response.data.msg, "error");
        }
    };

    return (
        <div className="container">
            <div className="row form-row">
                <div className="col s12 m8 l6 offset-m2 offset-l3">
                <div className="card grey darken-4">
                    <div className="card-content">
                    <span className="card-title">Settings</span>
                    <div className="row">
                        <div className="input-field col s12">
                            <p>{userData.user.firstName} {userData.user.lastName}</p>
                        </div>
                        <div className="input-field col s12">
                            <p>{userData.user.email}</p>
                        </div>
                        <div className="input-field col s12">
                            <PhoneInput id="phoneNumber" country={'us'} value={phoneNumber} onChange={phone => setPhoneNumber(phone)}/>
                        </div>
                        <div className="input-field col s12">
                                <input id="notificationTarget" type="number" value={notificationTarget} onChange={e => setNotificationTarget(e.target.value)}/>
                                <label className="active" htmlFor="notificationTarget">Notification Target (%)</label>
                            </div>
                        <div className="row">
                            <div className="col s12">
                            <button
                                className="
                                btn
                                waves-effect waves-light
                                blue
                                right
                                "
                                onClick={save}
                            >
                                Save
                                <i className="material-icons right">send</i>
                            </button>
                            </div>
                        </div>
                    </div>
                    </div>
                </div>
                </div>
            </div>
        </div>
    )
}