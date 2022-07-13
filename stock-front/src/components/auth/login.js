import React, {useState, useContext, useEffect} from 'react';
import {useNavigate} from 'react-router-dom';
import UserContext from '../../context/user.context';
import Axios from 'axios';
import sendToast from '../../utils/toast'
import M from 'materialize-css';

export default function Login() {
    const [email, setEmail] = useState();
    const [password, setPassword] = useState();

    const {userData, setUserData} = useContext(UserContext);
    const navigate = useNavigate();
    
    const login = async() => {
        try{
            const loginUser = {
                email, 
                password
            };
            const loginRes = await Axios.post(process.env.REACT_APP_BACKEND_DOMAIN + '/api/auth/login', loginUser);
            const userRes = await Axios.get(process.env.REACT_APP_BACKEND_DOMAIN + '/api/users', {headers: {"authorization": loginRes.data.token}});
            localStorage.setItem('token', loginRes.data.token);
            setUserData({
                token: loginRes.data.token,
                user: userRes.data,
            });
            sendToast("Successfully Logged In!", "success");
            navigate('/');
            M.Dropdown.init(document.querySelector(".dropdown-trigger"), {
                coverTrigger: false,
            });
        }
        catch (err) {
            if(err.response.data.msg){
                sendToast(err.response.data.msg, "error");
            }
        }
    };

    useEffect(() => {
        if(userData.user)
            return navigate('/');
    }, [userData, navigate]);

    return (
    <>
        <div className="container">
            <div className="row form-row">
                <div className="col s12 m8 l6 offset-m2 offset-l3">
                    <div className="card grey darken-4">
                        <div className="card-content">
                            <span className="card-title">Login</span>
                            <div className="row">
                                <div className="input-field col s12">
                                    <input id="email" type="email" className="validate" onChange={e => setEmail(e.target.value)}/>
                                    <label htmlFor="email">Email</label>
                                </div>
                                <div className="input-field col s12">
                                    <input id="password" type="password" className="validate" onChange={e => setPassword(e.target.value)}/>
                                    <label htmlFor="password">Password</label>
                                </div>
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
                                        onClick={login}
                                    >
                                        Login
                                        <i className="material-icons right">send</i>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </>
    )
}