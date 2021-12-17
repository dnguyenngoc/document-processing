import React from 'react'
import { Route, Switch, Redirect } from "react-router-dom";
import isAuth from "./admin/auth";
import Home from './screens/Home';
import FaceRecognitionDemo from './screens/FaceReconitionDemo';



function PrivateRoute ({component: Component, authed, ...rest}) {
  return (
    <Route
      {...rest}
      render={(props) => authed === true
        ? <Component {...props} />
        : <Redirect to={{pathname: '/login', state: {from: props.location}}} />}
    />
  )
}

export const Routes = () => {
    const auth = isAuth()
    return (
      <Switch>
         {/* <Route path='/login' component={Login} /> */}
         <Route path='/demo/face-recognition' component={FaceRecognitionDemo}/>
         <PrivateRoute authed={auth} path='/' component={Home}/> 

      </Switch>
    );
  };