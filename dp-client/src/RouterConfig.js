import Home from "./screens/Home";
import FaceRecognitionDemo from "./screens/demo/FaceReconitionDemo";
import IdentityCardDemo from "./screens/demo/IdentityCardDemo";



export const RConfig = {
    Home: { path: "/", component: Home},
    FaceRecognitionDemo: { path: "/demo/face-recognition", component: FaceRecognitionDemo},
    IdentityCardDemo: { path: "/demo/identity-card", component: IdentityCardDemo},


};