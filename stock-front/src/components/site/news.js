import React, {useState, useContext, useEffect, useCallback} from 'react';
import UserContext from '../../context/user.context';
import Axios from 'axios';
import Loading from './loading';
import sendToast from '../../utils/toast';
import parseDate from '../../utils/date';

export default function News() {
    const {userData} = useContext(UserContext);

    const [headlines, setHeadlines] = useState([]);
    const [lastPage, setLastPage] = useState(0);
    const [loaded, setLoaded] = useState(false);
    //const [loadingMore, setLoadingMore] = useState(false);

    const getHeadlines = useCallback(async(notify=false, placement="pre", offset=0) => {
        try{
            const headlinesRes = await Axios.get(process.env.REACT_APP_BACKEND_DOMAIN + "/api/headlines?offset=" + offset, {headers: {"authorization": userData.token}})
            
            setLastPage(headlinesRes.data.lastPage);
            
            setHeadlines(currentHeadlines => {
                const temp = [...currentHeadlines]
                let newHeadlines = false
                for(let i = headlinesRes.data.headlines.length - 1; i >= 0; i--){
                    const headline = headlinesRes.data.headlines[i]
                    const found = temp.some(item => headline._id === item._id);
                    if(!found){
                        newHeadlines = true
                        //New index so add it to headlines
                        if(placement === "pre")
                            temp.unshift(headline)
                        else
                            temp.push(headline)
                    }
                }
                
                temp.sort((a,b) => {
                    return new Date(b.date) - new Date(a.date);
                })

                if(newHeadlines && notify){
                    sendToast("New News!", "info")
                }
                return temp;
            });

        }
        catch (err){
            if(err.response && err.response.status !== 401){
                console.log(err.response.data);
            }
        }
    }, [userData.token]);

    useEffect(() => {
        let loadingMore = false
        const handleScroll = (e) => {
            if(!loadingMore && !lastPage && window.innerHeight + e.target.documentElement.scrollTop + (e.target.documentElement.scrollHeight * .25) + 1 >= e.target.documentElement.scrollHeight){
                loadingMore = true
                getHeadlines(false, "post", headlines.length);
            }
        };

        window.addEventListener("scroll", handleScroll)

        return () => {
            window.removeEventListener("scroll", handleScroll)
        }

    }, [headlines, lastPage, getHeadlines]);

    useEffect(() => {
        getHeadlines()
        const interval = setInterval(() => {
            getHeadlines(true)
        }, 60 * 1000)
        setLoaded(true);

        return () => {
            clearInterval(interval)
        }

    }, [getHeadlines]);

    return (
        <>
        {loaded ? (
            <div className="container">
                <h3 className="center-align">News</h3>
                <table className="striped">
                    <thead>
                    <tr>
                        <th>Headline</th>
                        <th>Analysis</th>
                        <th>Stocks</th>
                        <th>Date</th>
                        <th>Article Link</th>
                    </tr>
                    </thead>

                    <tbody>
                        {headlines.map((headline, i) => {
                            return (
                                <tr key={headline._id}>
                                    <td>{headline.headline}</td>
                                    <td>{headline.sentiment}</td>
                                    <td>{headline.stocks.toString()}</td>
                                    <td>{parseDate(headline.date)}</td>
                                    <td><a className="btn waves-effect waves-light blue" href={headline.url} target="_blank" rel="noreferrer">View Article</a></td>
                                </tr>
                            )
                        })}
                    </tbody>
                </table>
            </div>
        ) : (
            <Loading />
        )}
        </>
    )
}