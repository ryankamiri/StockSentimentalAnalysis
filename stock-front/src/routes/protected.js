import React, {useContext} from 'react';
import { Navigate } from 'react-router-dom';
import UserContext from '../context/user.context';

const Protected = ({ children }) => {

  const {userData} = useContext(UserContext);

  const renderRoute = () => {
    return children;
  };

  const renderRedirect = (path) => {
    return <Navigate to={path} replace />;
  };

  if(userData.user){
    return renderRoute();
  }
  else{
    return renderRedirect("/login");
  }
}

export default Protected