# arable-python-lib

Python cliennt library for [Arable API][Arable API]

**Requirements**: Python 2.7, 3.3+, Pandas 0.24.2

---

## Installation

Clone repository from GitHub using pip:

    $ pip install git+https://github.com/walterarable/arable-python-lib/
    
## Quickstart

Create a client instance:

    import arablepy
    client = arablepy.ArableClient()
    
Provide credentials:

    client.connect(email='email@domain.com', password='password1')
    
Retrieve available tables. Use optional `df` parameter to get response as a pandas DataFrame:

    client.schema(df=True)
    
Retrieve data dictionary for a specific table:

    client.schema('daily', df=True)
    
Query data:

    client.data('daily', device='C00####', start_time='2020-01-01T00:00:00Z', end_time='2020-03-26', df=True)
    
    
    
[Arable API]: https://developer.arable.com
