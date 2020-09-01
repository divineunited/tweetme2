import React, {useEffect, useState} from 'react';
import logo from './logo.svg';
import './App.css';


function loadTweets(callback) {
  // All modern browsers have a built-in XMLHttpRequest object to request data from a server
      // This object is a dream object because it can:
      // Update a web page without reloading the page
      // Request data from a server - after the page has loaded
      // Receive data from a server  - after the page has loaded
      // Send data to a server - in the background
  // Here, we define our xml request as a JSON type
  const xhr = new XMLHttpRequest()
  const method = 'GET'
  const url = 'http://localhost:8000/api/tweets/'
  xhr.responseType = 'json'

  // We define the XMLHttpRequest to Get at this URL when it opens
  xhr.open(method, url)

  // When the request loads, the XMLHttpRequest will render the final Tweets as a str.
  xhr.onload = function() {
    callback(xhr.response, xhr.status)
  }
  xhr.onerror = function(e) {
    console.log(e)
    callback({"message": "The request was an error"}, 400)
  }
  xhr.send()
}


function Tweet(props) {
  // Tweet functional component
  // props allows us to add in various things to the element. It is like *args.
  const {tweet} = props
  const className = props.className ? props.className : "col-10 mx-auto col-md-6"
  return <div className={className}>
    <p>{tweet.id} - {tweet.content}</p>
  </div>
}


function App() {
  // declare a new STATE variable which we'll call tweets which will utilize a function we call setTweets
  // Now we can call our state below using {tweets}
  const [tweets, setTweets] = useState([])
  useEffect(() => {
    const myCallback = (response, status) => {
      console.log(response, status)
      if (status === 200) {
        setTweets(response)
      } else {
        alert("There was an error.")
      }
    }
    loadTweets(myCallback)
  }, [])
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <div>
          {tweets.map((item, index)=> {
            // always assign keys to each child and each element inside children so React can handle minimal DOM change
            return <Tweet tweet={item} className='my-5 py-5 border bg-white text-dark' key={`${index}-{item.id}`}/>
          })}
        </div>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
