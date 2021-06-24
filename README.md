# shoppy_analysis

This is a small python script that uses the Shoppy.gg API to gather more data on the payment methods used in your store. The current Shoppy.gg analytics page is lacking to say the least so I found this tool to be a great help in finding which payment methods are used the most and how much revenue each one generates.
## How to Use

To use this tool replace the Authorization field in the request headers. <br> 
```req_headers = {"useragent": "python", "Authorization": "key_here"}``` <br>
You can obtain this key from your Shoppy.gg settings page <br> <br>
![image](https://user-images.githubusercontent.com/30198937/123180371-001f9f80-d440-11eb-9747-da74d7118515.png) <br><br>
After that simply run the script and it will output a file of all your customers emails, ids, purchase gateways, and purchase amounts.
<br>
It also generates a breakdown of the amount purchased through each gateway and the number of times each gateway was used for a purchase.

## Dependencies

```
numpy
pandas
requests
```

