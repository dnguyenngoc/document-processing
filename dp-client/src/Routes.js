import React from 'react'
import { Route, Switch, Redirect } from "react-router-dom";
import isAuth from "./admin/auth";
import { RConfig } from './RouterConfig';


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
        <Route path={RConfig.FaceRecognitionDemo.path} component={RConfig.FaceRecognitionDemo.component}/>
        <PrivateRoute authed={auth} path={RConfig.Home.path} component={RConfig.Home.component}/> 
    </Switch>
  );
};