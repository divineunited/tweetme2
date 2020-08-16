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


function App() {
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
        <p>
          {tweets.map((tweet, index)=> {
            return <li>{tweet.content}</li>
          })}
        </p>
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
