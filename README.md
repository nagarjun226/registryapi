# Deivce Regitry Service

## Usage

Response Format

```json
{
    "data": "Content of response. Mixed Data",
    "metadata": "Any Metadata"
}
```

Henceforth, we will only show the value of the `data` field

### List all Devices

**Definition**

`GET /devices`

**Response**
- `200 OK` on Success
```json
[
    {
        "device_id": 12345, `string`
        "device_name": "Floor Lamp", `string`
        "device_type": "switch", `string`
        "controller_gateway": "192.1.68.0.3" `string`
    },
    {
        "device_id": 44321, 
        "device_name": "Hue", 
        "device_type": "bulb", 
        "controller_gateway": "192.1.69.0.3" 
    },
    .
    .
    .
]
```

### Registering a new device

**Definition**

`POST /devices`

**Arguments**

- `"name" : string` Human Readable name for this device
- `"controller_gateway": string` IP address of the device's controller

**Response**
- `201 Created` on Success
```json
{
    "device_id": 12345, `string`
    "device_name": "Floor Lamp", `string`
    "device_type": "switch", `string`
    "controller_gateway": "192.1.68.0.3" `string`
},
```

### Look up details of Device

**Definition**

`GET /devices/<device_id>`

**Response**
- `404 Not Found` If the device does not exist
- `200 OK` on Success
```json
{
    "device_id": 12345, `string`
    "device_name": "Floor Lamp", `string`
    "device_type": "switch", `string`
    "controller_gateway": "192.1.68.0.3" `string`
}
```

### Deleting a device

**Definition**

`DELETE /devices/<device_id>`

**Response**
- `404 Not Found` If the device does not exist
- `204 No Content` on success
