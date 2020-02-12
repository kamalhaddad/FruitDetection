const React = require('react')

class Upload extends React.Component {
  constructor(props){
    super(props)
    this.state = {
        image: null,
        image_name: ""
      }
    this.handleChange = this.handleChange.bind(this)
  }

  handleChange(event) {
    this.setState({
      image: event.target.files[0],
      image_name: event.target.files[0].name,
      display_image : URL.createObjectURL(event.target.files[0])
    }, () => {
        this.props.handler({
            image: this.state.image,
            image_name: this.state.image_name
        })    
    })


  }
  render() {
    return (
      <div>
        <input type="file" onChange={this.handleChange}/>
        <img alt={this.state.image_name} src={this.state.display_image}/>
        
      </div>
    );
  }
}
export default Upload;