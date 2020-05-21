from base64 import b64encode
import pandas as pd
import requests


class ArableClient(object):
    """ A client for connecting to Arable and making data queries.
        >>> from arablepy import ArableClient
        >>> client = ArableClient()
        >>> client.connect(email='user@loremipsum.com', password='#@#SS')
    """
    _base_url = "https://api.arable.cloud/api/v2"
    _param_options = {"device","end_time", "format", "limit", "location", "measure", "order", "select", "start_time", "temp"
                        "pres", "ratio", "size", "speed", "local_time"}

    def __init__(self):
        self.header = None

    def _login(self, email=None, password=None, apikey=None):

        url = "{0}/devices".format(ArableClient._base_url)
        if apikey:
            headers = {"Authorization": "Apikey " + apikey}
            return headers
        # utf-8 encode/decode for python3 support
        elif email and password:
            cred = b64encode("{0}:{1}".format(email, password).encode('utf-8')).decode('utf-8')
            headers = {"Authorization": "Basic " + cred}

            r = requests.get(url, headers=headers)
            if r.status_code == 200:
                return headers
            else:
                r.raise_for_status()

    def _check_connection(self):
        """ Returns True if client has auth token, raises an exception if not. """
        if not self.header:
            raise Exception("Authentication exception: not connected.")
        return True

    def _output(self, url=None, df=False, header=None, params=None):
        r = requests.get(url, headers=header, params=params)
        data = r.json()
        if 200 == r.status_code:
            if df == True:
                if isinstance(data, dict):
                    if 'items' in data.keys():
                        a = len(data['items'])
                        return pd.DataFrame([data['items'][i] for i in range(0,a)])
                    else:
                        return pd.DataFrame([data])
                elif isinstance(data, list):
                    return pd.DataFrame(data)
            else:
                return data
        else:
            r.raise_for_status()

    # class apikeys:

    #     def __init__(self):
    #         self.header = ArableClient.header
        
    def create_apikey(self, scopes=None, name=None, exp=None):
        """
        """

        ArableClient._check_connection()

        url = ArableClient._base_url + "/apikeys"
        params = {}
        if scopes is not None:
            params["scopes"] = scopes
        if name is not None:
            params["name"] = name
        if exp is not None:
            params["exp"] = exp
        headers = self.header.copy()
        headers.update({"content-type": "application/json"})

        r = requests.post(url, headers=headers, json=params)
        if r.status_code == 200:
            return r.json()['apikey']
        else:
            r.raise_for_status()



    def list_apikeys(self, df=False):
        """
        """

        self._check_connection()

        url = ArableClient._base_url + "/apikeys"

        return self._output(url=url, df=df, header=self.header)

    def delete_apikeys(self, apikey_id):
        """
        """

        self._check_connection()

        for i in apikey_id:

            url = ArableClient._base_url + "/apikeys/" + i


            r = requests.delete(url, headers=self.header)

            if r.status_code == 200:
                print("Apikey with ID " + i + " was deleted")
    def scopes(self, df=False):
        """
        """

        self._check_connection()

        url = ArableClient._base_url + "/apikeys/scopes"

        return self._output(url=url, df=df, header=self.header)


    def connect(self, email=None, password=None, apikey=None):
        """ Logs the client in to the API.
            :param email: user email address
            :param password: user password
            >>> client.connect(email='test@loremipsum.com', password='$#$!%')
        """
        # todo: reinstate apikeys in docs
        # :param apikey: user 's apikey (a UUID string)
        #
        # >>> apikey = "<key>"
        # >>> client.connect(apikey=apikey)

        if apikey:
            self.header = self._login(apikey=apikey)
            return
        elif not all([email, password]):
            raise Exception("Missing parameter; connect requires email and password")
        try:
            self.header = self._login(email=email, password=password)
        except Exception as e:
            raise Exception("Failed to connect:\n{}".format(str(e)))

    def devices(self, name=None, order=None, order_by=None, limit=None, page=None, stats=False, battery=False, email=None,
                days=None, locations=False, find=False, df=False):
        """ Lists the devices associated with the user's group.
            >>> client.devices()
            :param df: optional; show response as a pandas DataFrame object.
            :param name: optional; look up a single device by name (serial); ignored if device_id is present
            >>> client.devices(name='C000##')
            :param order: optional; field to order by when looking up multiple devices,
                e.g. "name" for name ascending or "-name" for name descending (default "-last_post")
            :param limit: optional; max number of devices to retrieve when looking up multiple (default 24)
            :param page: optional; results page to retrieve when looking up multiple devices (default 1)
            :param battery: optional; shows battery percentage for 
        """

        self._check_connection()

        url = ArableClient._base_url + "/devices"
        if stats:
            url += "/stats"
        elif name:
            url += "/" + name
            if battery:
                url += "/battery"
            elif locations:
                url += "/locations"
            elif find:
                url += "/find"
           # elif email:
               # url += "/email"

        params = {}
        if order is not None:
            params['order'] = order
        if order_by is not None or name:
            params['order_by'] = order_by
        else:
            params['order_by'] = 'state'    
        if limit is not None:
            params['limit'] = limit
        if page is not None:
            params['page'] = page
        if days is not None:
            params['days'] = days


            # r = requests.post(url, headers=self, )
        return self._output(url=url, df=df, header=self.header, params=params)

    def _query(self, table, params=None):

        self._check_connection()

        url = ArableClient._base_url + "/data/" + table                

        if not params.get('limit'):
            params['limit'] = '10000'

        return self._output(url=url, header=self.header, params=params)

    def data(self, measure, devices, **kwargs):
        """ Query Arable prod data. One of devices or location must be provided, or no data will be retrieved.
            >>> device="C00####"
            >>> start = dt.strftime("%Y-%m-%dT%H:%M:%SZ")
            >>> table = 'daily'
            # Get data in a pandas DataFrame
            >>> client.data(measure, device=device, start_time=start, df=True)
            :param device: device name to retrieve data for (required if location not specified)
            :param location: optional; id of a location to retrieve data for; devices ignored if this is present (required if device not specified)
            :param start_time: beginning of query time range string <date-time> Start date/time, e.g., 2019-01-01 or 2019-01-01T00:00:00Z
            :param df: optional; return pandas dataframe. Default: "False"
            :param end_time: optional; end of query time range string <date-time> End date/time, e.g., 2019-01-01 or 2019-01-01T00:00:00Z
            :param order: optional; string Default: "asc" Enum: "asc" "desc"
            :param limit: optional; maximum number of data points to return; defaults to 1000
            :param select: optional; Comma-separated column list, e.g., time,device,location,tair
            :param cursor: optional; string <cursor-token> Encoded cursor token (for pagination, from X-Cursor-Next response header)
            :param temp: optional; string Enum: "C" "F" Temperature unit in either [C]elsius or [F]ahrenheit
            :param pres: optional; string Enum: "mb" "kp" Pressure unit in either millibars [mb] or kilopascals [kp]
            :param ratio: optional; string Enum: "dec" "pct" Ratio either as percent [pct] or decimal value [dec]
            :param size: optional; string Enum: "in" "mm" Size unit in either [in]ches or millimeters [mm]
            :param speed: optional; string Enum: "mps" "kph" "mph" Speed unit; meters per second [mps], kilometers per hour [kph], or miles per hour [mph]
            :param local_time: optional; string Local time column specified as timezone name, offset seconds or ISO format(e.g. America/Los_Angeles, -14400, -10: 30)(optional)
        """
        df = pd.DataFrame()

        params = {}
        for param in ArableClient._param_options:
            if kwargs.get(param):
                    params[param] = str(kwargs[param])
        for i in devices:
            try:
                params['device'] = str(i)
                # print(params)
                df = df.append(self._query(measure, params=params))
            except:
                continue
                    
        return df

    def schema(self, table=None, df=False):
        """ See available tables and data dictionary for specific tables
            >>> client.schema()
            See schema as pandas DataFrame
            :param table: optional; string. See data dictionary for the specified table
            >>> client.schema('daily', df=True)
        """
        self._check_connection()

        url = ArableClient._base_url + "/schemas"
        if table:
            url += "/" + table
        return self._output(url=url, df=df, header=self.header)

    def locations(self, page=None, limit=None, df=False):
        """ Get all loactions you can access
        """
        self._check_connection()

        url = ArableClient._base_url + "/locations"

        params = {}
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit

        return self._output(url=url, df=df, header=self.header, params=params)

    # class Locations(object):
        
    #     def __init__(self):
            


    def orgs(self, org_id=None, param=None, df=False):
        """
        """
        self._check_connection()

        url = ArableClient._base_url + "/orgs"
        if org_id:
            url += '/' + org_id
        if param:
            url += '/' + param
        return self._output(url=url, df=df, header=self.header)

    def search(self, name, suggest=False, df=False):
        """
        """
        self._check_connection()

        url = ArableClient._base_url + "/search"
        if suggest == True:
            url += "/suggestions"

        params = {}
        params['name'] = name

        return self._output(url=url, df=df, header=self.header, params=params)       

    def team(self):
        pass

    def users(self, page=None, limit=None, df=False):
        """
        """
        self._check_connection()

        url = ArableClient._base_url + "/users"

        params = {}
        if page is not None:
            params['page'] = page
        if limit is not None:
            params['limit'] = limit
        return self._output(url=url, df=df, header=self.header, params=params)
