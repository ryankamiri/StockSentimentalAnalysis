//Import Cores
import React, {useState, useEffect } from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Axios from 'axios';
import { ToastContainer } from 'react-toastify';

//Import components
import Protected from './routes/protected';
import Error404 from './components/site/error404';
import Loading from './components/site/loading';
import UserContext from './context/user.context';
import Register from './components/auth/register';
import Login from './components/auth/login';
import Settings from './components/site/settings';
import News from './components/site/news';
import Navbar from './components/site/navbar';

//Import css
import './index.css';
import 'react-toastify/dist/ReactToastify.css';

export default function App() {

  const [userData, setUserData] = useState({
    token: undefined,
    user: undefined,
  });

  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    const initialize = async () => {
        let token = localStorage.getItem("token");
        if (!token){
            localStorage.setItem('token', '');
            token = '';
        }
        try{
            const userRes = await Axios.get(process.env.REACT_APP_BACKEND_DOMAIN + '/api/users', {headers: {"authorization": token}});
            setUserData({
                token,
                user: userRes.data,
            });
        }
        catch (err){
          if(err.response && err.response.status !== 401){
            console.log(err.response.data);
          }
        }
        setLoaded(true);
    }

    initialize();
  }, []);

  return (
    <>
    {loaded ? (
      <BrowserRouter>
        <UserContext.Provider value={{userData, setUserData}}>
          <Navbar />
          <ToastContainer 
            theme="colored"
            position="top-right"
            autoClose={5000}
            hideProgressBar={false}
            newestOnTop
            closeOnClick
            rtl={false}
            pauseOnFocusLoss
            draggable
            pauseOnHover
          />
          <Routes>
            <Route exact path="/" element={
              <Protected>
                <News />
              </Protected>
            } />
            <Route exact path="/settings" element={
              <Protected>
                <Settings />
              </Protected>
            } />

            <Route exact path="/login" element={<Login />} />
            <Route exact path="/register" element={<Register />} />

            <Route path="*" element={<Error404 />} />
          </Routes>
        </UserContext.Provider>
      </BrowserRouter>
    ) : (
      <Loading />
    )}
    </>
  );
}