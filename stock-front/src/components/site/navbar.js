import React, {useEffect} from 'react';
import {Link} from 'react-router-dom';
import AuthOptions from "./authoptions";
import M from 'materialize-css';

export default function Navbar() {

    useEffect(() => {
        M.Sidenav.init(document.querySelector(".sidenav"));
    }, []);

    return (
        <header>
            <nav>
                <div className="nav-wrapper grey darken-4">
                    <Link to='/' className="brand-logo">News Ainvesting</Link>
                    <button data-target="mobile-nav" className="sidenav-trigger no-button hide-on-large-only" 
                    ><i className="material-icons">menu</i></button>
                    <ul className="left hide-on-med-and-down">
                        <li><Link to='/'>News</Link></li>
                    </ul>

                    <AuthOptions />
                </div>
                </nav>

                <ul className="sidenav grey darken-4" id="mobile-nav">
                    <li><Link className="white-text" to='/'>News</Link></li>
                </ul>
        </header>
    )
}
