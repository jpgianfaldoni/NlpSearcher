import React from 'react';
import ChosenWebsite from "./components/ChosenWebsite"
import Stack from '@mui/material/Stack';
import './style.css'






class App extends React.Component {

	constructor(){
		super()
		this.state = {
			loading: true,
			searchString:"",
			page: 0,
      dataResult : "",
      chosenPages : [],

		}
    this.handleChange = this.handleChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
	}

	componentDidMount() {
      this.setState({
        loading: false,
    })
	}

  handleChange(event) {
    this.setState({searchString: event.target.value});
  }

  handleSubmit(event) {
    event.preventDefault();
    fetch("http://127.0.0.1:5000/Search?searchString=" + this.state.searchString).then(response => response.json())
    .then(data => {
      this.setState({
        dataResult : data.Search,
        loading: false,
        chosenPages : [],
      })
    })
  }




	
	render(){
    this.state.chosenPages = []
    for (let i = 0; i < this.state.dataResult.length; i++) {
      this.state.chosenPages.push(<ChosenWebsite Info= {this.state.dataResult[i]}/>);
    }
			return(
        this.state.loading ? <div>Loading</div> :
			<div className='mainPage'>
          <div className = 'searchBar'>
              <h1>NLP Searcher</h1>
              <div className='Test'>
                <form onSubmit={this.handleSubmit}>
                <label>
                  <input  type="text" size = "30"  value={this.state.value} onChange={this.handleChange} />
                </label>
                <input  type="submit" value="Enviar" />
              </form>
            </div>
        </div>
        <div className='result'> 
          <Stack spacing={1.2}>
            {this.state.chosenPages}
          </Stack>
        </div> 
			</div>	
      
	)

}
}


export default App;
