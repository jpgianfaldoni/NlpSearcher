import React from 'react';
import Card from '@material-ui/core/Card';
import Typography from '@material-ui/core/Typography';




class ChosenWebsite extends React.Component {
  constructor() {
    super()
    this.state = {
      loading: true,
      Info: {}
    }
  }

  componentDidMount() {
    this.setState({
      loading: false,
    })
  }







  render() {
    console.log(this.props.Info[2])
    return (
      this.state.loading ? <h1>Loading</h1> :
      <div>
        <a href = {this.props.Info[1]}>{this.props.Info[0]}</a>
        <p>{this.props.Info[2].slice(0,130)}...</p>
      </div>
    );

  }
}



export default ChosenWebsite