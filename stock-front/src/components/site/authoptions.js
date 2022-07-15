import React, {useContext, useEffect} from 'react';
import {useNavigate, Link} from 'react-router-dom';
import UserContext from '../../context/user.context';
import Axios from 'axios';
import M from 'materialize-css';
import toast from '../../utils/toast'

export default function Authoptions() {
    const {userData, setUserData} = useContext(UserContext);

    const navigate = useNavigate();

    const login = () => navigate('/login');
    const register = () => navigate('/register');
    const logout = async () => {
        try{
            const logoutRes = await Axios.post(process.env.REACT_APP_BACKEND_DOMAIN + '/api/auth/logout', null, {headers: {"authorization": userData.token}});
            if(logoutRes.data.status){
                setUserData({
                    token: undefined,
                    user: undefined,
                })
                localStorage.setItem('token', '');
                navigate('/login');
            }
            else{
                toast("Error while trying to logout.", "error");
            }
            
        }
        catch (err){
            console.log(err.response.data);
        }
    };

    useEffect(() => {
        M.Dropdown.init(document.querySelector(".dropdown-trigger"), {
            coverTrigger: false,
        });
    }, []);

    return (
        <div className="auth-options">
            {userData.user ? (
                <>
                    <button
                    className="dropdown-trigger right no-button"
                    data-target="dropdown-profile"
                    >
                        <span className="hide-on-med-and-down">{userData.user.firstName}</span>
                        <i className="material-icons">arrow_drop_down</i>
                    </button>

                    <ul id="dropdown-profile" className="dropdown-content grey darken-3">
                    <li className="hide-on-large-only">
                        <span>{userData.user.firstName}</span>
                    </li>
                    <li>
                        <Link to='/settings'><i className="material-icons">settings</i>Settings</Link>
                    </li>
                    <li className="divider" tabIndex="-1"></li>
                    <li>
                        <a href="/#" onClick={logout}>
                            <i className="material-icons red-text">power_settings_new</i>Logout
                        </a>
                    </li>
                    </ul>
                </>
            ) : (
                <>
                    <span onClick={login} className="right clickable">Login</span>
                    <span onClick={register} className="right clickable">Register</span>
                </>
            )}
        </div>
    )
}
