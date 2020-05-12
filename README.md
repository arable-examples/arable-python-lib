# arable-python-lib

Python client library for [Arable API][Arable API]

**Requirements**: Python 2.7, 3.3+, Pandas 0.24.2

---
## Developer API

[Developer API](https://developer.arable.com/)


## Installation

Clone repository from GitHub using pip:

    $ pip install git+https://github.com/arable-examples/arable-python-lib
    
## Quickstart

Create a client instance:
```python
    import arablepy
    client = arablepy.ArableClient()
```
Provide credentials:
```python
    client.connect(email='email@domain.com', password='password1')
```
Retrieve available tables. Use optional `df` parameter to get response as a pandas DataFrame:
```python
    client.schema(df=True)
```   
Retrieve data dictionary for a specific table:
```python
    client.schema('daily', df=True)
```    
Query data:
```python
    client.data('daily', device='C00####', start_time='2020-01-01T00:00:00Z', end_time='2020-03-26', df=True)
```    
QUERY PARAMETERS

| Parameter | Type                   | Description  |
| --------- |------------------------| -------------|
| cursor    | string <cursor-token>  | Encoded cursor token (for pagination, from X-Cursor-Next response header) |
| limit     | integer `[ 1...10000 ]`| Default: `1000` |
| order     | string                 | Default: `"asc"`. Enum: `"asc"` `"desc"` |
| temp      | string                 | Enum: `"C"` `"F"`. Temperature unit in either [C]elsius or [F]ahrenheit |
| pres      | string                 | Enum: `"mb"` `"kp"` Pressure unit in either millibars [mb] or kilopascals [kp] |
| ratio     | string                 | Enum: `"dec"` `"pct"` Ratio either as percent [pct] or decimal value [dec] |
| size      | string                 | Enum: `"in"` `"mm"` Size unit in either [in]ches or millimeters [mm] |
| speed     | string                 | Enum: `"mps"` `"kph"` `"mph"` Speed unit; meters per second [mps], kilometers per hour [kph], or miles per hour [mph] |
| device    | string                 | Device name, e.g., A000123 (required if location not specified) |
| location  | string                 | Location ID (required if device not specified) |
| local_time| string                 | Local time column specified as timezone name, offset seconds or ISO format(e.g. America/Los_Angeles, -14400, -10: 30)(optional) |
| select    | Array of strings       | Comma-separated column list, e.g., time,device,location,tair |
| start_time| string <date-time>     | Start date/time, e.g., 2019-01-01 or 2019-01-01T00:00:00Z |
| end_time  | string <date-time>     | End date/time, e.g., 2019-01-01 or 2019-01-01T00:00:00Z|

[Arable API]: https://developer.arable.com
