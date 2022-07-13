import React, {useState, useContext, useEffect} from 'react';
import UserContext from '../../context/user.context';
import Axios from 'axios';
import Loading from './loading';

export default function Settings() {
    const {userData, setUserData} = useContext(UserContext);

    const [loaded, setLoaded] = useState(false);

    useEffect(() => {
        const getData = async () => {
            setLoaded(true);
        }
    
        getData();
    }, []);

    return (
        <>
        {loaded ? (
            <div>
                <h1>Settings</h1>
            </div>
        ) : (
            <Loading />
        )}
        </>
    )
}