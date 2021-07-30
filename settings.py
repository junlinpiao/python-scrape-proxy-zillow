# Zillow API Keys
ZILLOW_API_KEYS = [
    'X1-ZWz1dxrmof9ybv_2ninr',
    'X1-ZWz1dxv4yehgqz_55f1z',
    'X1-ZWz1b2nc015gqz_56tmg',
    'X1-ZWz1dxv8wgpkp7_5886x',
    'X1-ZWz1g9z5pxcwln_39zrb',
    'X1-ZWz1gb8jfimc5n_5m9vn',
    'X1-ZWz1gqkkat2zgr_91vx7',
    'X1-ZWz1bvi5ru1gqz_4srxq',
    'X1-ZWz1gqko8vb3ez_94p25',
    'X1-ZWz189xspkbu2z_963mm',
    'X1-ZWz186tfw7fcp7_98wrk', #New
    'X1-ZWz186tby578qz_9bpwi',
    'X1-ZWz186t802z4sr_9ej1g',
    'X1-ZWz1gtpcwevwnf_9fxlx',
    'X1-ZWz186t420r0uj_9hc6e',
    'X1-ZWz186t03yiwwb_9k5bc',
    'X1-ZWz1gtpksjc4jv_9ljvt',
    'X1-ZWz186sw5wasy3_9myga',
    'X1-ZWz1gtpoqlk8i3_9od0r',
    'X1-ZWz186ss7u2ozv_9prl8', #End
    'X1-ZWz1gtsjc7f37v_1pt0f',
    'X1-ZWz186q1kafy8b_1oefy',
    'X1-ZWz1gtsfe56z9n_1mzvh',
    'X1-ZWz186q5ico26j_1llb0'
]


# Enter Property Columns
# Property_Address_Column     =   'F'
# Property_City_Column        =   'G'
# Property_State_Column       =   'H'
# Property_Zip_Column         =   'I'

# Zillow API Error Code
STATUS_CODE_LIST = {
    '0': 'Request successfully processed',
    '1': 'Service error-there was a server-side error while processing the request',
    '2': 'The specified ZWSID parameter was invalid or not specified in the request',
    '3': 'Web services are currently unavailable',
    '4': 'The API call is currently unavailable',
    '7': 'This account has reached is maximum number of calls for today',
    '500': 'Invalid or missing address parameter',
    '501': 'Invalid or missing citystatezip parameter',
    '502': 'No results found',
    '503': 'Failed to resolve city, state or ZIP code',
    '504': 'No coverage for specified area',
    '505': 'Timeout',
    '506': 'Address string too long',
    '507': 'No exact match found.',
    '508': 'No exact match found for input address',
}
