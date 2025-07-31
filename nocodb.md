# Create Table Records

This API endpoint allows the creation of new records within a specified table. Records to be inserted are input as an array of key-value pair objects, where each key corresponds to a field name. Ensure that all the required fields are included in the payload, with exceptions for fields designated as auto-increment or those having default values.

When dealing with 'Links' or 'Link To Another Record' field types, you should utilize the 'Create Link' API to insert relevant data.

Certain read-only field types will be disregarded if included in the request. These field types include 'Look Up,' 'Roll Up,' 'Formula,' 'Auto Number,' 'Created By,' 'Updated By,' 'Created At,' 'Updated At,' 'Barcode,' and 'QR Code.'

## path Parameters

| Name     | Type   | Description | require |
| -------- | ------ | ----------- | ------- |
| tableId  | string | Table ID    | true    |

## header Parameters

| Name     | Type   | Description | require |
| -------- | ------ | ----------- | ------- |
| xc-token | string | API Token | true |

## request body
Request Body schema: 
One of objectArray of objects

object (table one row content)
array of objects (table some rows content)

## response
200 OK
Response Schema: application/json

400 Bad Request
Response Schema: application/json
| Name     | Type   | Description | require |
| -------- | ------ | ----------- | ------- |
| msg  | string | Error message | true |

## example

### Request
https://{nocodb-host}/api/v2/tables/{tableId}/records

Content type
application/json
```
[
  {
    "SingleLineText": "David",
    "LongText": "The sunsets in the small coastal town were a breathtaking sight. The sky would transform from a vibrant blue to warm hues of orange and pink as the day came to an end. Locals and tourists alike would gather at the beach, sipping on cool drinks and watching in awe as the sun dipped below the horizon.",
    "CreatedAt": "2023-10-16 08:27:59+00:00",
    "UpdatedAt": "2023-10-16 08:56:32+00:00",
    "Decimal": 23.658,
    "Checkbox": true,
    "Attachment": [
      {
        "url": "https://some-s3-server.com/nc/uploads/2023/10/16/some-key/3niqHLngUKiU2Hupe8.jpeg",
        "title": "2 be loved.jpeg",
        "mimetype": "image/jpeg",
        "size": 146143,
        "signedUrl": "https://some-s3-server.com/nc/uploads/2023/10/16/signed-url-misc-info"
      }
    ],
    "MultiSelect": "Jan,Feb",
    "SingleSelect": "Jan",
    "Date": "2023-10-16",
    "Year": 2023,
    "Time": "06:02:00",
    "PhoneNumber": "123456789",
    "Email": "a@b.com",
    "URL": "www.google.com",
    "Currency": 23,
    "Percent": 55,
    "Duration": 74040,
    "Rating": 1,
    "JSON": {
      "name": "John Doe",
      "age": 30,
      "email": "johndoe@example.com",
      "isSubscribed": true,
      "address": {
        "street": "123 Main Street",
        "city": "Anytown",
        "zipCode": "12345"
      },
      "hobbies": [
        "Reading",
        "Hiking",
        "Cooking"
      ],
      "scores": {
        "math": 95,
        "science": 88,
        "history": 75
      }
    },
    "DateTime": "2023-10-16 08:56:32+00:00",
    "Geometry": "23.23, 36.54",
    "Number": 5248
  }
]
```

### Response
200
```
[
{
"Id": 10
},
{
"Id": 11
}
]
```
or 400
```
{
  "msg": "BadRequest [Error]: <ERROR MESSAGE>"
}
```


https://app.nocodb.com/api/v2/tables/{tableId}/records