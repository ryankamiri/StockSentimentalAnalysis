import { toast } from 'react-toastify';

const sendToast = (text, typeText) => {
    let type = null
    if (typeText === "info")
        type = toast.TYPE.INFO
    else if (typeText === "success")
        type = toast.TYPE.SUCCESS
    else if (typeText === "warning")
        type = toast.TYPE.WARNING
    else if (typeText === "error")
        type = toast.TYPE.ERROR
    toast(text, {
        position: "top-right",
        type: type,
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
    });
};

export default sendToast;