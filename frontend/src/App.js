import React, { Component } from 'react';
import axios from 'axios';
import Upload from './Upload';

class App extends Component {

  handleImageChange = (e) => {
    this.setState({
      image: e.target.files[0]
    })
  };

  handleSubmit = (e) => {
    e.preventDefault();
    let form_data = new FormData();
    form_data.append('image', this.state.image);
    form_data.append('title', this.state.image_name);
    let url = 'http://localhost:8000/api/classify/';
    axios.post(url, form_data, {
      headers: {
        'content-type': 'multipart/form-data'
      }
    })
        .then(res => {
          console.log(res.data);
          this.setState({posts: res.data.image});
        })
        .catch(err => console.log(err))
  };

  handler = (e) => {
    console.log(e.image);
    this.setState({
      image:e.image,
      image_name:e.image_name
    })
  };

  state = {
    posts: null
  }
  render() {
    return (
      <div className="App">
        <Upload handler={this.handler}/>
        <div className="parent">
                <form onSubmit={this.handleSubmit}>
                <input value="Classify" type="submit"/>
                </form>            
        </div>
        <div>
            <p>{this.state.posts}</p>
        </div>
      </div>
    );
  }
}

export default App;
